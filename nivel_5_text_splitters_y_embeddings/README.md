# ⭐⭐⭐⭐ Nivel 5 — Text Splitters y Embeddings: Procesamiento de Texto

Estrategias de **splitting** (división de textos en fragmentos) y generación de **embeddings** semánticos con OpenAI.

## Scripts

| # | Archivo | Descripción |
|---|---------|-------------|
| 20 | `20_text_splitters_parte1.py` | Carga y resumen de un PDF completo con `PyPDFLoader` y LLM. |
| 21 | `21_text_splitters_parte2.py` | División en chunks con `RecursiveCharacterTextSplitter`, resumen progresivo por fragmentos. |
| 22 | `22_embeding_language.py` | Embeddings semánticos con `OpenAIEmbeddings` y cálculo de similitud coseno con NumPy. |

## Conceptos clave

- **`RecursiveCharacterTextSplitter`** — Divide texto en fragmentos solapados respetando separadores naturales.
- **`OpenAIEmbeddings`** — Genera vectores de alta dimensión que representan el significado semántico del texto.
- **Similitud coseno** — Métrica para medir la cercanía semántica entre dos vectores de embeddings.
- **Chunks solapados** — Fragmentos con overlap para no perder contexto en los bordes.

## Ejecución

```bash
python nivel_5_text_splitters_y_embeddings/20_text_splitters_parte1.py
python nivel_5_text_splitters_y_embeddings/21_text_splitters_parte2.py
python nivel_5_text_splitters_y_embeddings/22_embeding_language.py
```

## Requisitos

- `langchain`, `langchain-openai`, `langchain-text-splitters`, `pypdf`, `numpy`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.
- PDF de ejemplo en `datos/cambridge_english_first.pdf` (scripts 20, 21).

## Navegación

⬅️ [Nivel 4 — Document Loaders](../nivel_4_document_loaders/) · ➡️ [Nivel 6 — Retrievers](../nivel_6_retrievers/)
