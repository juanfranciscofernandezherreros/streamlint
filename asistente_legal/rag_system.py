# rag_system.py
import os
import streamlit as st
import config
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableParallel

def format_docs(docs):
    if not docs: return "No hay contexto disponible."
    return "\n\n".join([
        f"[Doc {i+1}] (Fuente: {os.path.basename(d.metadata.get('source', 'S/N'))}, Pág: {d.metadata.get('page', 'S/N')})\n{d.page_content}"
        for i, d in enumerate(docs)
    ])

@st.cache_resource
def initialize_rag_system():
    vector_store = Chroma(
        persist_directory=config.CHROMA_DB_PATH,
        embedding_function=OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
    )
    
    llm_query = ChatOpenAI(model=config.QUERY_MODEL, temperature=0)
    llm_gen = ChatOpenAI(model=config.GENERATION_MODEL, temperature=0)
    
    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 5})

    # Expansión de consulta (Multi-query)
    q_prompt = ChatPromptTemplate.from_template("Genera 3 variantes de esta duda legal: {question}")
    query_chain = q_prompt | llm_query | StrOutputParser() | RunnableLambda(lambda x: x.split('\n'))

    def get_docs(questions):
        all_docs = []
        for q in questions: all_docs.extend(retriever.invoke(q))
        return list({d.page_content: d for d in all_docs}.values()) # Unique

    # --- ARREGLO SECUENCIAL AQUÍ ---
    prompt = ChatPromptTemplate.from_template(config.RAG_TEMPLATE)

    chain = (
        RunnableParallel({
            "docs": query_chain | RunnableLambda(get_docs),
            "question": RunnablePassthrough()
        })
        .assign(context=lambda x: format_docs(x["docs"]))  # Primero creamos context
        .assign(answer=(prompt | llm_gen | StrOutputParser())) # Luego generamos respuesta
    )
    return chain

def query_rag(question):
    chain = initialize_rag_system()
    result = chain.invoke({"question": question})
    
    processed_docs = [{
        "fragmento": i+1,
        "fuente": os.path.basename(d.metadata.get('source', 'Desconocido')),
        "pagina": str(d.metadata.get('page', 'S/N')),
        "contenido": d.page_content
    } for i, d in enumerate(result["docs"])]
    
    return result["answer"], processed_docs

def get_retriever_info():
    return {"tipo": "Multi-Query Secuencial (FIXED)"}