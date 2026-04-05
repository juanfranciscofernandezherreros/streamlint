# Asistente Legal — RAG para Contratos

Sistema **RAG** (Retrieval-Augmented Generation) completo para consulta de contratos de arrendamiento. Ingesta PDFs a un índice FAISS, utiliza `MultiQueryRetriever` para mejorar la recuperación y ofrece una interfaz de chat con Streamlit.

## Estructura

```text
asistente_legal/
├── app.py          # Interfaz de chat Streamlit
├── config.py       # Configuración del proyecto (rutas, modelos)
├── ingest.py       # Ingesta de PDFs y creación del índice FAISS
├── prompt.py       # Templates de prompts legales
└── rag_system.py   # Cadena RAG con MultiQueryRetriever
```

## ¿Cómo funciona?

1. **Ingesta** (`ingest.py`): Lee los contratos PDF de `datos/contratos/`, los divide en chunks y genera un índice FAISS.
2. **RAG** (`rag_system.py`): Recibe una pregunta, genera múltiples variantes con `MultiQueryRetriever`, recupera fragmentos relevantes y genera una respuesta contextualizada.
3. **Interfaz** (`app.py`): Chat Streamlit donde el usuario hace preguntas sobre los contratos y obtiene respuestas con citas del documento.

## Ejecución

```bash
# 1. Indexar los contratos (solo la primera vez)
python nivel_9_proyectos_integradores/asistente_legal/ingest.py

# 2. Lanzar la interfaz de chat
streamlit run nivel_9_proyectos_integradores/asistente_legal/app.py
```

## Requisitos

- `langchain`, `langchain-openai`, `langchain-community`, `faiss-cpu`, `pypdf`, `streamlit`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.
- PDFs de contratos en `datos/contratos/`.

## Tecnologías

- **FAISS** — Índice vectorial para búsqueda semántica.
- **MultiQueryRetriever** — Genera múltiples consultas para ampliar cobertura.
- **Streamlit** — Interfaz web de chat interactiva.
- **LangChain** — Orquestación del pipeline RAG.
