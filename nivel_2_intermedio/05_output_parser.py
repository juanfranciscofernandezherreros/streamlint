"""
05_output_parser.py
-------------------
Ejemplo básico de salida estructurada con Pydantic y LangChain.

Define un modelo Pydantic (``AnalisisTexto``) con dos campos tipados —
``resumen`` y ``sentimiento`` — y usa ``llm.with_structured_output()`` para que
el LLM devuelva directamente una instancia validada del modelo en lugar de
texto libre.

Requiere la variable de entorno ``OPENAI_API_KEY`` configurada.

Ejecutar:
    python nivel_2_intermedio/05_output_parser.py
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