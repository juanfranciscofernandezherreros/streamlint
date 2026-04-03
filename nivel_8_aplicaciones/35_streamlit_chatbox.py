"""
33_streamlit_chatbox.py
-----------------------
Aplicación principal de chatbot construida con Streamlit y LangChain.

Características:
- Interfaz de chat interactiva con streaming de respuestas en tiempo real.
- Gestión de múltiples conversaciones con persistencia en archivos JSON dentro
  de la carpeta ``sesiones/``.
- Historial de chats recientes accesible desde la barra lateral.
- Configuración de la API Key de OpenAI directamente desde la interfaz.
- Cadena LCEL basada en ``ChatPromptTemplate`` + ``MessagesPlaceholder`` que
  mantiene el contexto completo de la conversación en cada llamada al modelo.

Uso:
    streamlit run nivel_7_aplicaciones/33_streamlit_chatbox.py
"""

import streamlit as st
import json
import os
import sys
import io
from pathlib import Path
from datetime import datetime

# --- LANGCHAIN IMPORTS ---
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- CONFIGURACIÓN DE ENTORNO ---
# Asegurar codificación UTF-8 para evitar errores en terminales Linux
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Carpeta donde se guardarán las sesiones JSON
CHAT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sesiones")
if not os.path.exists(CHAT_DIR):
    os.makedirs(CHAT_DIR)

# --- FUNCIONES DE PERSISTENCIA ---

def _ruta_segura(nombre_archivo: str) -> Path:
    """Devuelve la ruta absoluta del archivo dentro de CHAT_DIR.

    Usa pathlib para resolver cualquier componente '..' y verifica que la
    ruta resultante esté dentro de CHAT_DIR, evitando ataques de path traversal.
    Lanza ValueError si la ruta resultante escapa del directorio permitido.
    """
    base = Path(CHAT_DIR).resolve()
    ruta = (base / Path(nombre_archivo).name).resolve()
    ruta.relative_to(base)  # lanza ValueError si ruta no está dentro de base
    return ruta

def obtener_lista_chats():
    """Lista los nombres de archivos .json en la carpeta de sesiones."""
    if not os.path.exists(CHAT_DIR): return []
    archivos = [f for f in os.listdir(CHAT_DIR) if f.endswith(".json")]
    # Ordenar por fecha de modificación (más nuevos primero)
    archivos.sort(key=lambda x: os.path.getmtime(os.path.join(CHAT_DIR, x)), reverse=True)
    return archivos

def guardar_chat(nombre_archivo, mensajes):
    """Guarda la lista de mensajes en un archivo JSON."""
    ruta = _ruta_segura(nombre_archivo)
    datos = []
    for m in mensajes:
        if isinstance(m, SystemMessage): tipo = "system"
        elif isinstance(m, HumanMessage): tipo = "human"
        else: tipo = "ai"
        datos.append({"type": tipo, "content": m.content})
    
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def cargar_chat(nombre_archivo):
    """Carga mensajes de un archivo específico convirtiéndolos a objetos LangChain."""
    ruta = _ruta_segura(nombre_archivo)
    if not os.path.exists(ruta):
        return [SystemMessage(content="Eres un asistente amigable.")]
    
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)
        mensajes = []
        for d in datos:
            if d["type"] == "system": mensajes.append(SystemMessage(content=d["content"]))
            elif d["type"] == "human": mensajes.append(HumanMessage(content=d["content"]))
            else: mensajes.append(AIMessage(content=d["content"]))
        return mensajes

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Chat Manager Pro", page_icon="🤖", layout="wide")

# Inicializar estados de sesión
if "chat_actual" not in st.session_state:
    st.session_state.chat_actual = None
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("📂 Gestión de Chats")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    
    if st.button("➕ Nueva Conversación", use_container_width=True):
        st.session_state.chat_actual = None
        st.session_state.mensajes = [SystemMessage(content="Eres un asistente amigable.")]
        st.rerun()

    st.divider()
    st.subheader("Historial Reciente")
    
    chats_disponibles = obtener_lista_chats()
    for chat_file in chats_disponibles:
        nombre_visible = chat_file.replace(".json", "").replace("_", " ")[:20]
        if st.button(f"💬 {nombre_visible}...", key=chat_file, use_container_width=True):
            st.session_state.chat_actual = chat_file
            st.session_state.mensajes = cargar_chat(chat_file)
            st.rerun()

# --- ÁREA PRINCIPAL ---
st.title("🤖 ChatBot con PromptTemplate")

# Renderizar mensajes existentes (excluyendo el SystemMessage)
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage): continue
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Lógica de Chat
if api_key:
    # 1. Configuración del Modelo
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=api_key)
    
    # 2. Definición del PromptTemplate
    # El MessagesPlaceholder es clave para insertar el historial de la sesión
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="historial"),
        ("human", "{entrada_usuario}")
    ])
    
    # Cadena LCEL
    chain = prompt | llm

    pregunta = st.chat_input("Escribe tu mensaje...")

    if pregunta:
        # Generar nombre de archivo si es el primer mensaje
        if st.session_state.chat_actual is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            nombre_limpio = "".join(x for x in pregunta[:15] if x.isalnum() or x == " ").strip().replace(" ", "_")
            st.session_state.chat_actual = f"{nombre_limpio}_{timestamp}.json"
            if not st.session_state.mensajes:
                st.session_state.mensajes.append(SystemMessage(content="Eres un asistente amigable."))

        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(pregunta)
        
        # Respuesta de la IA con streaming
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = ""
            
            # Pasamos las variables al template: historial completo + pregunta actual
            for chunk in chain.stream({
                "historial": st.session_state.mensajes, 
                "entrada_usuario": pregunta
            }):
                full_res += chunk.content
                placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
        
        # Actualizar historial y guardar en disco
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_res))
        guardar_chat(st.session_state.chat_actual, st.session_state.mensajes)

else:
    st.warning("⚠️ Por favor, introduce tu OpenAI API Key en la barra lateral para continuar.")

# Pie de página informativo
if st.session_state.chat_actual:
    st.caption(f"Archivo actual: `{st.session_state.chat_actual}`")