import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from config import *

# -------------------------------
# Configuración de la página
# -------------------------------
st.set_page_config(
    page_title="Basketball RAG Assistant",
    page_icon="🏀",
    layout="wide"
)

# -------------------------------
# Cargar Vectorstore (cacheado)
# -------------------------------
@st.cache_resource
def load_vectorstore():
    # Asegúrate de que EMBEDDINGS_MODEL y CHROMADB_PATH estén en tu config.py
    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
    vectorstore = Chroma(
        persist_directory=CHROMADB_PATH,
        embedding_function=embeddings
    )
    return vectorstore

# -------------------------------
# Crear cadena RAG
# -------------------------------
def create_qa_chain(vectorstore):
    # LLM principal para la respuesta y para generar múltiples consultas
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0
    )

    # 1. Definición del Prompt (Personalidad)
    template = """Eres un analista experto en baloncesto.

Usa EXCLUSIVAMENTE el contexto proporcionado para responder.
- No inventes información.
- Si no encuentras la respuesta en el contexto, di claramente: "No lo sé con los datos disponibles".
- Incluye detalles como equipos, fechas y resultados cuando sea posible.

Contexto:
{context}

Pregunta: {question}

Respuesta:"""

    QA_PROMPT = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    # 2. Configuración del MultiQueryRetriever
    # Esto genera varias versiones de la pregunta del usuario para mejorar la recuperación
    base_retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "lambda_mult": 0.5}
    )
    
    mq_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm
    )

    # 3. Creación de la cadena de QA (RetrievalQA)
    # Aquí es donde se usa correctamente .from_chain_type
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=mq_retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_PROMPT}
    )

    return qa_chain

# -------------------------------
# UI principal
# -------------------------------
def main():
    st.title("🏀 Basket Data Assistant")
    st.caption(f"Base de datos: `{CHROMADB_PATH}` | Embeddings: `{EMBEDDINGS_MODEL}`")

    # Inicialización de componentes
    try:
        vectorstore = load_vectorstore()
        qa_chain = create_qa_chain(vectorstore)
    except Exception as e:
        st.error(f"Error al inicializar la base de datos: {e}")
        return

    # Estado del chat (Historial)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial de la sesión
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input del usuario
    if prompt := st.chat_input("¿Qué quieres saber sobre los partidos?"):
        # Añadir mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generar respuesta del asistente
        with st.chat_message("assistant"):
            with st.spinner("Consultando base de datos y analizando jugadas..."):
                try:
                    # RetrievalQA usa "query" como input por defecto
                    response = qa_chain.invoke({"query": prompt})

                    result = response.get("result", "No se obtuvo respuesta.")
                    sources = response.get("source_documents", [])

                except Exception as e:
                    result = f"❌ Error al consultar: {str(e)}"
                    sources = []

                # Mostrar respuesta final
                st.markdown(result)

                # Mostrar fuentes (metadatos y contenido)
                if sources:
                    with st.expander("📚 Ver fuentes consultadas"):
                        for i, doc in enumerate(sources):
                            src = doc.metadata.get("source", "Documento local")
                            st.markdown(f"**Fuente {i+1}:** `{src}`")
                            st.info(doc.page_content)

        # Guardar respuesta en el historial
        st.session_state.messages.append({
            "role": "assistant",
            "content": result
        })

# -------------------------------
# Ejecución
# -------------------------------
if __name__ == "__main__":
    main()