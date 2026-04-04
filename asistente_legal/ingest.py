# ingest.py
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import config

def main():
    print(f"🚀 Iniciando ingesta desde: {config.CONTRATOS_PATH}")
    
    if not os.path.exists(config.CONTRATOS_PATH):
        print(f"❌ Error: La carpeta {config.CONTRATOS_PATH} no existe.")
        return

    # 1. Cargar PDFs
    loader = DirectoryLoader(config.CONTRATOS_PATH, glob="./*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    print(f"📄 Documentos cargados: {len(docs)}")
    # 2. Partir en fragmentos
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    print(f"✂️ Fragmentos creados: {len(chunks)}")

    # 3. Guardar en Chroma
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(model=config.EMBEDDING_MODEL),
        persist_directory=config.CHROMA_DB_PATH
    )
    print(f"✅ Base de datos guardada en: {config.CHROMA_DB_PATH}")

if __name__ == "__main__":
    main()