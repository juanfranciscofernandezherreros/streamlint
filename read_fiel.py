"""
read_fiel.py
------------
Ejemplo de lectura de archivos PDF con ``PyPDFLoader`` de LangChain.

``PyPDFLoader`` divide el PDF en páginas y devuelve una lista de objetos
``Document``.  Cada ``Document`` contiene:
- ``page_content``: texto extraído de la página.
- ``metadata``: información como el número de página y la ruta del archivo.

El ejemplo usa el archivo ``cambridge_english_first.pdf`` incluido en el
repositorio e imprime los primeros 200 caracteres y los metadatos de cada
página.

Ejecutar:
    python read_fiel.py
"""

from langchain_community.document_loaders import PyPDFLoader

ruta_pdf = "cambridge_english_first.pdf"

loader = PyPDFLoader(ruta_pdf)
documents = loader.load()

for i, doc in enumerate(documents):
    print(f"--- Página {i + 1} ---")
    print("Texto:")
    print(doc.page_content[:200])  # solo primeros 200 caracteres

    print("\nMetadatos:")
    print(doc.metadata)
    print("\n")