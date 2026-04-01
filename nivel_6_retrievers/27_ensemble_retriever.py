from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Cargar documentos
path_contratos = "/home/usuario/streamlint/contratos"
loader = PyPDFDirectoryLoader(path_contratos)
documentos = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs_split = text_splitter.split_documents(documentos)

print(f"Se cargaron {len(docs_split)} chunks de texto.\n")

# 2. Crear retriever BM25 (búsqueda por palabras clave)
bm25_retriever = BM25Retriever.from_documents(docs_split)
bm25_retriever.k = 5

# 3. Crear retriever vectorial con FAISS (búsqueda semántica)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = FAISS.from_documents(docs_split, embeddings)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# 4. EnsembleRetriever: combina BM25 y vector search con Fusión de Ranking Recíproco
# Pesos: 30% BM25 (palabras clave) + 70% vectorial (semántica)
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7]
)

# 5. Ejecutar la consulta
consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos?"
print("=== EnsembleRetriever (BM25 + Vector Search) ===\n")
resultados = ensemble_retriever.invoke(consulta)

print(f"Se han encontrado {len(resultados)} fragmentos relevantes:\n")
for i, doc in enumerate(resultados, start=1):
    print(f"--- Resultado {i} ---")
    print(f"Contenido: {doc.page_content[:400]}...")
    print(f"Metadatos: {doc.metadata}\n")
