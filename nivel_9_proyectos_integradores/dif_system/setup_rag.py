import os, shutil
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- CONFIGURACIÓN ---
from config import CHROMADB_PATH as CHROMA_PATH, DOCS_PATH, EMBEDDINGS_MODEL

def build_openai_rag():
    print("🚀 Iniciando proceso con OpenAI...")
    
    # 1. Embeddings de OpenAI
    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
    
    # 2. Cargar todos los PDFs de la carpeta
    loader = DirectoryLoader(DOCS_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    print(f"✅ {len(docs)} páginas cargadas.")

    # 3. Partir el texto en trozos
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # 4. Crear Base de Datos (Limpieza previa)
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    
    vectorstore = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_PATH
    )
    print(f"✨ Base de datos OpenAI lista en: {CHROMA_PATH}")

if __name__ == "__main__":
    build_openai_rag()
