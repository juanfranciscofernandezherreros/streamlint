from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# 1. Ruta al directorio de contratos (relativa al proyecto)
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_contratos = os.path.join(_BASE_DIR, "datos", "contratos")
loader = PyPDFDirectoryLoader(path_contratos)
documentos = loader.load()

print(f"Se cargaron {len(documentos)} documentos desde el directorio.")

# 2. Dividimos el texto
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000,
    chunk_overlap=1000
)
docs_split = text_splitter.split_documents(documentos)

print(f"Se crearon {len(docs_split)} chunks de texto.")

# 3. Guardamos la base de datos FAISS
persist_db = os.path.join(_BASE_DIR, "faiss_db")

vectorstore = FAISS.from_documents(
    docs_split,
    # RECUERDA: No pegues la clave aquí, usa la variable de entorno que configuramos
    embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
)
vectorstore.save_local(persist_db)

# 4. Ejecutamos la consulta
consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos?"

# Cambié k=2 a k=3 porque tu print de abajo dice "Top 3"
resultados = vectorstore.similarity_search(consulta, k=3)

print("Top 3 documentos más similares a la consulta:\n")
for i, doc in enumerate(resultados, start=1):
    print(f"--- Resultado {i} ---")
    print(f"Contenido: {doc.page_content[:500]}...") # Corto el texto para que no sature la terminal
    print(f"Metadatos: {doc.metadata}\n")