# ⭐⭐⭐⭐ Nivel 6 — Retrievers: Recuperación de Información

**9 tipos de retrievers** para búsqueda semántica: vector stores, multi-query, compresión contextual, ensemble, parent document, self-query, time-weighted y MMR.

## Scripts

| # | Archivo | Descripción | Retriever |
|---|---------|-------------|-----------|
| 23 | `23_vector_stores.py` | Creación de índice FAISS a partir de PDFs de contratos | `FAISS` |
| 24 | `24_retriever_langchain.py` | Retriever básico sobre FAISS | `VectorStoreRetriever` |
| 25 | `25_multi_query_retriever.py` | Genera múltiples consultas para mejorar la cobertura | `MultiQueryRetriever` |
| 26 | `26_contextual_compression_retriever.py` | Comprime y filtra documentos con LLM | `ContextualCompressionRetriever` |
| 27 | `27_ensemble_retriever.py` | Combina FAISS (semántico) + BM25 (léxico) | `EnsembleRetriever` |
| 28 | `28_parent_document_retriever.py` | Busca en chunks hijos, retorna documentos padre completos | `ParentDocumentRetriever` |
| 29 | `29_self_query_retriever.py` | Genera filtros de metadatos automáticamente desde lenguaje natural | `SelfQueryRetriever` |
| 30 | `30_time_weighted_retriever.py` | Prioriza documentos recientes con decaimiento temporal | `TimeWeightedVectorStoreRetriever` |
| 31 | `31_advanced_retrievers.py` | Retrievers avanzados: MMR, filtros por score y combinaciones | Varios |

## Conceptos clave

- **FAISS** — Índice vectorial local para búsqueda por similitud eficiente.
- **BM25** — Algoritmo de búsqueda léxica basado en frecuencia de términos.
- **EnsembleRetriever** — Combina múltiples retrievers con pesos configurables.
- **MMR (Maximal Marginal Relevance)** — Equilibra relevancia y diversidad en los resultados.

## ⚠️ Orden de ejecución

El script `23_vector_stores.py` **debe ejecutarse primero** para crear el índice FAISS en `faiss_db/`. Los scripts 24–26 y 31 dependen de este índice.

```bash
# 1. Crear el índice FAISS (requiere datos/contratos/)
python nivel_6_retrievers/23_vector_stores.py

# 2. Usar los retrievers
python nivel_6_retrievers/24_retriever_langchain.py
python nivel_6_retrievers/25_multi_query_retriever.py
python nivel_6_retrievers/26_contextual_compression_retriever.py
python nivel_6_retrievers/27_ensemble_retriever.py
python nivel_6_retrievers/28_parent_document_retriever.py
python nivel_6_retrievers/29_self_query_retriever.py
python nivel_6_retrievers/30_time_weighted_retriever.py
python nivel_6_retrievers/31_advanced_retrievers.py
```

## Requisitos

- `langchain`, `langchain-openai`, `langchain-community`, `faiss-cpu`, `rank_bm25`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.
- PDFs de contratos en `datos/contratos/`.

## Navegación

⬅️ [Nivel 5 — Text Splitters y Embeddings](../nivel_5_text_splitters_y_embeddings/) · ➡️ [Nivel 7 — LangGraph](../nivel_7_langgraph/)
