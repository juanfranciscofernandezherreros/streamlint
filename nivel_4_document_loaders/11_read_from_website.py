"""
11_read_from_website.py
-----------------------
Ejemplo de carga de contenido web con ``WebBaseLoader`` de LangChain.

``WebBaseLoader`` descarga y parsea el HTML de una URL, devolviendo una lista
de objetos ``Document`` con el texto extraído y metadatos (URL, título, etc.).
Útil como primer paso en pipelines de RAG (Retrieval-Augmented Generation).

Incluye un ejemplo básico (una URL) y uno avanzado (múltiples URLs con filtrado
de elementos HTML mediante BeautifulSoup).

Ejecutar:
    python nivel_4_document_loaders/11_read_from_website.py
"""

import bs4
from langchain_community.document_loaders import WebBaseLoader

# ── Ejemplo básico: una sola URL ─────────────────────────────────────────────
print("=== Ejemplo básico ===")
loader = WebBaseLoader("https://es.wikipedia.org/wiki/Granollers")
docs = loader.load()

print(f"Título: {docs[0].metadata.get('title', 'Sin título')}")
print(f"URL: {docs[0].metadata['source']}")
print(f"Contenido (primeros 300 chars): {docs[0].page_content[:300]}...")

# ── Ejemplo avanzado: múltiples URLs con filtrado de elementos HTML ───────────
print("\n=== Ejemplo avanzado (múltiples URLs) ===")
urls = [
    "https://python.langchain.com/docs/concepts/",
    "https://python.langchain.com/docs/tutorials/",
    "https://python.langchain.com/docs/how_to/",
]

loader = WebBaseLoader(
    web_paths=urls,
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer("article")  # solo el contenido principal
    ),
)
docs = loader.load()

print(f"Páginas cargadas: {len(docs)}")
for i, doc in enumerate(docs):
    print(f"  Página {i + 1}: {doc.metadata['source']}")
    print(f"  Longitud: {len(doc.page_content)} caracteres")
