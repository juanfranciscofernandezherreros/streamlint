import os as _os

_BASE_DIR = _os.path.dirname(_os.path.abspath(__file__))

CHROMADB_PATH = _os.path.join(_BASE_DIR, "chroma_db")
DOCS_PATH = _os.path.join(_BASE_DIR, "docs")
EMBEDDINGS_MODEL = "text-embedding-3-small"