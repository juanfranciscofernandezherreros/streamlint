"""
02_chat_prompt_template.py
--------------------------
Ejemplo básico de ``ChatPromptTemplate`` con LangChain.

Muestra cómo crear una plantilla de chat con un mensaje de sistema fijo y un
mensaje de usuario parametrizado mediante una variable (``{texto}``).  Al
invocar ``format_messages()`` se obtiene una lista de objetos de mensaje
(``SystemMessage``, ``HumanMessage``) listos para enviar a un LLM.

Ejecutar:
    python nivel_1_basico/02_chat_prompt_template.py
"""

from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor del español al inglés muy preciso."),
    ("human", "{texto}")
])

mensajes = chat_prompt.format_messages(texto="Hola mundo, ¿cómo estás?")

for m in mensajes:
    print(f"{type(m)}: {m.content}")