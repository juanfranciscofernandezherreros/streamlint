# config.py
import os

# Rutas (relativas al proyecto)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTRATOS_PATH = os.path.join(BASE_DIR, "datos", "contratos")
FAISS_DB_PATH = os.path.join(BASE_DIR, "faiss_db")

# Modelos
EMBEDDING_MODEL = "text-embedding-3-large"
QUERY_MODEL = "gpt-4o-mini"
GENERATION_MODEL = "gpt-4o"

# Prompt
RAG_TEMPLATE = """
Eres un asistente legal experto. Responde a la consulta utilizando exclusivamente el contexto proporcionado. 
Si la información no está en los documentos, indícalo honestamente.

Contexto:
{context}

Pregunta: {question}

Respuesta detallada (cita la fuente y página):
"""