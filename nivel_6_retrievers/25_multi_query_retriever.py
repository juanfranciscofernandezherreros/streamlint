from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
import os

# 1. Ajustamos la ruta al directorio de la base de datos en Linux
# Usamos la dirección que confirmamos antes en tu terminal
path_db = "/home/usuario/streamlint/chroma_db"

vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory=path_db
)

# 2. Configuramos el modelo de lenguaje (LLM)
# gpt-4o-mini es ideal para tu portátil porque responde rápido
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3. Configuramos el sistema de recuperación (Retriever)
base_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

# El MultiQueryRetriever generará 3 variaciones de tu pregunta para buscar mejor
retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)

# 4. Ejecutamos la consulta
consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos?"
resultados = retriever.invoke(consulta)

print(f"Se han encontrado {len(resultados)} fragmentos relevantes:\n")

for i, doc in enumerate(resultados, start=1):
    print(f"--- Resultado {i} ---")
    print(f"Contenido: {doc.page_content[:400]}...") # Limitamos salida para no saturar la terminal
    print(f"Metadatos: {doc.metadata}\n")