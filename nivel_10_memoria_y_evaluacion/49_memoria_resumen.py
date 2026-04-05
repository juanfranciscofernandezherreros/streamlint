from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class ChatState(TypedDict):
    messages: List[BaseMessage]
    conversation_summary: str
    message_count: int


def summarize_conversation(state: ChatState) -> dict:
    """Condensa mensajes antiguos en un resumen cuando se alcanza el limite."""
    messages = state["messages"]
    current_summary = state.get("conversation_summary", "")

    # Si tenemos menos de 10 mensajes, no resumir aun
    if len(messages) < 10:
        return {"message_count": len(messages)}

    # Mantener los ultimos 4 mensajes y resumir el resto
    recent_messages = messages[-4:]
    messages_to_summarize = messages[:-4]

    # Crear prompt para resumir
    summary_prompt = f"""
    Resumen anterior: {current_summary}

    Nuevos mensajes a resumir:
    {[f"{msg.type}: {msg.content}" for msg in messages_to_summarize]}

    Crea un resumen conciso que capture los puntos clave de la conversacion.
    """

    summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
    new_summary = summary_response.content

    # Crear mensaje de sistema con el resumen
    summary_message = SystemMessage(
        content=f"Resumen de conversacion previa: {new_summary}"
    )

    return {
        "messages": [summary_message] + recent_messages,
        "conversation_summary": new_summary,
        "message_count": len(recent_messages) + 1,
    }


def chatbot_node(state: ChatState) -> dict:
    """Nodo que procesa mensajes y genera respuestas."""
    messages = state["messages"]
    current_summary = state.get("conversation_summary", "")

    system_content = "Eres un asistente amigable que recuerda conversaciones previas."
    if current_summary:
        system_content += f"\n\nResumen de la conversacion hasta ahora: {current_summary}"

    all_messages = [SystemMessage(content=system_content)] + messages
    response = llm.invoke(all_messages)
    return {"messages": [response]}


def should_summarize(state: ChatState) -> str:
    """Decide si necesitamos resumir la conversacion."""
    if len(state["messages"]) >= 10:
        return "summarize"
    return "chatbot"


# Construir el grafo
workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("summarize", summarize_conversation)

workflow.add_conditional_edges(START, should_summarize, ["summarize", "chatbot"])
workflow.add_edge("summarize", "chatbot")
workflow.add_edge("chatbot", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def chat(message, thread_id="sesion_terminal"):
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke(
        {
            "messages": [HumanMessage(content=message)],
            "conversation_summary": "",
            "message_count": 0,
        },
        config,
    )
    return result["messages"][-1].content


if __name__ == "__main__":
    print("Chat con memoria de resumen (escribe 'salir' para terminar)\n")
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
