import streamlit as st

# 1. Imports de LangChain (Estándar v1.x / 2026)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# --- CONFIGURACIÓN ---
from config import CHROMADB_PATH, EMBEDDINGS_MODEL

st.set_page_config(page_title="DIF - Clases GAP", page_icon="💪")
st.title("🏋️‍♂️ Asistente de Clases GAP (OpenAI)")

# Inicializar componentes
@st.cache_resource
def load_rag():
    # Inicializar embeddings y base de datos
    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
    
    # Cargamos la base de datos de Chroma
    db = Chroma(
        persist_directory=CHROMADB_PATH, 
        embedding_function=embeddings
    )
    
    # Configuramos el modelo (GPT-4o mini)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # Definimos el System Prompt (Lógica de negocio)
    system_prompt = (
        "Eres un asistente virtual del gimnasio. Tu especialidad absoluta son las clases de GAP (Glúteos, Abdominales y Piernas). "
        "Usa exclusivamente el contexto proporcionado para responder. "
        "Si la pregunta no está relacionada con GAP o el gimnasio, responde amablemente que solo tienes "
        "información sobre horarios y clases de GAP.\n\n"
        "Contexto:\n{context}"
    )
    
    # Creamos el template de chat
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Creamos la cadena de procesamiento de documentos
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    # Creamos la cadena final de recuperación
    return create_retrieval_chain(
        db.as_retriever(search_kwargs={"k": 3}), 
        question_answer_chain
    )

# Cargar la cadena
try:
    qa_chain = load_rag()
except Exception as e:
    st.error(f"Error al cargar la base de datos: {e}")
    st.stop()

# --- INTERFAZ DE CHAT ---

# Inicializar historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Entrada del usuario
if user_input := st.chat_input("¿Qué quieres saber de GAP? (ej: ¿Hay clase el lunes?)"):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Consultando horarios..."):
            # En la versión moderna usamos .invoke() y el campo es "input"
            response = qa_chain.invoke({"input": user_input})
            answer = response["answer"]
            
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})