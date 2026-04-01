"""
04_message_placeholders.py
--------------------------
Ejemplo de uso de ``MessagesPlaceholder`` para gestionar historial de conversación.

``MessagesPlaceholder`` permite insertar dinámicamente una lista de mensajes
(``HumanMessage``, ``AIMessage``, etc.) en un punto concreto del
``ChatPromptTemplate``.  Esto es fundamental para mantener el contexto de la
conversación sin hardcodear los mensajes previos en la plantilla.

Este módulo simula un historial de dos turnos y añade una nueva pregunta del
usuario, mostrando cómo el prompt queda ensamblado con todos los mensajes.

Ejecutar:
    python nivel_1_basico/04_message_placeholders.py
"""

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil que mantiene el contexto de la conversación."),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "Usuario: {pregunta_actual}")
])

# Simulamos un historial de conversación
historial_conversacion = [
    HumanMessage(content="Usuario: ¿Cuál es la capital de Francia?"),
    AIMessage(content="IA: La capital de Francia es París."),
    HumanMessage(content="Usuario: ¿Y cuántos habitantes tiene?"),
    AIMessage(content="IA: París tiene aproximadamente 2.2 millones de habitantes en la ciudad propiamente dicha.")
]

mensajes = chat_prompt.format_messages(
    historial=historial_conversacion,
    pregunta_actual="¿Puedes decirme algo interesante de su arquitectura?"
)

for m in mensajes:
    print(m.content)