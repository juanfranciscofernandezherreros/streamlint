from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class ChatState(TypedDict):
    messages: List[BaseMessage]


def calculate_adaptive_window_size(state: ChatState) -> int:
    """Calcula tamano de ventana dinamicamente."""
    messages = state["messages"]
    base_size = 6

    # Mas contexto para programacion
    if any("codigo" in msg.content.lower() for msg in messages[-3:]):
        return base_size + 4

    # Mas contexto para narrativas
    if any("historia" in msg.content.lower() for msg in messages[-2:]):
        return base_size + 6

    # Menos mensajes si son muy largos
    if any(len(msg.content) > 500 for msg in messages[-2:]):
        return max(base_size - 2, 2)

    return base_size


def adaptive_sliding_window(state: ChatState) -> dict:
    """Ventana deslizante que se adapta al contexto."""
    messages = state["messages"]
    window_size = calculate_adaptive_window_size(state)

    if len(messages) <= window_size:
        return {}

    recent_messages = messages[-window_size:]
    return {"messages": recent_messages}


def chatbot_node(state: ChatState) -> dict:
    """Nodo que procesa mensajes y genera respuestas."""
    system_prompt = (
        "Eres un asistente amigable que adapta su ventana de contexto "
        "segun el tipo de conversacion (programacion, narrativas, etc.)."
    )
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def determine_window_strategy(state: ChatState) -> str:
    """Decide que estrategia de ventana usar."""
    if len(state["messages"]) > calculate_adaptive_window_size(state):
        return "adaptive_window"
    return "chatbot"


# Construir el grafo
workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("adaptive_window", adaptive_sliding_window)

workflow.add_conditional_edges(
    START, determine_window_strategy, ["adaptive_window", "chatbot"]
)
workflow.add_edge("adaptive_window", "chatbot")
workflow.add_edge("chatbot", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def chat(message, thread_id="sesion_terminal"):
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=message)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print("Chat con ventana deslizante adaptativa")
    print("La ventana se ajusta segun el contexto de la conversacion.")
    print("Escribe 'salir' para terminar\n")
    session_id = "sesion_terminal"

    while True:
        try:
            user_input = input("Tu: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"salir", "exit", "quit"}:
            print("Hasta luego!")
            break

        respuesta = chat(user_input, session_id)
        print("Asistente:", respuesta)
