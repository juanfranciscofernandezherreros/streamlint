"""
37_langgraph_checkpointer.py
----------------------------
Persistencia de estado con MemorySaver en LangGraph.

LangGraph permite guardar y recuperar el estado de un grafo entre invocaciones
mediante **checkpointers**.  El más sencillo es ``MemorySaver``, que almacena
en RAM; en producción se puede sustituir por ``SqliteSaver`` o integraciones
con bases de datos externas.

Clave: cada ejecución se identifica con un ``thread_id``.  Si se vuelve a
invocar el grafo con el mismo ``thread_id``, el grafo retoma el estado
exactamente donde lo dejó.

Se usa el reducer ``add_messages`` en el estado para que LangGraph acumule
los mensajes automáticamente en el checkpoint, evitando duplicados.

Conceptos clave:
- ``MemorySaver`` como checkpointer en memoria
- ``Annotated[..., add_messages]`` para acumulación automática de mensajes
- ``config = {"configurable": {"thread_id": "..."}}`` para identificar hilos
- Conversación multi-turno sin gestionar el historial manualmente

Ejecutar:
    python nivel_7_langgraph/37_langgraph_checkpointer.py
"""

from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# ---------------------------------------------------------------------------
# 1. Esquema del estado
# ---------------------------------------------------------------------------

class State(TypedDict):
    # add_messages es el reducer oficial de LangGraph: acumula mensajes en vez
    # de reemplazar la lista completa, evitando duplicados entre turnos.
    mensajes: Annotated[List[BaseMessage], add_messages]


# ---------------------------------------------------------------------------
# 2. Nodo del asistente
# ---------------------------------------------------------------------------

def asistente(state: State) -> State:
    """Responde al último mensaje del usuario manteniendo todo el historial."""
    respuesta = llm.invoke(state["mensajes"])
    # Solo devolvemos el nuevo mensaje; add_messages lo añadirá al historial
    return {"mensajes": [AIMessage(content=respuesta.content)]}


# ---------------------------------------------------------------------------
# 3. Construcción del grafo con checkpointer
# ---------------------------------------------------------------------------

memory = MemorySaver()

graph = StateGraph(State)
graph.add_node("Asistente", asistente)
graph.add_edge(START, "Asistente")
graph.add_edge("Asistente", END)

# El checkpointer se pasa al compilar el grafo
compiled = graph.compile(checkpointer=memory)


# ---------------------------------------------------------------------------
# 4. Simulación de una conversación multi-turno
# ---------------------------------------------------------------------------

def chat(thread_id: str, mensaje_usuario: str) -> str:
    """Envía un mensaje al grafo usando el hilo indicado y devuelve la respuesta.

    Gracias a ``add_messages`` y al checkpointer, basta con pasar solo el nuevo
    mensaje humano; LangGraph recupera el historial anterior del checkpoint y
    acumula el nuevo mensaje de forma automática.
    """
    config = {"configurable": {"thread_id": thread_id}}
    resultado = compiled.invoke(
        {"mensajes": [HumanMessage(content=mensaje_usuario)]},
        config=config,
    )
    return resultado["mensajes"][-1].content


if __name__ == "__main__":
    HILO = "usuario_demo"

    turnos = [
        "Hola, me llamo Lucía. ¿Cuál es tu función?",
        "¿Recuerdas cómo me llamo?",
        "¿Qué temas puedes ayudarme a explorar?",
    ]

    print("=== Conversación con persistencia de estado ===\n")
    for pregunta in turnos:
        print(f"Usuario : {pregunta}")
        respuesta = chat(HILO, pregunta)
        print(f"Asistente: {respuesta}\n")

