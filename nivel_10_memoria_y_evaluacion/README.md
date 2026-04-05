# ⭐⭐⭐⭐⭐⭐ Nivel 10 — Memoria y Evaluación: Calidad y Persistencia

Gestión de **memoria conversacional** y **evaluación de salidas de LLMs** para garantizar la calidad de las aplicaciones.

## Scripts

| # | Archivo | Descripción |
|---|---------|-------------|
| 41 | `41_conversacion_con_memoria.py` | Tres tipos de memoria conversacional: `ConversationBufferMemory`, `ConversationBufferWindowMemory` y `ConversationSummaryMemory`. |
| 42 | `42_evaluacion_llm.py` | Evaluación de LLMs con `CriteriaEvalChain`, `QAEvalChain` y criterios personalizados. |
| 43 | `43_fundamentos_memoria.py` | Chat básico en terminal sin framework de memoria (prompt + LLM directo). |
| 44 | `44_fundamentos_memoria_langchain.py` | Memoria con `RunnableWithMessageHistory` e `InMemoryChatMessageHistory` de LangChain. |
| 45 | `45_memoria_simple_langgraph.py` | Memoria simple con `MemorySaver` en LangGraph (`StateGraph`). |
| 46 | `46_memoria_ventana_deslizante.py` | Memoria con ventana deslizante usando `trim_messages` en LangGraph. |
| 47 | `47_memoria_persistence_langgraph.py` | Persistencia de memoria en SQLite con `SqliteSaver` en LangGraph. |
| 48 | `48_memoria_vectorial_langgraph.py` | Memoria vectorial avanzada con ChromaDB y embeddings en LangGraph. |

## Conceptos clave

### Memoria conversacional (script 41)

- **`ConversationBufferMemory`** — Guarda todos los turnos de la conversación sin límite.
- **`ConversationBufferWindowMemory`** — Mantiene solo los últimos _k_ turnos (ventana deslizante).
- **`ConversationSummaryMemory`** — Genera un resumen progresivo de la conversación con un LLM.
- **`ConversationChain`** — Cadena que integra un LLM con un wrapper de memoria.

### Evaluación de LLMs (script 42)

- **`CriteriaEvalChain`** — Evalúa respuestas según criterios predefinidos (relevancia, coherencia, etc.).
- **`QAEvalChain`** — Compara la respuesta del LLM con una respuesta de referencia.
- **Criterios personalizados** — Define métricas propias para evaluar calidad, formato o tono.

### Fundamentos de memoria (scripts 43–44)

- **Chat directo** — Bucle de chat sin persistencia de contexto (script 43).
- **`RunnableWithMessageHistory`** — Wrapper de LangChain que añade historial automáticamente (script 44).
- **`InMemoryChatMessageHistory`** — Almacén de mensajes en memoria para sesiones de chat.

### Memoria con LangGraph (scripts 45–48)

- **`MemorySaver`** — Checkpointer en memoria para grafos de estado (script 45).
- **`trim_messages`** — Ventana deslizante que mantiene solo los últimos _k_ mensajes (script 46).
- **`SqliteSaver`** — Persistencia de estado en base de datos SQLite (script 47).
- **Memoria vectorial** — Embeddings + ChromaDB para búsqueda semántica de contexto pasado (script 48).

## Ejecución

```bash
python nivel_10_memoria_y_evaluacion/41_conversacion_con_memoria.py
python nivel_10_memoria_y_evaluacion/42_evaluacion_llm.py
python nivel_10_memoria_y_evaluacion/43_fundamentos_memoria.py
python nivel_10_memoria_y_evaluacion/44_fundamentos_memoria_langchain.py
python nivel_10_memoria_y_evaluacion/45_memoria_simple_langgraph.py
python nivel_10_memoria_y_evaluacion/46_memoria_ventana_deslizante.py
python nivel_10_memoria_y_evaluacion/47_memoria_persistence_langgraph.py
python nivel_10_memoria_y_evaluacion/48_memoria_vectorial_langgraph.py
```

## Requisitos

- `langchain`, `langchain-openai`, `langgraph`, `chromadb`, `langchain-chroma`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.

## Navegación

⬅️ [Nivel 9 — Proyectos Integradores](../nivel_9_proyectos_integradores/)
