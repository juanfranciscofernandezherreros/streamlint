"""
app.py
------
Aplicación principal del Asistente Legal de Contratos de Arrendamiento.

Permite consultar el contenido de contratos de arrendamiento indexados en
ChromaDB mediante un sistema RAG con MultiQueryRetriever y MMR.

Uso:
    streamlit run asistente_legal/app.py
"""

import os
import sys
import io
import streamlit as st

# Asegurar codificación UTF-8 para evitar errores en terminales Linux
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Añadir el directorio actual al path para que los imports relativos funcionen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_system import initialize_rag_system

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Asistente Legal - Contratos de Arrendamiento",
    page_icon="⚖️",
    layout="wide"
)

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("⚖️ Asistente Legal")
    st.markdown("Consulta inteligente de contratos de arrendamiento.")
    st.divider()

    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Introduce tu clave de API de OpenAI para activar el asistente."
    )

    st.divider()
    st.markdown(
        "**Cómo funciona:**\n"
        "- Recupera fragmentos relevantes de los contratos indexados\n"
        "- Usa MultiQueryRetriever para ampliar la búsqueda\n"
        "- Genera una respuesta fundamentada en los documentos"
    )

# --- ÁREA PRINCIPAL ---
st.title("⚖️ Asistente Legal de Contratos de Arrendamiento")
st.markdown(
    "Haz preguntas sobre los contratos indexados: "
    "arrendadores, arrendatarios, importes, fechas, condiciones, etc."
)

# Inicializar historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial
for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Lógica de consulta
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

    try:
        chain = initialize_rag_system()
    except Exception as e:
        st.error(f"Error al inicializar el sistema RAG: {e}")
        st.stop()

    pregunta = st.chat_input("Escribe tu consulta sobre los contratos...")

    if pregunta:
        # Mostrar pregunta del usuario
        with st.chat_message("user"):
            st.markdown(pregunta)
        st.session_state.mensajes.append({"role": "user", "content": pregunta})

        # Generar y mostrar respuesta con streaming
        with st.chat_message("assistant"):
            placeholder = st.empty()
            respuesta = ""
            try:
                for chunk in chain.stream(pregunta):
                    respuesta += chunk
                    placeholder.markdown(respuesta + "▌")
                placeholder.markdown(respuesta)
            except Exception as e:
                placeholder.error(f"Error al generar la respuesta: {e}")
                respuesta = ""

        if respuesta:
            st.session_state.mensajes.append({"role": "assistant", "content": respuesta})

    if st.session_state.mensajes:
        if st.button("🗑️ Limpiar conversación", use_container_width=False):
            st.session_state.mensajes = []
            st.rerun()

else:
    st.warning("⚠️ Introduce tu OpenAI API Key en la barra lateral para empezar.")
