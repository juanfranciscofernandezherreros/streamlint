"""
prompt_templates.py
-------------------
Ejemplo básico de ``PromptTemplate`` con LangChain.

``PromptTemplate`` genera prompts de texto plano (no chat) a partir de una
cadena de formato con variables entre llaves.  El método ``format()`` sustituye
las variables y devuelve la cadena final lista para enviar a un modelo.

Este ejemplo define una plantilla para solicitar eslóganes de marketing y la
rellena con el producto "café orgánico".

Ejecutar:
    python nivel_1_basico/01_prompt_templates.py
"""

from langchain_core.prompts import PromptTemplate

template = "Eres un experto en marketing. Sugiere un eslogan creativo para un producto {producto}"

prompt = PromptTemplate(
    template = template,
    input_variables=["producto"]
)

prompt_lleno = prompt.format(producto="café orgánico")
print(prompt_lleno)