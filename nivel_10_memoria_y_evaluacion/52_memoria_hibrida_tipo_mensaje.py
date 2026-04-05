from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class ChatState(TypedDict):
    messages: List[BaseMessage]


def hybrid_memory_management(state: ChatState) -> dict:
    """Aplica diferentes estrategias segun el tipo de mensaje."""
    messages = state["messages"]

    if len(messages) <= 6:
        return {}

    system_messages = []
    human_messages = []
    ai_messages = []

    # Clasificar mensajes por tipo
    for msg in messages:
        if isinstance(msg, SystemMessage):
            system_messages.append(msg)
        elif isinstance(msg, HumanMessage):
            human_messages.append(msg)
        elif isinstance(msg, AIMessage):
            ai_messages.append(msg)

    # Estrategias diferenciadas:
    # - Mantener TODOS los system messages
    # - Mantener los ultimos 4 human messages
    # - Mantener solo las ultimas 2 AI responses
    filtered_messages = []
    filtered_messages.extend(system_messages)
    filtered_messages.extend(human_messages[-4:])
    filtered_messages.extend(ai_messages[-2:])

    # Reordenar cronologicamente
    filtered_messages.sort(key=lambda x: messages.index(x))

    return {"messages": filtered_messages}


def chatbot_node(state: ChatState) -> dict:
    """Nodo que procesa mensajes y genera respuestas."""
    system_prompt = (
        "Eres un asistente amigable que aplica estrategias de retencion "
        "diferenciadas segun el tipo de mensaje."
    )
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def should_apply_hybrid(state: ChatState) -> str:
    """Decide si aplicar gestion hibrida por tipo de mensaje."""
    if len(state["messages"]) > 6:
        return "hybrid"
    return "chatbot"


# Construir el grafo
workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("hybrid", hybrid_memory_management)

workflow.add_conditional_edges(START, should_apply_hybrid, ["hybrid", "chatbot"])
workflow.add_edge("hybrid", "chatbot")
workflow.add_edge("chatbot", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def chat(message, thread_id="sesion_terminal"):
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=message)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print("Chat con memoria hibrida por tipo de mensaje")
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
