from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import DocumentCompressorPipeline, LLMChainExtractor
from langchain_community.document_transformers import EmbeddingsRedundantFilter
from langchain_text_splitters import CharacterTextSplitter
import os

# 1. Conectar al vector store existente
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_db = os.path.join(_BASE_DIR, "faiss_db")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vectorstore = FAISS.load_local(
    path_db,
    embeddings,
    allow_dangerous_deserialization=True
)

# 2. Configurar el modelo de lenguaje
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3. ContextualCompressionRetriever básico
# El compresor extrae solo las partes del documento relevantes para la consulta
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 4})
)

# 4. Ejecutar la consulta con compresión básica
consulta = "¿Cuáles son las obligaciones del arrendatario en los contratos?"
print("=== ContextualCompressionRetriever básico ===\n")
compressed_results = compression_retriever.invoke(consulta)

print(f"Se han encontrado {len(compressed_results)} fragmentos comprimidos:\n")
for i, doc in enumerate(compressed_results, start=1):
    print(f"--- Resultado {i} ---")
    print(f"Contenido: {doc.page_content[:400]}...")
    print(f"Metadatos: {doc.metadata}\n")

# 5. Pipeline avanzado de compresión
# Pasos: dividir → filtrar redundantes → comprimir por relevancia
print("=== Pipeline avanzado de compresión ===\n")

splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0, separator=".")
redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
relevant_filter = LLMChainExtractor.from_llm(llm)

pipeline_compressor = DocumentCompressorPipeline(
    transformers=[splitter, redundant_filter, relevant_filter]
)

pipeline_retriever = ContextualCompressionRetriever(
    base_compressor=pipeline_compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 4})
)

pipeline_results = pipeline_retriever.invoke(consulta)

print(f"Pipeline: {len(pipeline_results)} fragmentos tras dividir, filtrar redundantes y comprimir:\n")
for i, doc in enumerate(pipeline_results, start=1):
    print(f"--- Resultado {i} ---")
    print(f"Contenido: {doc.page_content[:400]}...")
    print(f"Metadatos: {doc.metadata}\n")
