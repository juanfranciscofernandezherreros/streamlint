from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.retrievers.multi_query import MultiQueryRetriever
import streamlit as st
import config

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

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": multi_query_retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm_generation
        | StrOutputParser()
    )

    return chain