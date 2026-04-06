from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os

# =========================
# CONFIG
# =========================

os.environ["OPENAI_API_KEY"] = "TU_API_KEY"

PERSIST_DIR = "./vector_db"
COLLECTION_NAME = "mi_coleccion"


# =========================
# INIT VECTOR DB
# =========================

def init_db():
    embeddings = OpenAIEmbeddings()

    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    return db


# =========================
# ADD DATA
# =========================

def add_data(db):
    texts = [
        "Me gusta la inteligencia artificial",
        "LangChain sirve para construir aplicaciones con LLMs",
        "Chroma es una base de datos vectorial",
        "Los embeddings permiten búsqueda semántica"
    ]

    db.add_texts(texts)
    db.persist()

    print("Datos añadidos correctamente.")


# =========================
# SEARCH
# =========================

def search(db, query):
    results = db.similarity_search(query, k=2)

    print("\nResultados:\n")
    for r in results:
        print("-", r.page_content)


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    db = init_db()

    add_data(db)

    search(db, "¿Qué es una base de datos vectorial?")
