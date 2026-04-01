from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
import os
import streamlit as st
import config

def format_docs(docs):
    formatted = []
    for i, doc in enumerate(docs,1):
        header = f"[Fragmento {i}]  "
        if doc.metadata:
            if 'source' in doc.metadata:
                source = os.path.basename(doc.metadata['source'])
                header += f"({source})  "
            if 'page' in doc.metadata:
                header += f"(Página {doc.metadata['page']})  "
        content = doc.page_content.strip()
        formatted.append(f"{header}\n{content}")
    return "\n\n".join(formatted)

@st.cache_resource
def initialize_rag_system():
    # Vector Store
    vector_store = Chroma(
        embedding_function=OpenAIEmbeddings(model=config.EMBEDDING_MODEL),
        persist_directory=config.CHROMA_DB_PATH
    )
    # Modelos
    llm_query = ChatOpenAI(model=config.QUERY_MODEL, temperature=0.0)
    llm_generation = ChatOpenAI(model=config.GENERATION_MODEL, temperature=0.0)
    # Retriever MMR
    mmr_retriever = vector_store.as_retriever(
        search_type=config.SEARCH_TYPE,
        search_kwargs={
            "fetch_k": config.MMR_FETCH_K,
            "k": config.SEARCH_K,
            "lambda_mult": config.MMR_DIVERSITY_LAMBDA
        })

    # Prompt personalizado para MultiQueryRetriever
    multi_query_prompt = PromptTemplate.from_template(config.MULTI_QUERY_PROMPT)
    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=mmr_retriever,
        llm=llm_query,
        query_prompt=multi_query_prompt
    )
    prompt = PromptTemplate.from_template(config.RAG_TEMPLATE)

    rag_chain = ({
        "context" : multi_query_retriever | format_docs,
        "question" : RunnablePassthrough(),
    }
    | prompt
    | llm_generation
    | StrOutputParser())
    return rag_chain, multi_query_retriever


def query_rag(question):
    rag_chain, multi_query_retriever = initialize_rag_system()

    retrieved_docs = multi_query_retriever.invoke(question)
    response = rag_chain.invoke(question)

    docs = []
    seen = set()
    for i, doc in enumerate(retrieved_docs, 1):
        content = doc.page_content.strip()
        if content in seen:
            continue
        seen.add(content)
        source = ""
        page = ""
        if doc.metadata:
            if 'source' in doc.metadata:
                source = os.path.basename(doc.metadata['source'])
            if 'page' in doc.metadata:
                page = str(doc.metadata['page'])
        docs.append({
            "fragmento": i,
            "fuente": source,
            "pagina": page,
            "contenido": content
        })

    return response, docs


def get_retriever_info():
    return {"tipo": "MultiQuery + MMR"}
