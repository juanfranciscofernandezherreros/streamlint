import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_classic.retrievers import RetrievalQA
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
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0
    )

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

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "lambda_mult": 0.5}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_PROMPT}
    )

    return qa_chain

# -------------------------------
# UI principal
# -------------------------------
def main():
    st.title("🏀 Basket Data Assistant")
    st.caption(f"Base de datos: {CHROMADB_PATH} | Embeddings: {EMBEDDINGS_MODEL}")

    # Inicialización
    vectorstore = load_vectorstore()
    qa_chain = create_qa_chain(vectorstore)

    # Estado del chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input usuario
    if prompt := st.chat_input("¿Qué quieres saber sobre los partidos?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consultando base de datos..."):
                try:
                    response = qa_chain.invoke({"query": prompt})

                    result = response.get("result", "No se obtuvo respuesta.")
                    sources = response.get("source_documents", [])

                except Exception as e:
                    result = f"❌ Error al consultar: {str(e)}"
                    sources = []

                # Mostrar respuesta
                st.markdown(result)

                # Mostrar fuentes
                if sources:
                    with st.expander("📚 Ver fuentes de los datos"):
                        for i, doc in enumerate(sources):
                            src = doc.metadata.get("source", "Desconocido")
                            st.markdown(f"**Fuente {i+1}: {src}**")
                            st.caption(doc.page_content)

        st.session_state.messages.append({
            "role": "assistant",
            "content": result
        })

# -------------------------------
# Ejecutar app
# -------------------------------
if __name__ == "__main__":
    main()