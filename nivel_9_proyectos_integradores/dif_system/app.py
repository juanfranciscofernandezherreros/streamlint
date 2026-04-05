import streamlit as st
from pathlib import Path

# 1. Imports de LangChain (Rutas oficiales)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
# Estas son las librerías correctas para las cadenas de recuperación
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# --- CONFIGURACIÓN DE RUTAS (dinámicas desde config.py) ---
# Asegúrate de que config.py exista en el mismo directorio
try:
    from config import CHROMADB_PATH, EMBEDDINGS_MODEL
except ImportError:
    st.error("No se encontró config.py. Por favor, crea el archivo con CHROMADB_PATH y EMBEDDINGS_MODEL.")
    st.stop()

# Configuración de página
st.set_page_config(page_title="DIF - Horarios GAP", page_icon="🏋️‍♂️")

st.title("🏋️‍♂️ Asistente DIF - Enero")
st.markdown("Consulta horarios de **GAP**, actividades en salas y el plan de entrenamiento.")

# --- LÓGICA RAG ---

@st.cache_resource
def load_rag_system():
    # Validar que existe la DB
    if not Path(CHROMADB_PATH).exists():
        st.error(f"No se encontró la base de datos en: {CHROMADB_PATH}")
        st.info("Asegúrate de que setup_rag.py se ejecutó correctamente.")
        st.stop()

    # Inicializar componentes
    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
    
    db = Chroma(
        persist_directory=CHROMADB_PATH, 
        embedding_function=embeddings
    )
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # System Prompt optimizado
    system_prompt = (
        "Eres el asistente oficial del gimnasio DIF. "
        "Tu fuente de verdad es el 'Plan Maestro de Entrenamiento - Enero'. "
        "Responde preguntas sobre las Salas A, B y C, horarios de GAP y modalidades. "
        "Si la información no está en el contexto, indica que solo tienes el plan de Enero disponible.\n\n"
        "Contexto:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Construcción de la cadena (Uso de las funciones oficiales)
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(
        db.as_retriever(search_kwargs={"k": 5}), 
        combine_docs_chain
    )
    
    return retrieval_chain

# Cargar sistema con manejo de errores
try:
    qa_chain = load_rag_system()
except Exception as e:
    st.error(f"Error crítico al cargar el sistema: {e}")
    st.stop()

# --- INTERFAZ DE CHAT ---

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if user_query := st.chat_input("¿Qué clase hay el 21 de enero en la Sala A?"):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Revisando el Plan Maestro..."):
            try:
                # Invocar la cadena
                response = qa_chain.invoke({"input": user_query})
                answer = response["answer"]
                
                st.markdown(answer)
                
                # Mostrar fuentes en un expansor
                with st.expander("Ver fuentes"):
                    for i, doc in enumerate(response["context"]):
                        st.caption(f"Fragmento {i+1}: {doc.page_content[:200]}...")
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e: 
                st.error(f"Hubo un error en la consulta: {e}")