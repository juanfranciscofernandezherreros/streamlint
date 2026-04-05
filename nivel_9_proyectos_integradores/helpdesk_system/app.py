import streamlit as st
from pathlib import Path
import os

# 1. Imports de LangChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# --- CONFIGURACIÓN ---
try:
    from config import CHROMADB_PATH, EMBEDDINGS_MODEL, OPENAI_API_KEY
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
except ImportError:
    CHROMADB_PATH = "/home/usuario/streamlint/nivel_9_proyectos_integradores/dif_system/chroma_db"
    EMBEDDINGS_MODEL = "text-embedding-3-small"

st.set_page_config(page_title="DIF Assistant Pro", page_icon="💪", layout="wide")

@st.cache_resource
def load_rag_system():
    if not Path(CHROMADB_PATH).exists():
        st.error("Error: No se encontró la base de datos de vectores.")
        st.stop()

    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
    db = Chroma(persist_directory=CHROMADB_PATH, embedding_function=embeddings)
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # SYSTEM PROMPT: El cerebro de la operación
    system_prompt = (
        "Eres el asistente experto del gimnasio DIF. "
        "Tu fuente de información es un archivo JSON con el 'Plan Maestro de Entrenamiento - Enero'. "
        "\n\n"
        "INSTRUCCIONES DE RESPUESTA:\n"
        "1. El contexto contiene un JSON con 'calendario_diario' (fechas y salas), "
        "'glosario_modalidades' (descripciones) y 'actividades_fijas_sala_c'.\n"
        "2. Si te preguntan por una fecha, busca el objeto con esa 'fecha' y reporta qué hay en cada sala.\n"
        "3. Si te preguntan por una sala (ej. '¿Qué hay en la Sala A?'), recorre el calendario y resume los entrenamientos de esa sala.\n"
        "4. Usa siempre el 'glosario_modalidades' para explicar qué significa cada entrenamiento si el usuario pregunta.\n"
        "5. Si la información no está en el JSON, di amablemente que solo tienes el plan de enero.\n"
        "\n\n"
        "Contexto:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    
    # k=5 asegura que traiga el día consultado + glosario + actividades fijas
    return create_retrieval_chain(
        db.as_retriever(search_kwargs={"k": 5}), 
        combine_docs_chain
    )

# Inicializar
try:
    qa_chain = load_rag_system()
except Exception as e:
    st.error(f"Error al cargar: {e}")
    st.stop()

# --- INTERFAZ ---
st.title("🏋️‍♂️ Asistente DIF - Plan Enero")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy tu asistente del DIF. ¿Qué quieres saber sobre los entrenamientos de enero?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ej: ¿Qué hay el 21 de enero en la Sala A?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analizando calendario JSON..."):
            response = qa_chain.invoke({"input": user_input})
            answer = response["answer"]
            st.markdown(answer)
            
            with st.expander("🔍 Ver contexto técnico recuperado"):
                for doc in response["context"]:
                    st.json(doc.page_content) # Esto mostrará el JSON recuperado
            
            st.session_state.messages.append({"role": "assistant", "content": answer})