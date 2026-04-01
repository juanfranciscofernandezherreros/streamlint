"""
14_unstructured_html_loader.py
------------------------------
Ejemplo de procesamiento de HTML local con ``UnstructuredHTMLLoader``.

A diferencia de ``WebBaseLoader`` (que descarga HTML de una URL),
``UnstructuredHTMLLoader`` procesa archivos HTML almacenados localmente.

Usando ``mode="elements"`` el loader devuelve un documento por elemento
estructural del HTML (párrafos, títulos, tablas, etc.) e incluye en
``metadata`` el tipo de elemento (``category``).

Estrategias disponibles:
- ``"fast"``:   parseo rápido con lxml/html.parser (sin OCR).
- ``"hi_res"``: análisis de alta resolución (requiere dependencias adicionales).

Dependencias adicionales:
    pip install unstructured

Ejecutar:
    python nivel_4_document_loaders/14_unstructured_html_loader.py
"""

import os
import tempfile
from langchain_community.document_loaders import UnstructuredHTMLLoader

# Creamos un archivo HTML de ejemplo para la demostración
SAMPLE_HTML = """<!DOCTYPE html>
<html lang="es">
<head><title>Reporte de ejemplo</title></head>
<body>
  <h1>Informe Anual 2024</h1>
  <p>Este informe resume los resultados obtenidos durante el ejercicio fiscal 2024.</p>
  <h2>Resultados financieros</h2>
  <p>Los ingresos totales aumentaron un 15 % respecto al año anterior,
     alcanzando los 2,4 millones de euros.</p>
  <h2>Próximos objetivos</h2>
  <p>Para 2025 se prevé expandir la presencia en mercados internacionales
     y lanzar dos nuevas líneas de producto.</p>
</body>
</html>"""

# Guardamos el HTML temporal para poder cargarlo
tmp = tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False)
tmp.write(SAMPLE_HTML)
tmp.close()

try:
    loader = UnstructuredHTMLLoader(
        tmp.name,
        mode="elements",   # un documento por elemento HTML
        strategy="fast",   # parseo rápido sin OCR
    )
    docs = loader.load()

    print(f"Elementos HTML procesados: {len(docs)}")

    # Conteo por tipo de elemento
    element_types: dict[str, int] = {}
    for doc in docs:
        cat = doc.metadata.get("category", "unknown")
        element_types[cat] = element_types.get(cat, 0) + 1

    print("\nTipos de elementos encontrados:")
    for element_type, count in sorted(element_types.items()):
        print(f"  {element_type}: {count}")

    # Elementos de texto más largos
    text_elements = [d for d in docs if d.metadata.get("category") == "NarrativeText"]
    text_elements.sort(key=lambda x: len(x.page_content), reverse=True)

    print(f"\nTop {min(3, len(text_elements))} elementos de texto más largos:")
    for i, element in enumerate(text_elements[:3]):
        print(f"  {i + 1}. {len(element.page_content)} caracteres:")
        print(f"     {element.page_content[:150]}...")

finally:
    os.unlink(tmp.name)
