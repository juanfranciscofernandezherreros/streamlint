# config.py
import os

# Rutas
BASE_DIR = "/home/usuario/streamlint"
CONTRATOS_PATH = os.path.join(BASE_DIR, "contratos")
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")

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