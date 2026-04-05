"""
38_conversacion_con_memoria.py
------------------------------
Tipos de memoria conversacional en LangChain.

LangChain ofrece distintas estrategias para gestionar el historial de una
conversación.  Este módulo ilustra tres de ellas usando ``ConversationChain``
y los wrappers de memoria más habituales:

1. **ConversationBufferMemory** — guarda todos los turnos sin límite.
2. **ConversationBufferWindowMemory** — ventana deslizante de *k* turnos.
3. **ConversationSummaryMemory** — resume el historial con el LLM para ahorrar
   tokens en conversaciones largas.

Ejecutar:
    python nivel_10_memoria_y_evaluacion/38_conversacion_con_memoria.py
"""

from langchain_openai import ChatOpenAI
from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory,
)
from langchain.chains import ConversationChain

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Turnos de ejemplo para probar los tres tipos de memoria
TURNOS = [
    "Hola, me llamo Andrés y soy programador Python.",
    "¿Cuáles son las ventajas de usar LangChain?",
    "¿Recuerdas mi nombre y mi profesión?",
    "Muy bien. ¿Qué framework de grafos aprendí en el nivel 7?",
]


def demo_buffer_memory() -> None:
    """Conserva TODO el historial de la conversación."""
    print("\n" + "=" * 60)
    print("1) ConversationBufferMemory (historial completo)")
    print("=" * 60)

    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=llm, memory=memory, verbose=False)

    for turno in TURNOS:
        respuesta = chain.predict(input=turno)
        print(f"Usuario  : {turno}")
        print(f"Asistente: {respuesta}\n")


def demo_window_memory(k: int = 2) -> None:
    """Conserva solo los últimos *k* intercambios (ventana deslizante)."""
    print("\n" + "=" * 60)
    print(f"2) ConversationBufferWindowMemory (ventana k={k})")
    print("=" * 60)

    memory = ConversationBufferWindowMemory(k=k)
    chain = ConversationChain(llm=llm, memory=memory, verbose=False)

    for turno in TURNOS:
        respuesta = chain.predict(input=turno)
        print(f"Usuario  : {turno}")
        print(f"Asistente: {respuesta}\n")


def demo_summary_memory() -> None:
    """Resume el historial con el LLM para minimizar el uso de tokens."""
    print("\n" + "=" * 60)
    print("3) ConversationSummaryMemory (resumen automático)")
    print("=" * 60)

    memory = ConversationSummaryMemory(llm=llm)
    chain = ConversationChain(llm=llm, memory=memory, verbose=False)

    for turno in TURNOS:
        respuesta = chain.predict(input=turno)
        print(f"Usuario  : {turno}")
        print(f"Asistente: {respuesta}\n")

    print("Resumen actual del historial:")
    print(memory.buffer)


if __name__ == "__main__":
    demo_buffer_memory()
    demo_window_memory(k=2)
    demo_summary_memory()
