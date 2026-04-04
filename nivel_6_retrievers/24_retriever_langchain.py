from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Cargamos la base de datos FAISS desde disco
vectorstore = FAISS.load_local(
    "/home/usuario/streamlint/faiss_db",
    OpenAIEmbeddings(model="text-embedding-3-large"),
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos?"
resultados = retriever.invoke(consulta)

print("Top 2 documentos más similares a la consulta:\n")
for i, doc in enumerate(resultados, start=1):
    print(f"--- Resultado {i} ---")
    print(f"Contenido: {doc.page_content}")
    print(f"Metadatos: {doc.metadata}\n")