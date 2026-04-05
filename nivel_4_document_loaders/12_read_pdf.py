"""
12_read_pdf.py
--------------
Ejemplo de lectura de archivos PDF con ``PyPDFLoader`` de LangChain.

``PyPDFLoader`` divide el PDF en páginas y devuelve una lista de objetos
``Document``.  Cada ``Document`` contiene:
- ``page_content``: texto extraído de la página.
- ``metadata``: información como el número de página y la ruta del archivo.

Incluye estadísticas por página (palabras, caracteres) y búsqueda de páginas
que contengan una palabra clave específica.

Ejecutar:
    python nivel_4_document_loaders/12_read_pdf.py
"""

import os
from langchain_community.document_loaders import PyPDFLoader

ruta_pdf = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "datos", "cambridge_english_first.pdf"
)

loader = PyPDFLoader(ruta_pdf)
pages = loader.load_and_split()

print(f"Total de páginas: {len(pages)}")

# Analizar contenido de las primeras 3 páginas
for i, page in enumerate(pages[:3]):
    print(f"\n=== PÁGINA {i + 1} ===")
    print(f"Número de página: {page.metadata['page']}")
    print(f"Archivo fuente: {page.metadata['source']}")
    print(f"Contenido (primeros 200 chars): {page.page_content[:200]}...")

    words = len(page.page_content.split())
    chars = len(page.page_content)
    print(f"Palabras: {words}, Caracteres: {chars}")

# Buscar páginas con contenido específico
keyword = "english"
relevant_pages = [
    page for page in pages if keyword.lower() in page.page_content.lower()
]
print(f"\nPáginas que mencionan '{keyword}': {len(relevant_pages)}")
