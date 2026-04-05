"""
40_streamlit_quiz_exam.py
-------------------------
Aplicación de examen tipo test con Streamlit.

Presenta un cuestionario de preguntas con opciones de respuesta usando
``st.radio`` (botones de selección).  El usuario responde todas las preguntas,
envía el examen y obtiene:

- Puntuación total (aciertos / total).
- Revisión pregunta a pregunta con indicación de correcto / incorrecto.
- Posibilidad de reiniciar el examen.

Las preguntas se definen en la constante ``PREGUNTAS`` como una lista de
diccionarios, lo que facilita ampliar o personalizar el banco de preguntas.

Uso:
    streamlit run nivel_8_aplicaciones/40_streamlit_quiz_exam.py
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Banco de preguntas
# ---------------------------------------------------------------------------
# Cada elemento es un diccionario con:
#   - "pregunta": texto de la pregunta
#   - "opciones": lista de cadenas con las opciones posibles
#   - "respuesta": texto exacto de la opción correcta
# ---------------------------------------------------------------------------

PREGUNTAS = [
    {
        "pregunta": "¿Qué clase de LangChain se usa para crear plantillas de texto plano?",
        "opciones": [
            "ChatPromptTemplate",
            "PromptTemplate",
            "MessagesPlaceholder",
            "SystemMessage",
        ],
        "respuesta": "PromptTemplate",
    },
    {
        "pregunta": "¿Cuál de estos parsers valida la salida con un esquema Pydantic?",
        "opciones": [
            "StrOutputParser",
            "CommaSeparatedListOutputParser",
            "PydanticOutputParser",
            "JsonOutputParser",
        ],
        "respuesta": "PydanticOutputParser",
    },
    {
        "pregunta": "¿Qué componente de LangChain permite ejecutar cadenas en paralelo?",
        "opciones": [
            "SequentialChain",
            "RunnableParallel",
            "ConversationChain",
            "MapReduceChain",
        ],
        "respuesta": "RunnableParallel",
    },
    {
        "pregunta": "¿Qué loader de LangChain se utiliza para leer archivos PDF?",
        "opciones": [
            "WebBaseLoader",
            "CSVLoader",
            "PyPDFLoader",
            "DirectoryLoader",
        ],
        "respuesta": "PyPDFLoader",
    },
    {
        "pregunta": "¿Qué estrategia de splitting divide el texto respetando saltos de párrafo?",
        "opciones": [
            "CharacterTextSplitter",
            "TokenTextSplitter",
            "RecursiveCharacterTextSplitter",
            "SentenceTextSplitter",
        ],
        "respuesta": "RecursiveCharacterTextSplitter",
    },
    {
        "pregunta": "¿Cuál es la base de datos vectorial local que usa este curso?",
        "opciones": [
            "Pinecone",
            "Weaviate",
            "Chroma",
            "FAISS",
        ],
        "respuesta": "Chroma",
    },
    {
        "pregunta": "¿Qué clase de LangGraph define un grafo de estado?",
        "opciones": [
            "AgentExecutor",
            "StateGraph",
            "ConversationChain",
            "DAGScheduler",
        ],
        "respuesta": "StateGraph",
    },
    {
        "pregunta": "¿Qué tipo de memoria conserva TODOS los turnos de la conversación?",
        "opciones": [
            "ConversationSummaryMemory",
            "ConversationBufferWindowMemory",
            "ConversationBufferMemory",
            "ConversationEntityMemory",
        ],
        "respuesta": "ConversationBufferMemory",
    },
    {
        "pregunta": "¿Con qué framework se construyen las interfaces de chat de este curso?",
        "opciones": [
            "Gradio",
            "Flask",
            "Streamlit",
            "Django",
        ],
        "respuesta": "Streamlit",
    },
    {
        "pregunta": "¿Qué operador LCEL conecta un prompt con un modelo en LangChain?",
        "opciones": [
            ">>",
            "&&",
            "|",
            "+",
        ],
        "respuesta": "|",
    },
]


# ---------------------------------------------------------------------------
# Configuración de la página
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="📝 Examen tipo test — LangChain",
    page_icon="📝",
    layout="centered",
)

st.title("📝 Examen tipo test")
st.markdown(
    "Responde a las siguientes preguntas seleccionando **una opción** por "
    "pregunta y pulsa **Enviar examen** cuando termines."
)
st.divider()

# ---------------------------------------------------------------------------
# Estado de la sesión
# ---------------------------------------------------------------------------

if "enviado" not in st.session_state:
    st.session_state.enviado = False
if "respuestas_usuario" not in st.session_state:
    st.session_state.respuestas_usuario = {}


# ---------------------------------------------------------------------------
# Formulario del examen
# ---------------------------------------------------------------------------

with st.form("examen"):
    for idx, p in enumerate(PREGUNTAS):
        st.subheader(f"Pregunta {idx + 1}")
        st.markdown(p["pregunta"])

        clave = f"pregunta_{idx}"
        st.radio(
            label="Selecciona tu respuesta:",
            options=p["opciones"],
            key=clave,
            label_visibility="collapsed",
        )

        if idx < len(PREGUNTAS) - 1:
            st.divider()

    enviado = st.form_submit_button("✅ Enviar examen", use_container_width=True)

    if enviado:
        # Guardar las respuestas seleccionadas
        for idx in range(len(PREGUNTAS)):
            clave = f"pregunta_{idx}"
            st.session_state.respuestas_usuario[idx] = st.session_state.get(
                clave, PREGUNTAS[idx]["opciones"][0]
            )
        st.session_state.enviado = True


# ---------------------------------------------------------------------------
# Resultado y revisión
# ---------------------------------------------------------------------------

if st.session_state.enviado:
    st.divider()
    st.header("📊 Resultado")

    aciertos = 0
    for idx, p in enumerate(PREGUNTAS):
        seleccion = st.session_state.respuestas_usuario.get(
            idx, p["opciones"][0]
        )
        es_correcta = seleccion == p["respuesta"]
        if es_correcta:
            aciertos += 1

    total = len(PREGUNTAS)
    porcentaje = (aciertos / total) * 100 if total else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Aciertos", f"{aciertos}/{total}")
    col2.metric("Porcentaje", f"{porcentaje:.0f} %")
    col3.metric(
        "Calificación",
        "✅ Aprobado" if porcentaje >= 50 else "❌ Suspenso",
    )

    # Barra de progreso visual
    st.progress(porcentaje / 100)

    st.divider()
    st.subheader("🔍 Revisión de respuestas")

    for idx, p in enumerate(PREGUNTAS):
        seleccion = st.session_state.respuestas_usuario.get(
            idx, p["opciones"][0]
        )
        es_correcta = seleccion == p["respuesta"]

        with st.expander(
            f"{'✅' if es_correcta else '❌'} Pregunta {idx + 1}: {p['pregunta']}"
        ):
            st.markdown(f"**Tu respuesta:** {seleccion}")
            if not es_correcta:
                st.markdown(f"**Respuesta correcta:** {p['respuesta']}")

    # Botón para reiniciar
    st.divider()
    if st.button("🔄 Reiniciar examen", use_container_width=True):
        st.session_state.enviado = False
        st.session_state.respuestas_usuario = {}
        st.rerun()
