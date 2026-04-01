"""
rol_prompt_tempaltes.py
-----------------------
Ejemplo de plantillas de prompt con rol dinámico usando LangChain.

Combina ``SystemMessagePromptTemplate`` y ``HumanMessagePromptTemplate``
dentro de un ``ChatPromptTemplate`` para crear asistentes con identidad y
especialización configurables en tiempo de ejecución mediante las variables:

- ``rol``: tipo de experto (p.ej. "nutricionista").
- ``especialidad``: área de conocimiento (p.ej. "dietas veganas").
- ``tono``: estilo de comunicación (p.ej. "profesional pero accesible").
- ``tema``: asunto de la pregunta.
- ``pregunta``: texto concreto del usuario.

Ejecutar:
    python rol_prompt_tempaltes.py
"""

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

plantilla_sistema = SystemMessagePromptTemplate.from_template(
    "Eres un {rol} especializado en {especialidad}. Responde de manera {tono}"
)

plantilla_humano = HumanMessagePromptTemplate.from_template(
    "Mi pregunta sobre {tema} es: {pregunta}"
)

chat_prompt = ChatPromptTemplate.from_messages([
    plantilla_sistema,
    plantilla_humano
])

mensajes = chat_prompt.format_messages(
    rol="nutricionista",
    especialidad="dietas veganas",
    tono="profesional pero accesible",
    tema="proteínas vegetales",
    pregunta="¿Cuáles son las mejores fuentes de proteína vegana para un atleta profesional?"
)

for m in mensajes:
    print(m.content)