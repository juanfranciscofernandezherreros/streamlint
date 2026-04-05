from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class ChatState(TypedDict):
    messages: List[BaseMessage]


def extract_keywords(text: str) -> List[str]:
    """Extrae palabras clave simples del texto."""
    words = text.lower().split()
    stop_words = {
        "el", "la", "de", "que", "y", "en", "un", "es", "se", "no",
        "te", "lo", "por", "con", "una", "los", "las", "del", "para",
        "como", "pero", "mas", "este", "esta", "son", "fue", "ser",
    }
    keywords = [word for word in words if len(word) > 3 and word not in stop_words]
    return list(set(keywords))[:10]


def calculate_relevance(text: str, keywords: List[str]) -> float:
    """Calcula relevancia simple basada en keywords."""
    text_lower = text.lower()
    matches = sum(1 for keyword in keywords if keyword in text_lower)
    return matches / max(len(keywords), 1)


def priority_context_memory(state: ChatState) -> dict:
    """Mantiene mensajes relevantes al contexto actual."""
    messages = state["messages"]

    if len(messages) <= 8:
        return {}

    # Obtener temas de los ultimos mensajes
    recent_content = " ".join([msg.content for msg in messages[-3:]])
    current_keywords = extract_keywords(recent_content)

    # Puntuar mensajes por relevancia
    scored_messages = []
    for i, msg in enumerate(messages):
        relevance_score = calculate_relevance(msg.content, current_keywords)
        # Los mensajes mas recientes tienen bonus
        recency_bonus = max(0, len(messages) - i) * 0.1
        total_score = relevance_score + recency_bonus
        scored_messages.append((total_score, msg))

    # Mantener top 8 mensajes mas relevantes
    scored_messages.sort(reverse=True)
    selected_messages = [msg for _, msg in scored_messages[:8]]

    # Reordenar cronologicamente
    selected_messages.sort(key=lambda x: messages.index(x))

    return {"messages": selected_messages}


def chatbot_node(state: ChatState) -> dict:
    """Nodo que procesa mensajes y genera respuestas."""
    system_prompt = (
        "Eres un asistente amigable que prioriza los mensajes mas "
        "relevantes para el contexto actual de la conversacion."
    )
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def should_prioritize(state: ChatState) -> str:
    """Decide si aplicar priorizacion de contexto."""
    if len(state["messages"]) > 8:
        return "prioritize"
    return "chatbot"


# Construir el grafo
workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("prioritize", priority_context_memory)

workflow.add_conditional_edges(START, should_prioritize, ["prioritize", "chatbot"])
workflow.add_edge("prioritize", "chatbot")
workflow.add_edge("chatbot", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def chat(message, thread_id="sesion_terminal"):
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=message)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print("Chat con prioridad de contexto")
    print("Los mensajes se priorizan segun su relevancia al tema actual.")
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
