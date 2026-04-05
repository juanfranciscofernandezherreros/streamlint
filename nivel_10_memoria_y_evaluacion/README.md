# ⭐⭐⭐⭐⭐⭐ Nivel 10 — Memoria y Evaluación: Calidad y Persistencia

Gestión de **memoria conversacional** y **evaluación de salidas de LLMs** para garantizar la calidad de las aplicaciones.

## Scripts

| # | Archivo | Descripción |
|---|---------|-------------|
| 41 | `41_conversacion_con_memoria.py` | Tres tipos de memoria conversacional: `ConversationBufferMemory`, `ConversationBufferWindowMemory` y `ConversationSummaryMemory`. |
| 42 | `42_evaluacion_llm.py` | Evaluación de LLMs con `CriteriaEvalChain`, `QAEvalChain` y criterios personalizados. |

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

## Ejecución

```bash
python nivel_10_memoria_y_evaluacion/41_conversacion_con_memoria.py
python nivel_10_memoria_y_evaluacion/42_evaluacion_llm.py
```

## Requisitos

- `langchain`, `langchain-openai`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.

## Navegación

⬅️ [Nivel 9 — Proyectos Integradores](../nivel_9_proyectos_integradores/)
