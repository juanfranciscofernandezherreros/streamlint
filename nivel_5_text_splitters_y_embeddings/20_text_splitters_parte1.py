"""
20_text_splitters_parte1.py
---------------------------
Ejemplo básico de carga y resumen de un PDF completo con LangChain.

Carga todas las páginas de un PDF con ``PyPDFLoader``, combina el texto y
lo envía al LLM para obtener un resumen global del documento.

Requiere la variable de entorno ``OPENAI_API_KEY`` configurada.

Ejecutar:
    python nivel_5_text_splitters_y_embeddings/20_text_splitters_parte1.py
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI

# 1. Cargar el documento PDF
ruta_pdf = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "cambridge_english_first.pdf"
)
loader = PyPDFLoader(ruta_pdf)
pages = loader.load()

# 2. Combinar todas las páginas en un texto único
full_text = ""
for page in pages:
    full_text += page.page_content + "\n"

# 3. Pasar el texto al LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
response = llm.invoke(f"Haz un resumen de los puntos más importantes del siguiente documento: {full_text}")

print(response)
