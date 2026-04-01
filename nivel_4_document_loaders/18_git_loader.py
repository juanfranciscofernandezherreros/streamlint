"""
18_git_loader.py
----------------
Ejemplo de carga de código fuente desde un repositorio Git con ``GitLoader``.

``GitLoader`` clona (o reutiliza) un repositorio local y carga los archivos
que coincidan con el filtro indicado.  Cada archivo se convierte en un
``Document`` con ``page_content`` igual al contenido del archivo y
``metadata`` con la ruta relativa, el tipo de archivo y el commit actual.

Parámetros clave:
- ``clone_url``:   URL del repositorio remoto a clonar.
- ``repo_path``:   carpeta local donde se almacenará (o ya existe) el repo.
- ``branch``:      rama a cargar (por defecto ``"main"``).
- ``file_filter``: función que devuelve ``True`` para los archivos a incluir.

Dependencia adicional:
    pip install gitpython

Ejecutar:
    python nivel_4_document_loaders/18_git_loader.py
"""

import os
import tempfile
from langchain_community.document_loaders import GitLoader

# Usamos un repositorio público pequeño como ejemplo
CLONE_URL = "https://github.com/langchain-ai/langchain-template-simple.git"

with tempfile.TemporaryDirectory() as tmp_dir:
    repo_path = os.path.join(tmp_dir, "repo")

    loader = GitLoader(
        clone_url=CLONE_URL,
        repo_path=repo_path,
        branch="main",
        # Solo cargamos ficheros Python, Markdown y de texto
        file_filter=lambda path: path.endswith((".py", ".md", ".txt")),
    )

    try:
        docs = loader.load()
        print(f"Archivos cargados del repositorio: {len(docs)}")

        # Análisis por tipo de archivo
        file_types: dict[str, int] = {}
        total_lines = 0

        for doc in docs:
            file_path = doc.metadata.get("source", "")
            ext = file_path.rsplit(".", 1)[-1] if "." in file_path else "sin_ext"
            file_types[ext] = file_types.get(ext, 0) + 1
            lines = doc.page_content.count("\n") + 1
            total_lines += lines

            print(f"  {file_path}  ({lines} líneas)")

        print(f"\nEstadísticas del repositorio:")
        print(f"  Total de líneas: {total_lines:,}")
        print(f"  Tipos de archivo:")
        for ext, count in sorted(file_types.items()):
            print(f"    .{ext}: {count} archivo(s)")

    except Exception as e:
        print(f"Error al cargar el repositorio: {e}")
        print("Asegúrate de tener GitPython instalado: pip install gitpython")
