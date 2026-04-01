"""
analisis_pydantic.py
--------------------
Análisis estructurado de texto con LangChain y Pydantic v2.

Define el modelo ``AnalisisTexto`` con tres campos:
- ``resumen``: resumen breve del texto analizado.
- ``sentimiento``: clasificación (Positivo, Neutro, Negativo).
- ``palabras_clave``: lista de 3–5 palabras clave extraídas.

La cadena LCEL ``prompt | structured_llm`` envía el texto al modelo y devuelve
directamente una instancia validada de ``AnalisisTexto``, eliminando la
necesidad de parseo manual.

Requiere la variable de entorno ``OPENAI_API_KEY`` configurada.

Ejecutar:
    python analisis_pydantic.py
"""

from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Modelo de datos (Pydantic v2)
class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto")
    sentimiento: str = Field(description="Sentimiento: Positivo, Neutro o Negativo")
    palabras_clave: List[str] = Field(description="3-5 palabras clave principales")

# 2. Inicializar el LLM con Salida Estructurada
# Esto reemplaza al Parser y al PromptTemplate complejo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(AnalisisTexto)

# 3. Prompt simplificado
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto analista de textos. Extrae la información solicitada de forma precisa."),
    ("human", "{texto}")
])

# 4. Cadena (Chain)
# Ahora es mucho más directa
chain = prompt | structured_llm

# 5. Ejecución
if __name__ == "__main__":
    texto_ejemplo = "Me encantó la nueva película de acción, tiene efectos especiales increíbles."
    
    try:
        # La respuesta ya es un objeto AnalisisTexto, no hace falta parsear manualmente
        resultado = chain.invoke({"texto": texto_ejemplo})
        
        print("✅ Análisis exitoso:")
        print(resultado.model_dump_json(indent=2))
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")