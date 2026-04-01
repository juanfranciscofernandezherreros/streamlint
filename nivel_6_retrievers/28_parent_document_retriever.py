from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

# 1. Cargar documentos
path_contratos = "/home/usuario/streamlint/contratos"
loader = PyPDFDirectoryLoader(path_contratos)
documentos = loader.load()

print(f"Se cargaron {len(documentos)} documentos desde el directorio.\n")

# 2. Definir los splitters
# Splitter para documentos padre: chunks grandes con contexto amplio
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

# Splitter para documentos hijo: chunks pequeños para embeddings más precisos
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

# 3. Vector store para los chunks pequeños (hijos)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = Chroma(
    collection_name="parent_document_retriever",
    embedding_function=embeddings
)

# 4. Almacenamiento en memoria para los documentos padre
store = InMemoryStore()

# 5. Configurar el ParentDocumentRetriever
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

# 6. Indexar los documentos (crea chunks hijo para búsqueda y guarda padres)
retriever.add_documents(documentos)

# Verificar cuántos chunks hijo se indexaron
num_hijos = len(vectorstore.get()["ids"])
print(f"Chunks hijo indexados en el vector store: {num_hijos}")
print(f"Documentos padre en el almacenamiento: {len(list(store.yield_keys()))}\n")

# 7. Ejecutar la consulta
# El retriever busca en los chunks pequeños pero devuelve los documentos padre completos
consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos?"
print("=== ParentDocumentRetriever ===\n")
resultados = retriever.invoke(consulta)

print(f"Se han encontrado {len(resultados)} documentos padre relevantes:\n")
for i, doc in enumerate(resultados, start=1):
    print(f"--- Resultado {i} ---")
    print(f"Longitud del contenido: {len(doc.page_content)} caracteres")
    print(f"Contenido (primeros 500 chars): {doc.page_content[:500]}...")
    print(f"Metadatos: {doc.metadata}\n")
