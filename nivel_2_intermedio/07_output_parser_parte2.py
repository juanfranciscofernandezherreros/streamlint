"""
07_output_parser_parte2.py
--------------------------
Ejemplo de salida estructurada con Pydantic y ``with_structured_output()``.

Define un modelo Pydantic con dos campos (resumen y sentimiento), vincula
el LLM a ese esquema y analiza un texto de prueba obteniendo una respuesta
tipada en formato JSON.

Requiere la variable de entorno ``OPENAI_API_KEY`` configurada.

Ejecutar:
    python nivel_2_intermedio/07_output_parser_parte2.py
"""

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto.")
    sentimiento: str = Field(description="Sentimiento del texto (Positivo, neutro o negativo)")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)

structured_llm = llm.with_structured_output(AnalisisTexto)

texto_prueba = "Me encantó la nueva película de acción, tiene muchos efectos especiales y emoción."

resultado = structured_llm.invoke(f"Analiza el siguiente texto: {texto_prueba}")

print(resultado.model_dump_json())
