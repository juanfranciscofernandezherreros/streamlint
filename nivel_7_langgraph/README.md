# ⭐⭐⭐⭐⭐ Nivel 7 — LangGraph: Grafos de Estado

Diseño de workflows complejos con **LangGraph**: grafos de estado, nodos condicionales, procesamiento de reuniones y persistencia con checkpointers.

## Scripts

| # | Archivo | Descripción |
|---|---------|-------------|
| 32 | `32_primer_programa_langgraph.py` | Primer grafo de estado (`StateGraph`) con nodos secuenciales. |
| 33 | `33_procesador_reuniones.py` | Workflow completo: transcripción Whisper → extracción de participantes/temas/acciones → minutas. |
| 34 | `34_control_flujo_langgraph.py` | Control de flujo condicional con `StateGraph`. |
| 35 | `35_procesador_reuniones_langgraph.py` | Procesador de reuniones con interfaz gráfica (tkinter) para selección de archivo. |
| 36 | `36_langgraph_condicional.py` | Edges condicionales avanzados: clasificación de sentimiento con routing a ramas especializadas. |
| 37 | `37_langgraph_checkpointer.py` | Persistencia de estado con `MemorySaver`. Conversación multi-turno con memoria entre invocaciones. |

## Conceptos clave

- **`StateGraph`** — Grafo dirigido donde cada nodo transforma un estado tipado (`TypedDict`).
- **`START` / `END`** — Nodos especiales que marcan el inicio y fin del grafo.
- **Edges condicionales** — Routing dinámico basado en el estado (ej: sentimiento → rama positiva/negativa/neutra).
- **`MemorySaver`** — Checkpointer en RAM para persistir el estado entre invocaciones.
- **Whisper API** — Transcripción de audio/vídeo (usado en scripts 33, 35).

## Ejecución

```bash
python nivel_7_langgraph/32_primer_programa_langgraph.py
python nivel_7_langgraph/33_procesador_reuniones.py          # Requiere datos/Simulacion_reunion.mp4
python nivel_7_langgraph/34_control_flujo_langgraph.py
python nivel_7_langgraph/35_procesador_reuniones_langgraph.py # Requiere tkinter (interfaz gráfica)
python nivel_7_langgraph/36_langgraph_condicional.py
python nivel_7_langgraph/37_langgraph_checkpointer.py
```

## Requisitos

- `langchain`, `langchain-openai`, `langgraph`, `openai`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.
- Scripts 33, 35: archivo de vídeo/audio (ej: `datos/Simulacion_reunion.mp4`).
- Script 35: entorno gráfico con `tkinter` disponible.

## Navegación

⬅️ [Nivel 6 — Retrievers](../nivel_6_retrievers/) · ➡️ [Nivel 8 — Aplicaciones](../nivel_8_aplicaciones/)
