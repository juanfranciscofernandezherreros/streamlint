# ============================================================
# Nivel 6 — Script 23b: Base de datos vectorial con Chroma
# ============================================================
# Este script es el complemento de 23_vector_stores.py (que usa FAISS).
# Aquí usamos **Chroma**, otra opción muy popular de vector store, con la
# ventaja de que persiste los datos en disco de forma automática y permite
# añadir nuevos documentos de forma incremental sin reindexar todo.
#
# ¿Qué aprenderás?
#   1. Cómo inicializar una base de datos vectorial con Chroma.
#   2. Cómo convertir texto plano en embeddings y almacenarlos.
#   3. Cómo hacer búsqueda semántica sobre el contenido guardado.
#
# Diferencias clave frente a FAISS (script 23):
#   - Chroma persiste en SQLite automáticamente; no hay que llamar a save_local().
#   - Permite añadir textos en múltiples sesiones sin reemplazar el índice.
#   - La API es la misma que FAISS: add_texts() y similarity_search().
# ============================================================

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# ============================================================
# 1. CARGAR VARIABLES DE ENTORNO
# ============================================================
# Cargamos la clave de OpenAI desde el fichero .env del proyecto.
# Nunca pongas la clave directamente en el código (riesgo de seguridad).
# Crea un fichero .env en la raíz del proyecto con:
#   OPENAI_API_KEY=sk-...
# Puedes copiar .env.example como punto de partida.
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_BASE_DIR, ".env"))

# ============================================================
# 2. CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================
# PERSIST_DIR: carpeta donde Chroma guarda su base de datos SQLite.
#   Se crea automáticamente si no existe.
#   Se coloca en la raíz del proyecto para que sea fácil de localizar.
PERSIST_DIR = os.path.join(_BASE_DIR, "chroma_db")

# COLLECTION_NAME: nombre lógico de la colección dentro de Chroma.
#   Equivale a una "tabla" en una base de datos relacional.
#   Puedes tener varias colecciones en el mismo directorio.
COLLECTION_NAME = "mi_coleccion"


# ============================================================
# 3. INICIALIZAR LA BASE DE DATOS VECTORIAL
# ============================================================
def init_db() -> Chroma:
    """
    Crea o abre la base de datos Chroma en disco.

    - Si PERSIST_DIR ya existe y contiene datos, los carga.
    - Si no existe, crea una base de datos vacía nueva.
    - OpenAIEmbeddings convierte texto en vectores de alta dimensión
      usando el modelo text-embedding-ada-002 de OpenAI.

    Returns:
        Instancia de Chroma lista para usar.
    """
    # OpenAIEmbeddings se conecta a la API de OpenAI para generar los vectores.
    # Cada texto que añadamos se convertirá en un vector numérico que captura
    # su significado semántico.
    embeddings = OpenAIEmbeddings()

    # Chroma abre (o crea) la colección en el directorio indicado.
    # persist_directory garantiza que los datos sobrevivan entre ejecuciones.
    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
    )

    return db


# ============================================================
# 4. AÑADIR DATOS A LA BASE DE DATOS
# ============================================================
def add_data(db: Chroma) -> None:
    """
    Añade textos de ejemplo a la base de datos vectorial.

    - add_texts() convierte cada texto en un embedding y lo almacena.
    - En Chroma moderno (>= 0.4) la persistencia es automática; no es
      necesario llamar a db.persist(), pero lo mantenemos por compatibilidad
      con versiones anteriores.

    Args:
        db: Instancia de Chroma ya inicializada.
    """
    # Textos de ejemplo en español sobre IA y LangChain.
    # En un proyecto real estos vendrían de documentos reales
    # (PDFs, páginas web, etc.) procesados con un Document Loader.
    texts = [
        "Me gusta la inteligencia artificial",
        "LangChain sirve para construir aplicaciones con LLMs",
        "Chroma es una base de datos vectorial",
        "Los embeddings permiten búsqueda semántica",
    ]

    # add_texts() llama a OpenAI una vez por texto para generar el embedding
    # y luego lo inserta en la colección de Chroma.
    db.add_texts(texts)

    print(f"✅ {len(texts)} textos añadidos correctamente en '{PERSIST_DIR}'.")


# ============================================================
# 5. BÚSQUEDA SEMÁNTICA
# ============================================================
def search(db: Chroma, query: str) -> None:
    """
    Realiza una búsqueda semántica en la base de datos.

    similarity_search() convierte la consulta en un embedding y calcula
    la similitud coseno frente a todos los vectores almacenados.
    Devuelve los k documentos más cercanos en el espacio vectorial,
    es decir, los más parecidos en significado, aunque no compartan palabras.

    Args:
        db:    Instancia de Chroma ya inicializada.
        query: Pregunta o texto de búsqueda en lenguaje natural.
    """
    # k=2 → devuelve los 2 resultados más similares.
    # Aumenta k si necesitas más candidatos.
    results = db.similarity_search(query, k=2)

    print(f"\n🔍 Consulta: '{query}'")
    print("─" * 50)
    print("Resultados más similares:\n")
    for i, doc in enumerate(results, start=1):
        print(f"  {i}. {doc.page_content}")
    print()


# ============================================================
# 6. PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    # Paso 1: inicializar (o cargar) la base de datos
    db = init_db()

    # Paso 2: añadir los textos de ejemplo
    add_data(db)

    # Paso 3: hacer una búsqueda semántica
    # La consulta no tiene por qué contener las palabras exactas de los textos;
    # Chroma buscará los documentos más cercanos en significado.
    search(db, "¿Qué es una base de datos vectorial?")
