import streamlit as st
import json
import os
import sys
import io
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- CONFIGURACIÓN DE ENTORNO ---
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Carpeta donde se guardarán los JSONs
CHAT_DIR = "sesiones"
if not os.path.exists(CHAT_DIR):
    os.makedirs(CHAT_DIR)

# --- FUNCIONES DE PERSISTENCIA ---

def obtener_lista_chats():
    """Lista los nombres de archivos .json en la carpeta de sesiones."""
    archivos = [f for f in os.listdir(CHAT_DIR) if f.endswith(".json")]
    # Ordenar por fecha de modificación (más nuevos primero)
    archivos.sort(key=lambda x: os.path.getmtime(os.path.join(CHAT_DIR, x)), reverse=True)
    return archivos

def guardar_chat(nombre_archivo, mensajes):
    """Guarda la lista de mensajes en un archivo específico."""
    ruta = os.path.join(CHAT_DIR, nombre_archivo)
    datos = []
    for m in mensajes:
        tipo = "system" if isinstance(m, SystemMessage) else "human" if isinstance(m, HumanMessage) else "ai"
        datos.append({"type": tipo, "content": m.content})
    
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def cargar_chat(nombre_archivo):
    """Carga mensajes de un archivo específico."""
    ruta = os.path.join(CHAT_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        return [SystemMessage(content="Eres un asistente amigable llamado ChatBot Pro.")]
    
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)
        mensajes = []
        for d in datos:
            if d["type"] == "system": mensajes.append(SystemMessage(content=d["content"]))
            elif d["type"] == "human": mensajes.append(HumanMessage(content=d["content"]))
            else: mensajes.append(AIMessage(content=d["content"]))
        return mensajes

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Chat Manager", page_icon="🗂️", layout="wide")

# Inicializar estados de sesión
if "chat_actual" not in st.session_state:
    st.session_state.chat_actual = None # Ningún archivo seleccionado al inicio
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# --- BARRA LATERAL (GESTIÓN DE SESIONES) ---
with st.sidebar:
    st.title("📂 Mis Conversaciones")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    if st.button("➕ Nueva Conversación", use_container_width=True):
        st.session_state.chat_actual = None
        st.session_state.mensajes = [SystemMessage(content="Eres un asistente amigable.")]
        st.rerun()

    st.divider()
    
    # Listar chats existentes
    chats_disponibles = obtener_lista_chats()
    for chat_file in chats_disponibles:
        nombre_visible = chat_file.replace(".json", "").replace("_", " ")[:25]
        # Botón para seleccionar chat
        if st.button(f"💬 {nombre_visible}...", key=chat_file, use_container_width=True):
            st.session_state.chat_actual = chat_file
            st.session_state.mensajes = cargar_chat(chat_file)
            st.rerun()

# --- ÁREA PRINCIPAL ---
st.title("🤖 ChatBot Multitemático")

# Renderizar chat seleccionado
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage): continue
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Lógica de chat
if api_key:
    chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=api_key)
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="historial"),
        ("human", "{mensaje}")
    ])
    cadena = prompt | chat_model

    pregunta = st.chat_input("¿De qué quieres hablar hoy?")

    if pregunta:
        # Si es un chat nuevo y no tiene archivo, creamos el nombre basado en la pregunta
        if st.session_state.chat_actual is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Limpiar nombre para que sea un nombre de archivo válido
            nombre_base = "".join(x for x in pregunta[:20] if x.isalnum() or x == " ").strip().replace(" ", "_")
            st.session_state.chat_actual = f"{nombre_base}_{timestamp}.json"
            st.session_state.mensajes = [SystemMessage(content="Eres un asistente amigable.")]

        with st.chat_message("user"):
            st.markdown(pregunta)
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = ""
            for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes}):
                full_res += chunk.content
                placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
        
        # Guardar cambios
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_res))
        guardar_chat(st.session_state.chat_actual, st.session_state.mensajes)
else:
    st.info("👈 Introduce tu API Key en la barra lateral para comenzar.")