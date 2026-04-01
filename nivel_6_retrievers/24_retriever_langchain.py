from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Sustituimos la ruta de C:\ por la de tu usuario en Linux
vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory="/home/usuario/streamlint/chroma_db"
)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos?"
resultados = retriever.invoke(consulta)

print("Top 2 documentos más similares a la consulta:\n")
for i, doc in enumerate(resultados, start=1):
    print(f"--- Resultado {i} ---")
    print(f"Contenido: {doc.page_content}")
    print(f"Metadatos: {doc.metadata}\n")