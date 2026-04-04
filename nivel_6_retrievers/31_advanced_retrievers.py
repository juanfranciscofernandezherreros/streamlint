from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 1. Conectar al vector store existente
path_db = "/home/usuario/streamlint/faiss_db"
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vectorstore = FAISS.load_local(
    path_db,
    embeddings,
    allow_dangerous_deserialization=True
)

consulta = "¿Cuáles son las cláusulas de rescisión en los contratos de arrendamiento?"

# 2. MMR (Maximum Marginal Relevance)
# Balancea relevancia con diversidad para evitar resultados repetitivos
print("=== MMR (Maximum Marginal Relevance) ===\n")
mmr_retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "lambda_mult": 0.7  # 1.0 = máxima relevancia, 0.0 = máxima diversidad
    }
)

mmr_results = mmr_retriever.invoke(consulta)
print(f"Resultados MMR (relevancia + diversidad): {len(mmr_results)}\n")
for i, doc in enumerate(mmr_results, start=1):
    print(f"--- Resultado {i} ---")
    print(f"Contenido: {doc.page_content[:400]}...")
    print(f"Metadatos: {doc.metadata}\n")

# 3. Retrieval con Reranking usando CohereRerank (requiere COHERE_API_KEY)
# Descomenta este bloque si tienes una API Key de Cohere configurada
#
# from langchain.retrievers import ContextualCompressionRetriever
# from langchain_cohere import CohereRerank
# import os
#
# # Primer pase: recuperar muchos candidatos con similitud semántica
# base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})
#
# # Segundo pase: reordenar los candidatos con el modelo de Cohere
# reranker = CohereRerank(
#     model="rerank-multilingual-v2.0",
#     top_n=5,
#     cohere_api_key=os.environ.get("COHERE_API_KEY")
# )
#
# rerank_retriever = ContextualCompressionRetriever(
#     base_compressor=reranker,
#     base_retriever=base_retriever
# )
#
# rerank_results = rerank_retriever.invoke(consulta)
# print(f"=== Retrieval con Reranking (Cohere) ===\n")
# print(f"Resultados tras reranking: {len(rerank_results)}\n")
# for i, doc in enumerate(rerank_results, start=1):
#     print(f"--- Resultado {i} ---")
#     print(f"Contenido: {doc.page_content[:400]}...")
#     print(f"Metadatos: {doc.metadata}\n")

# 4. Comparación de búsqueda por similitud estándar vs MMR
print("=== Comparación: Similitud estándar vs MMR ===\n")

similarity_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
similarity_results = similarity_retriever.invoke(consulta)

print(f"Similitud estándar ({len(similarity_results)} resultados):")
for doc in similarity_results:
    print(f"  - {doc.page_content[:150]}...")

print(f"\nMMR ({len(mmr_results)} resultados, mayor diversidad):")
for doc in mmr_results:
    print(f"  - {doc.page_content[:150]}...")
