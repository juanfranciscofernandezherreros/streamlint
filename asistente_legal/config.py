from prompt import RAG_TEMPLATE, MULTI_QUERY_PROMPT

EMBEDDING_MODEL = "text-embedding-3-large"
CHROMA_DB_PATH = "/home/usuario/streamlint/asistente_legal/chroma_db"
QUERY_MODEL = "gpt-4o"
GENERATION_MODEL = "gpt-4o"
SEARCH_TYPE = "mmr"
MMR_DIVERSITY_LAMBDA = 0.5
MMR_FETCH_K = 20
SEARCH_K = 2