"""
12_directory_loader.py
----------------------
Ejemplo de carga masiva de archivos con ``DirectoryLoader`` de LangChain.

``DirectoryLoader`` recorre una carpeta de forma recursiva y carga todos los
archivos que coincidan con un patrón glob.  Cada archivo se procesa con el
``loader_cls`` indicado (en este caso ``UnstructuredMarkdownLoader``).

Opciones destacadas:
- ``glob``: patrón de archivos a incluir (p.ej. ``"**/*.md"``).
- ``recursive``: busca en subdirectorios de forma recursiva.
- ``show_progress``: muestra una barra de progreso en la consola.
- ``use_multithreading``: carga archivos en paralelo para mayor velocidad.

Ejecutar:
    python nivel_4_document_loaders/12_directory_loader.py
"""

import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader

# Carpeta a procesar: en este ejemplo usamos la raíz del proyecto
# donde existen archivos .md (README.md).
carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

loader = DirectoryLoader(
    carpeta,
    glob="**/*.md",
    loader_cls=UnstructuredMarkdownLoader,
    recursive=True,
    show_progress=True,
    use_multithreading=True,
)

docs = loader.load()
print(f"Documentos cargados: {len(docs)}")

# Estadísticas del contenido cargado
total_chars = sum(len(doc.page_content) for doc in docs)

file_stats = {}
for doc in docs:
    filename = os.path.basename(doc.metadata["source"])
    file_stats[filename] = {
        "chars": len(doc.page_content),
        "words": len(doc.page_content.split()),
        "lines": doc.page_content.count("\n") + 1,
    }

print(f"\nTotal de caracteres procesados: {total_chars:,}")
print("\nArchivos cargados (ordenados por longitud):")
sorted_files = sorted(file_stats.items(), key=lambda x: x[1]["chars"], reverse=True)
for filename, stats in sorted_files:
    print(f"  {filename}: {stats['chars']:,} chars | {stats['words']:,} palabras")
