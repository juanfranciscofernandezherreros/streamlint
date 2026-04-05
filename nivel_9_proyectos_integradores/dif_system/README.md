# DIF System — Asistente de Horarios de Gimnasio

Asistente inteligente para consultas sobre **horarios de actividades de gimnasio**. Usa RAG sobre un plan de clases almacenado en JSON para responder preguntas sobre horarios, salas, actividades y más.

## Estructura

```text
dif_system/
├── app.py          # Interfaz Streamlit
├── config.py       # Configuración (rutas, modelos)
├── setup_rag.py    # Indexación del plan de clases
└── docs/
    └── enero.json  # Plan de clases de enero (datos de ejemplo)
```

## ¿Cómo funciona?

1. **Indexación** (`setup_rag.py`): Lee el plan de clases en JSON, genera embeddings y crea un índice vectorial.
2. **Consulta** (`app.py`): El usuario hace preguntas en lenguaje natural y el sistema recupera la información relevante del plan de clases.

## Ejecución

```bash
# 1. Indexar el plan de clases (solo la primera vez)
python nivel_9_proyectos_integradores/dif_system/setup_rag.py

# 2. Lanzar el asistente
streamlit run nivel_9_proyectos_integradores/dif_system/app.py
```

## Preguntas de ejemplo

- ¿Qué clases hay el 21 de enero?
- ¿Qué actividad hay en la Sala A el 3 de enero?
- ¿Qué días hay GAP en enero?
- ¿Cuándo hay DEKA-DIF?
- ¿Qué es Strong?
- ¿Cuánto dura Power Play?
- ¿Qué horario tiene DIF Senior?
- ¿Cuándo hay fútbol?
- ¿Hay Pilates entre semana?

## Requisitos

- `langchain`, `langchain-openai`, `langchain-community`, `faiss-cpu`, `streamlit`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.

## Tecnologías

- **FAISS** — Índice vectorial para búsqueda semántica.
- **Streamlit** — Interfaz web de chat.
- **LangChain** — Pipeline RAG.
