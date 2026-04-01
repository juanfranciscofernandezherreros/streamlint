"""
17_selenium_url_loader.py
-------------------------
Ejemplo de carga de páginas con JavaScript con ``SeleniumURLLoader``.

A diferencia de ``WebBaseLoader``, ``SeleniumURLLoader`` renderiza la página
con un navegador real (Chrome o Firefox), lo que permite extraer contenido
generado dinámicamente por JavaScript (SPAs, dashboards interactivos, etc.).

Requisitos:
- Google Chrome (o Firefox) instalado en el sistema.
- ChromeDriver (o GeckoDriver) accesible en el PATH o indicado en
  ``executable_path``.

Instalación:
    pip install selenium

Ejecutar:
    python nivel_4_document_loaders/17_selenium_url_loader.py
"""

from langchain_community.document_loaders import SeleniumURLLoader

# URLs con contenido renderizado por JavaScript
urls = [
    "https://example.com",
]

loader = SeleniumURLLoader(
    urls=urls,
    browser="chrome",
    headless=True,          # Sin interfaz gráfica (modo servidor)
    arguments=["--no-sandbox", "--disable-dev-shm-usage"],
)

try:
    docs = loader.load()

    print(f"Páginas procesadas: {len(docs)}")

    for i, doc in enumerate(docs):
        print(f"\n=== PÁGINA {i + 1} ===")
        print(f"URL:      {doc.metadata['source']}")
        print(f"Título:   {doc.metadata.get('title', 'Sin título')}")
        print(f"Longitud: {len(doc.page_content)} caracteres")

        # Indicadores de contenido dinámico
        dynamic_indicators = ["data-", "ng-", "v-", "react-", "vue-"]
        has_dynamic = any(ind in doc.page_content for ind in dynamic_indicators)
        print(f"Elementos dinámicos detectados: {'Sí' if has_dynamic else 'No'}")

        print(f"Vista previa: {doc.page_content[:200]}...")

except Exception as e:
    print(f"Error: {e}")
    print(
        "Asegúrate de tener Chrome y ChromeDriver instalados y accesibles en el PATH."
    )
