import streamlit as st
from pathlib import Path
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# --- CONFIGURACIÓN ---
# Mantengo tu ruta de Linux
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
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    system_prompt = (
        "Eres el asistente experto del gimnasio DIF. "
        "Tu fuente es el 'Plan Maestro de Enero' en formato JSON. "
        "\n\n"
        "REGLAS DE ORO:\n"
        "1. Si el usuario pide 'todos los entrenamientos' o un 'resumen del mes', "
        "debes generar una respuesta organizada (tabla Markdown o lista) "
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

# --- LÓGICA DE PREGUNTAS POR DEFECTO ---
st.markdown("### 💡 Consultas Rápidas")
col1, col2, col3, col4 = st.columns(4)

preguntas_frecuentes = [
    "📅 Resumen del mes",
    "🏢 Sala A: Lunes",
    "🔥 Entrenamientos de Fuerza",
    "📋 Horario 15 de Enero"
]

# Variable para capturar la pregunta si se pulsa un botón
pregunta_clicada = None

with col1:
    if st.button(preguntas_frecuentes[0]):
        pregunta_clicada = "Dame un resumen completo de todos los entrenamientos del mes en una tabla"
with col2:
    if st.button(preguntas_frecuentes[1]):
        pregunta_clicada = "¿Cuáles son los entrenamientos de la Sala A todos los lunes de enero?"
with col3:
    if st.button(preguntas_frecuentes[2]):
        pregunta_clicada = "Busca todos los días que tengan entrenamiento enfocado en 'Fuerza'"
with col4:
    if st.button(preguntas_frecuentes[3]):
        pregunta_clicada = "Dime la planificación completa para el día 15 de enero en todas las salas"

st.divider()

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! He preparado unos accesos rápidos arriba, o puedes preguntarme lo que quieras aquí abajo."}]

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Capturar entrada (ya sea por teclado o por botón)
user_input = st.chat_input("Escribe tu duda aquí...")

# Prioridad: Si se hizo clic en un botón, usamos esa pregunta
final_query = pregunta_clicada if pregunta_clicada else user_input

if final_query:
    # Añadir a historial
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"):
        st.markdown(final_query)

    with st.chat_message("assistant"):
        with st.spinner("Consultando el Plan Maestro..."):
            response = qa_chain.invoke({"input": final_query})
            answer = response["answer"]
            st.markdown(answer)
            
            with st.expander("📊 Detalles de recuperación"):
                st.write(f"Fragmentos analizados: {len(response['context'])}")
            
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            # Si fue por botón, forzamos el refresco para que el chat se actualice limpio
            if pregunta_clicada:
                st.rerun()