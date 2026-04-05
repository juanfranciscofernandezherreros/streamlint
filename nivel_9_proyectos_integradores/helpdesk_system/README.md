# HelpDesk System — Sistema de Soporte Técnico

Sistema de **soporte técnico inteligente** con **LangGraph** que gestiona tickets, clasifica consultas y responde usando RAG sobre documentación interna.

## Estructura

```text
helpdesk_system/
├── app.py          # Interfaz principal Streamlit
├── config.py       # Configuración del sistema
├── graph.py        # Grafo LangGraph para workflow de soporte
├── rag_system.py   # Sistema RAG sobre documentación interna
├── setup_rag.py    # Indexación de la documentación
└── docs/           # Documentación interna de soporte
    ├── faq.md                          # Preguntas frecuentes
    ├── guia_resolucion_problemas.md    # Guía de resolución
    └── manual_usuario.md              # Manual de usuario
```

## ¿Cómo funciona?

1. **Indexación** (`setup_rag.py`): Lee la documentación interna (FAQ, manual, guía), genera embeddings y crea un índice vectorial.
2. **Grafo de soporte** (`graph.py`): LangGraph define un workflow con nodos para:
   - Clasificar el tipo de consulta (técnica, administrativa, etc.).
   - Enrutar al departamento o base de conocimiento correcta.
   - Generar una respuesta usando RAG.
3. **RAG** (`rag_system.py`): Recupera fragmentos relevantes de la documentación y genera respuestas contextualizadas.
4. **Interfaz** (`app.py`): Chat Streamlit donde el usuario hace consultas de soporte.

## Ejecución

```bash
# 1. Indexar la documentación (solo la primera vez)
python nivel_9_proyectos_integradores/helpdesk_system/setup_rag.py

# 2. Lanzar la interfaz de soporte
streamlit run nivel_9_proyectos_integradores/helpdesk_system/app.py
```

## Requisitos

- `langchain`, `langchain-openai`, `langchain-community`, `langgraph`, `faiss-cpu`, `streamlit`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.

## Tecnologías

- **LangGraph** — Workflow de soporte con grafos de estado y routing condicional.
- **FAISS** — Índice vectorial para búsqueda semántica sobre documentación.
- **Streamlit** — Interfaz web de chat para soporte.
- **LangChain** — Orquestación del pipeline RAG.
