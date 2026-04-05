# ⭐⭐⭐⭐⭐ Nivel 8 — Aplicaciones: Apps con Streamlit

Aplicaciones web completas construidas con **Streamlit** y **LangChain**: chatbots configurables, persistencia de sesiones y exámenes interactivos.

## Scripts

| # | Archivo | Descripción |
|---|---------|-------------|
| 38 | `38_all_exercise.py` | Chatbot con opciones de configuración (temperatura, modelo, personalidad) en la barra lateral. |
| 39 | `39_streamlit_chatbox.py` | Chatbot completo con streaming, gestión de múltiples conversaciones y persistencia en JSON. |
| 40 | `40_streamlit_quiz_exam.py` | Examen tipo test con `st.radio`, puntuación automática y revisión de respuestas. |

## Conceptos clave

- **Streamlit** — Framework Python para crear aplicaciones web interactivas.
- **`st.chat_message`** / **`st.chat_input`** — Componentes de chat nativo de Streamlit.
- **`st.session_state`** — Estado de sesión para mantener datos entre recargas.
- **Streaming** — Respuestas en tiempo real token a token.
- **Persistencia en JSON** — Guardar y recuperar conversaciones desde archivos.

## Ejecución

```bash
streamlit run nivel_8_aplicaciones/38_all_exercise.py        # Chatbot configurable
streamlit run nivel_8_aplicaciones/39_streamlit_chatbox.py   # Chatbot con persistencia
streamlit run nivel_8_aplicaciones/40_streamlit_quiz_exam.py # Examen tipo test
```

## Requisitos

- `streamlit`, `langchain`, `langchain-openai`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada (también puede introducirse desde la barra lateral en la app).

## Navegación

⬅️ [Nivel 7 — LangGraph](../nivel_7_langgraph/) · ➡️ [Nivel 9 — Proyectos Integradores](../nivel_9_proyectos_integradores/)
