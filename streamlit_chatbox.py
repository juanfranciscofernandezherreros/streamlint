import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. Configuración de la página
st.set_page_config(page_title="Chatbot Pro", page_icon="🤖")
st.title("🤖 Chatbot Básico con LangChain")
st.markdown("Este es un chatbot que mantiene el contexto de la conversación.")

# 2. Sidebar para configuración
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("OpenAI API Key", type="password")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.7, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
    
    if st.button("🗑️ Nueva conversación"):
        st.session_state.mensajes = [
            SystemMessage(content="Eres un asistente útil y amigable llamado ChatBot Pro.")
        ]
        st.rerun()

# 3. Inicializar el historial de mensajes en session_state
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        SystemMessage(content="Eres un asistente útil y amigable llamado ChatBot Pro.")
    ]

# 4. Renderizar historial existente (excluyendo el SystemMessage)
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        continue
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# 5. Lógica principal de entrada y respuesta
if api_key:
    # Definición del modelo y la cadena (LCEL)
    chat_model = ChatOpenAI(model=model_name, temperature=temperature, api_key=api_key)
    
    prompt_template = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="historial"),
        ("human", "{mensaje}")
    ])
    
    cadena = prompt_template | chat_model

    # Input del usuario
    pregunta = st.chat_input("Escribe tu mensaje aquí...")

    if pregunta:
        # Mostrar mensaje del usuario en la UI
        with st.chat_message("user"):
            st.markdown(pregunta)
        
        # Generar respuesta con streaming
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            try:
                # El historial se pasa tal cual está en session_state
                # La pregunta actual se pasa al placeholder {mensaje}
                for chunk in cadena.stream({
                    "mensaje": pregunta, 
                    "historial": st.session_state.mensajes
                }):
                    full_response += chunk.content
                    response_placeholder.markdown(full_response + "▌")
                
                # Quitar el cursor final
                response_placeholder.markdown(full_response)
                
                # 6. Guardar la interacción en el historial para la próxima vuelta
                st.session_state.mensajes.append(HumanMessage(content=pregunta))
                st.session_state.mensajes.append(AIMessage(content=full_response))

            except Exception as e:
                st.error(f"Hubo un error: {str(e)}")
else:
    st.info("Por favor, introduce tu OpenAI API Key en la barra lateral para empezar a chatear.")