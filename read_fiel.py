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