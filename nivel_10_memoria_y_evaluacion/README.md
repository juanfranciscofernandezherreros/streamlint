# ⭐⭐⭐⭐⭐⭐ Nivel 10 — Memoria, Evaluación, Streaming y Tool Calling

Gestión de **memoria conversacional**, **evaluación de salidas de LLMs**, **streaming** y **tool calling** para construir aplicaciones de calidad profesional.

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
| 49 | `49_memoria_resumen.py` | Memoria de resumen: condensa conversaciones largas automáticamente. |
| 50 | `50_memoria_filtrado_inteligente.py` | Filtrado inteligente: retiene mensajes importantes por criterios semánticos. |
| 51 | `51_memoria_limite_tokens.py` | Gestión de memoria por límite de tokens: evita superar el contexto del modelo. |
| 52 | `52_memoria_hibrida_tipo_mensaje.py` | Memoria híbrida con retención diferenciada por tipo de mensaje (system/human/AI). |
| 53 | `53_memoria_ventana_adaptativa.py` | Ventana deslizante adaptativa que ajusta su tamaño según el contexto. |
| 54 | `54_memoria_prioridad_contexto.py` | Prioridad de contexto: retiene mensajes por relevancia semántica al turno actual. |
| 55 | `55_streaming_responses.py` | Respuestas en tiempo real con `stream()`, `astream()` y `astream_events()`. |
| 56 | `56_tool_calling.py` | Tool calling: `@tool`, `bind_tools()`, agente ReAct y salida estructurada Pydantic. |

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

### Estrategias avanzadas de memoria (scripts 49–54)

- **Memoria de resumen** — Condensa conversaciones largas en un resumen progresivo (script 49).
- **Filtrado inteligente** — Retiene solo mensajes que superan un umbral de importancia (script 50).
- **Límite de tokens** — Gestiona la ventana de contexto respetando el límite máximo del modelo (script 51).
- **Memoria híbrida** — Políticas diferenciadas por tipo de mensaje: los mensajes del sistema siempre se conservan (script 52).
- **Ventana adaptativa** — Ajusta dinámicamente el número de mensajes según la complejidad del diálogo (script 53).
- **Prioridad de contexto** — Puntúa y retiene mensajes por relevancia semántica al turno actual (script 54).

### Streaming (script 55)

- **`stream()`** — Entrega tokens en cuanto están disponibles (síncrono).
- **`astream()`** — Versión asíncrona con `asyncio`, ideal para APIs web.
- **`astream_events()`** — Eventos tipados: `on_llm_start`, `on_llm_stream`, `on_llm_end`, etc.
- **Streaming en LangGraph** — Modo `stream_mode="updates"` para recibir actualizaciones de estado nodo a nodo.

### Tool calling (script 56)

- **`@tool`** — Decorador que convierte una función Python en herramienta invocable por el modelo.
- **`bind_tools()`** — Vincula herramientas a un `ChatOpenAI` para que las use automáticamente.
- **`ToolNode`** — Nodo LangGraph que ejecuta la herramienta seleccionada por el modelo.
- **`tools_condition`** — Edge condicional: si hay `tool_calls` → ejecutar tools; si no → END.
- **`with_structured_output()`** — Obtiene una respuesta validada con un esquema Pydantic.

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
python nivel_10_memoria_y_evaluacion/49_memoria_resumen.py
python nivel_10_memoria_y_evaluacion/50_memoria_filtrado_inteligente.py
python nivel_10_memoria_y_evaluacion/51_memoria_limite_tokens.py
python nivel_10_memoria_y_evaluacion/52_memoria_hibrida_tipo_mensaje.py
python nivel_10_memoria_y_evaluacion/53_memoria_ventana_adaptativa.py
python nivel_10_memoria_y_evaluacion/54_memoria_prioridad_contexto.py
python nivel_10_memoria_y_evaluacion/55_streaming_responses.py
python nivel_10_memoria_y_evaluacion/56_tool_calling.py
```

## Requisitos

- `langchain`, `langchain-openai`, `langgraph`, `chromadb`, `langchain-chroma`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.

## Navegación

⬅️ [Nivel 9 — Proyectos Integradores](../nivel_9_proyectos_integradores/)
