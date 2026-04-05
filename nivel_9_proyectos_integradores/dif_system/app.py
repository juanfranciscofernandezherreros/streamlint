import streamlit as st
from pathlib import Path
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# --- CONFIGURACIÓN ---
BASE_DIR = "/home/usuario/streamlint/nivel_9_proyectos_integradores/dif_system"
CHROMADB_PATH = os.path.join(BASE_DIR, "chroma_db")
EMBEDDINGS_MODEL = "text-embedding-3-small"

st.set_page_config(page_title="DIF Assistant Pro", page_icon="💪", layout="wide")

@st.cache_resource
def load_rag_system():
    if not Path(CHROMADB_PATH).exists():
        st.error("Error: Base de datos no encontrada.")
        st.stop()

    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
    db = Chroma(persist_directory=CHROMADB_PATH, embedding_function=embeddings)
    
    # Usamos GPT-4o-mini (tiene ventana de contexto de 128k, sobra para el JSON)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # AJUSTE 1: Prompt preparado para resúmenes masivos
    system_prompt = (
        "Eres el asistente experto del gimnasio DIF. "
        "Tu fuente es el 'Plan Maestro de Enero' en formato JSON. "
        "\n\n"
        "REGLAS DE ORO:\n"
        "1. Si el usuario pide 'todos los entrenamientos' o un 'resumen del mes', "
        "debes generar una respuesta organizada (preferiblemente una tabla Markdown o lista por semanas) "
        "usando CADA UNO de los días que aparecen en el contexto.\n"
        "2. No resumas de forma vaga; si la información está ahí, lístala.\n"
        "3. Para cada día, indica Sala A, B y C.\n"
        "Contexto:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    
    # AJUSTE 2: k=50 (Aumentamos drásticamente el alcance)
    # Como el mes tiene 31 días + glosario, k=50 asegura que traiga TODO el archivo JSON.
    return create_retrieval_chain(
        db.as_retriever(search_kwargs={"k": 50}), 
        combine_docs_chain
    )

# --- INICIALIZACIÓN ---
try:
    qa_chain = load_rag_system()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

st.title("🏋️‍♂️ Asistente DIF - Planificación Completa")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Puedo darte el horario de un día concreto o el calendario completo del mes. ¿Qué necesitas?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ej: Dame todos los entrenamientos de la Sala A de este mes"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Procesando todo el calendario de enero..."):
            response = qa_chain.invoke({"input": user_input})
            answer = response["answer"]
            st.markdown(answer)
            
            # AJUSTE 3: Ver cuántos fragmentos está leyendo (para tu control)
            with st.expander("📊 Detalles de recuperación"):
                st.write(f"Fragmentos recuperados: {len(response['context'])}")
            
            st.session_state.messages.append({"role": "assistant", "content": answer})