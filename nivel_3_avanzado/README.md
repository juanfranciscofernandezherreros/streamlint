# ⭐⭐⭐ Nivel 3 — Avanzado: Ejecución Paralela

Ejecución paralela y procesamiento por lotes con **RunnableParallel** y **batch**, incluyendo un pipeline completo de análisis de sentimientos.

## Scripts

| # | Archivo | Descripción |
|---|---------|-------------|
| 08 | `08_analisis_sentimientos.py` | Pipeline de análisis de sentimientos con preprocesador, ejecución paralela y postprocesador. |
| 09 | `09_paralelo.py` | Ejecución paralela con `RunnableParallel`: tres cadenas LCEL ejecutándose simultáneamente. |
| 10 | `10_paralelo_batch.py` | Procesamiento por lotes con `.batch()` y control de concurrencia (`max_concurrency`). |

## Conceptos clave

- **`RunnableParallel`** — Ejecuta múltiples cadenas LCEL en paralelo sobre la misma entrada.
- **`RunnableLambda`** — Convierte funciones Python en nodos de una cadena LCEL.
- **`.batch()`** — Procesa múltiples entradas simultáneamente con control de concurrencia.
- **Pipeline de análisis** — Combinación de preprocesamiento, análisis paralelo y postprocesamiento.

## Ejecución

```bash
python nivel_3_avanzado/08_analisis_sentimientos.py
python nivel_3_avanzado/09_paralelo.py
python nivel_3_avanzado/10_paralelo_batch.py
```

## Requisitos

- `langchain`, `langchain-openai`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.

## Navegación

⬅️ [Nivel 2 — Intermedio](../nivel_2_intermedio/) · ➡️ [Nivel 4 — Document Loaders](../nivel_4_document_loaders/)
