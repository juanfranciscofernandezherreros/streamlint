"""
21_text_splitters_parte2.py
---------------------------
Ejemplo de carga, división en chunks y resumen progresivo de un PDF con LangChain.

Carga un PDF con ``PyPDFLoader``, divide el texto en fragmentos solapados
con ``RecursiveCharacterTextSplitter`` y resume cada chunk por separado.
Finalmente combina todos los resúmenes en uno coherente.

Requiere la variable de entorno ``OPENAI_API_KEY`` configurada.

Ejecutar:
    python nivel_5_text_splitters_y_embeddings/21_text_splitters_parte2.py
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Cargar el documento PDF
ruta_pdf = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "cambridge_english_first.pdf"
)
loader = PyPDFLoader(ruta_pdf)
pages = loader.load()

# Dividir el texto en chunks más pequeños
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=10000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(pages)

# 3. Pasar el texto al LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
summaries = []

i = 0
for chunk in chunks:
    if i > 10:
        break
    response = llm.invoke(f"Haz un resumen de los puntos más importantes del siguiente texto: {chunk.page_content}")
    summaries.append(response.content)
    i += 1

print(summaries)

final_summary = llm.invoke(f"Combina y sintetiza estos resumenes en un resumen coherente y completo: {" ".join(summaries)}")
print(final_summary.content)
