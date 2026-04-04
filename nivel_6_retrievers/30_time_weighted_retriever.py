from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.schema import Document
from datetime import datetime, timedelta

# 1. Crear un vector store en memoria para el retriever con memoria temporal
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = InMemoryVectorStore(embedding=embeddings)

# 2. Configurar el TimeWeightedVectorStoreRetriever
# decay_rate: qué tan rápido "olvida" documentos antiguos (0=nunca olvida, 1=olvida inmediatamente)
# Un decay_rate alto (0.999) hace que los documentos de hace días tengan peso muy bajo
tw_retriever = TimeWeightedVectorStoreRetriever(
    vectorstore=vectorstore,
    decay_rate=0.999,  # Simula memoria que desvanece rápido (útil para pruebas)
    k=3
)

# 3. Agregar documentos con diferentes marcas de tiempo
# Documentos antiguos (simulados con fechas pasadas)
hace_una_semana = datetime.now() - timedelta(days=7)
hace_tres_dias = datetime.now() - timedelta(days=3)
hace_un_dia = datetime.now() - timedelta(days=1)

tw_retriever.add_documents(
    [Document(page_content="Contrato de arrendamiento firmado hace una semana en Madrid.")],
    timestamps=[hace_una_semana]
)

tw_retriever.add_documents(
    [Document(page_content="Contrato de compraventa registrado hace tres días en Barcelona.")],
    timestamps=[hace_tres_dias]
)

tw_retriever.add_documents(
    [Document(page_content="Contrato de arrendamiento de local comercial registrado ayer en Sevilla.")],
    timestamps=[hace_un_dia]
)

# Documento reciente (sin timestamp = ahora mismo, máximo peso)
tw_retriever.add_documents(
    [Document(page_content="Nuevo contrato de compraventa firmado hoy en Valencia, precio actualizado.")]
)

# 4. Ejecutar la consulta
# Los documentos más recientes tendrán mayor puntuación y aparecerán primero
consulta = "contratos inmobiliarios recientes"
print("=== TimeWeightedVectorStoreRetriever ===\n")
print(f"Consulta: '{consulta}'\n")
print("Los documentos más recientes aparecen con mayor prioridad:\n")

resultados = tw_retriever.invoke(consulta)

for i, doc in enumerate(resultados, start=1):
    # La fecha de último acceso se guarda en los metadatos
    last_accessed = doc.metadata.get("last_accessed_at", "N/A")
    print(f"--- Resultado {i} ---")
    print(f"Contenido: {doc.page_content}")
    print(f"Último acceso: {last_accessed}\n")
