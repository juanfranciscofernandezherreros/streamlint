"""
read_from_website.py
--------------------
Ejemplo de carga de contenido web con ``WebBaseLoader`` de LangChain.

``WebBaseLoader`` descarga y parsea el HTML de una URL, devolviendo una lista
de objetos ``Document`` con el texto extraído y metadatos (URL, título, etc.).
Útil como primer paso en pipelines de RAG (Retrieval-Augmented Generation).

Ejecutar:
    python read_from_website.py
"""

from langchain_community.document_loaders import WebBaseLoader

url = "https://es.wikipedia.org/wiki/Granollers"

loader = WebBaseLoader(url)
documents = loader.load()

print(documents)