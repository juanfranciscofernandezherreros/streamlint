from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

MAX_TOKENS = 2000


class ChatState(TypedDict):
    messages: List[BaseMessage]


def estimate_tokens(text: str) -> int:
    """Estimacion simple de tokens (aproximadamente 4 caracteres por token)."""
    return len(text) // 4


def manage_memory_by_tokens(state: ChatState) -> dict:
    """Gestiona memoria basandose en limite de tokens."""
    messages = state["messages"]

    # Calcular tokens actuales
    total_tokens = sum(estimate_tokens(msg.content) for msg in messages)

    if total_tokens <= MAX_TOKENS:
        return {}  # No necesita gestion

    # Estrategia: mantener primer mensaje (system) + mensajes mas recientes
    if messages and isinstance(messages[0], SystemMessage):
        system_msg = messages[0]
        other_messages = messages[1:]
        current_tokens = estimate_tokens(system_msg.content)
    else:
        system_msg = None
        other_messages = messages
        current_tokens = 0

    # Agregar mensajes desde el mas reciente hasta alcanzar el limite
    selected_messages = []
    for msg in reversed(other_messages):
        msg_tokens = estimate_tokens(msg.content)
        if current_tokens + msg_tokens <= MAX_TOKENS:
            selected_messages.insert(0, msg)
            current_tokens += msg_tokens
        else:
            break

    # Reconstruir lista de mensajes
    final_messages = []
    if system_msg:
        final_messages.append(system_msg)
    final_messages.extend(selected_messages)

    return {"messages": final_messages}


def chatbot_node(state: ChatState) -> dict:
    """Nodo que procesa mensajes y genera respuestas."""
    system_prompt = (
        "Eres un asistente amigable que gestiona la memoria "
        "basandose en un limite de tokens."
    )
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def check_token_limit(state: ChatState) -> str:
    """Verifica si necesitamos gestion por tokens."""
    total_tokens = sum(estimate_tokens(msg.content) for msg in state["messages"])
    if total_tokens > MAX_TOKENS:
        return "manage_tokens"
    return "chatbot"


# Construir el grafo
workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("manage_tokens", manage_memory_by_tokens)

workflow.add_conditional_edges(
    START, check_token_limit, ["manage_tokens", "chatbot"]
)
workflow.add_edge("manage_tokens", "chatbot")
workflow.add_edge("chatbot", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def chat(message, thread_id="sesion_terminal"):
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=message)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print(f"Chat con limite de tokens ({MAX_TOKENS} tokens max)")
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
