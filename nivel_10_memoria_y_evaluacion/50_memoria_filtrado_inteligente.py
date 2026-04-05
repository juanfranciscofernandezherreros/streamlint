from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class ChatState(TypedDict):
    messages: List[BaseMessage]


def filter_important_messages(state: ChatState) -> dict:
    """Mantiene mensajes importantes y elimina menos relevantes."""
    messages = state["messages"]

    if len(messages) <= 8:
        return {}  # No necesita filtrado aun

    important_messages = []
    regular_messages = []

    for msg in messages:
        # Criterios para mensajes importantes
        is_important = (
            isinstance(msg, SystemMessage)
            or "importante" in msg.content.lower()
            or "recuerda" in msg.content.lower()
            or "preferencia" in msg.content.lower()
            or len(msg.content) > 200  # Mensajes largos pueden ser importantes
        )

        if is_important:
            important_messages.append(msg)
        else:
            regular_messages.append(msg)

    # Mantener todos los importantes + los 4 regulares mas recientes
    filtered_messages = important_messages + regular_messages[-4:]

    return {"messages": filtered_messages}


def chatbot_node(state: ChatState) -> dict:
    """Nodo que procesa mensajes y genera respuestas."""
    system_prompt = (
        "Eres un asistente amigable que filtra y recuerda "
        "los mensajes mas importantes de la conversacion."
    )
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def analyze_message_importance(state: ChatState) -> str:
    """Decide si aplicar filtrado por importancia."""
    if len(state["messages"]) > 8:
        return "filter"
    return "chatbot"


# Construir el grafo
workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("filter", filter_important_messages)

workflow.add_conditional_edges(START, analyze_message_importance, ["filter", "chatbot"])
workflow.add_edge("filter", "chatbot")
workflow.add_edge("chatbot", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def chat(message, thread_id="sesion_terminal"):
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=message)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print("Chat con filtrado inteligente (escribe 'salir' para terminar)\n")
    print("Tip: usa palabras como 'importante', 'recuerda' o 'preferencia'")
    print("para marcar mensajes que no deben perderse.\n")
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
