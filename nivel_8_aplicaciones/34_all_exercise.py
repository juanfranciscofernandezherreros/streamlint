"""
34_all_exercise.py
------------------
Chatbot básico con opciones de configuración, construido con Streamlit y LangChain.

Permite al usuario seleccionar desde la barra lateral:
- **Temperatura** del modelo (creatividad de las respuestas, 0.0–1.0).
- **Modelo** de OpenAI a utilizar (gpt-4o-mini, gpt-4.1-mini, gpt-4.1).
- **Personalidad** del asistente: útil y amigable, profesional, casual,
  experto técnico o creativo.

El historial de conversación se mantiene en ``st.session_state`` durante la
sesión activa y se incluye en cada llamada al modelo (últimos 10 mensajes).
Las respuestas se renderizan con streaming para mejorar la experiencia de usuario.

Uso:
    streamlit run nivel_8_aplicaciones/34_all_exercise.py
"""

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot Básico con LangChain")

with st.sidebar:
    st.header("Configuración")

    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)

    # ✅ MODELOS ACTUALIZADOS
    model_name = st.selectbox(
        "Modelo",
        ["gpt-4o-mini", "gpt-4.1-mini", "gpt-4.1"]
    )

    personalidad = st.selectbox(
        "Personalidad del Asistente",
        [
            "Útil y amigable",
            "Profesional y formal",
            "Casual y relajado",
            "Experto técnico",
            "Creativo y divertido"
        ]
    )

    chat_model = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        streaming=True  # ✅ importante
    )

    system_messages = {
        "Útil y amigable": "Eres un asistente útil y amigable. Responde claro y conciso.",
        "Profesional y formal": "Eres un asistente profesional. Respuestas precisas y estructuradas.",
        "Casual y relajado": "Eres cercano y natural, como un amigo.",
        "Experto técnico": "Eres técnico y detallado. Explica con precisión.",
        "Creativo y divertido": "Eres creativo, usas ejemplos y analogías."
    }

    # ✅ PROMPT MEJORADO
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_messages[personalidad]),
        ("system", "Historial:\n{historial}"),
        ("human", "{mensaje}")
    ])

    cadena = chat_prompt | chat_model

# Estado
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Reset
if st.button("🗑️ Nueva conversación"):
    st.session_state.mensajes = []
    st.rerun()

# Input
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Historial optimizado
    historial = "\n".join(
        [
            f"Usuario: {m.content}" if isinstance(m, HumanMessage)
            else f"Asistente: {m.content}"
            for m in st.session_state.mensajes[-10:]
        ]
    ) or "(Sin historial)"

    try:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            respuesta = ""

            # ✅ STREAMING MÁS SEGURO
            for chunk in cadena.stream({
                "mensaje": pregunta,
                "historial": historial
            }):
                if chunk.content:
                    respuesta += chunk.content
                    placeholder.markdown(respuesta + "▌")

            placeholder.markdown(respuesta)

        # Guardar
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=respuesta))

    except Exception as e:
        st.error(f"Error: {str(e)}")