# ⭐⭐ Nivel 2 — Intermedio: Salida Estructurada

Parseo de salidas de LLM con **OutputParser** y validación con **Pydantic** para obtener respuestas tipadas y estructuradas.

## Scripts

| # | Archivo | Descripción |
|---|---------|-------------|
| 05 | `05_output_parser.py` | Salida estructurada básica con Pydantic y `with_structured_output()`. |
| 06 | `06_analisis_pydantic.py` | Análisis de texto con modelo Pydantic v2 (resumen, sentimiento, palabras clave). |
| 07 | `07_output_parser_parte2.py` | Output parsers avanzados: respuesta tipada en formato JSON. |

## Conceptos clave

- **`with_structured_output()`** — Vincula un LLM a un esquema Pydantic para obtener respuestas tipadas.
- **Modelos Pydantic** — Definen la estructura esperada de la respuesta (campos, tipos, validaciones).
- **OutputParser** — Parseo y validación automática de las salidas del modelo.

## Ejecución

```bash
python nivel_2_intermedio/05_output_parser.py
python nivel_2_intermedio/06_analisis_pydantic.py
python nivel_2_intermedio/07_output_parser_parte2.py
```

## Requisitos

- `langchain`, `langchain-openai`, `pydantic`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.

## Navegación

⬅️ [Nivel 1 — Básico](../nivel_1_basico/) · ➡️ [Nivel 3 — Avanzado](../nivel_3_avanzado/)
