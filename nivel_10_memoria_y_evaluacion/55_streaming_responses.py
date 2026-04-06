"""
55_streaming_responses.py
-------------------------
Respuestas en tiempo real con **streaming** de LangChain y LangGraph.

En lugar de esperar a que el modelo genere toda la respuesta antes de
mostrarla, el streaming entrega tokens en cuanto están disponibles,
mejorando la experiencia de usuario en aplicaciones interactivas.

Conceptos demostrados
---------------------
- ``stream()``        — Streaming síncrono de un LLM o cadena LCEL.
- ``astream()``       — Versión asíncrona con ``asyncio``.
- ``astream_events()``— Eventos detallados: tokens, inicio/fin de nodo, etc.
- Streaming en una cadena LCEL compuesta (``prompt | llm | parser``).
- Streaming en un grafo LangGraph (nodo chatbot).

Ejecutar:
    python nivel_10_memoria_y_evaluacion/55_streaming_responses.py
"""

import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, streaming=True)


# ---------------------------------------------------------------------------
# 1. Streaming directo del modelo
# ---------------------------------------------------------------------------

def ejemplo_stream_basico():
    """Stream token a token directamente desde el modelo."""
    print("\n=== 1. Streaming básico del modelo ===")
    print("Respuesta: ", end="", flush=True)
    for chunk in llm.stream("Escribe un haiku sobre programación en Python."):
        print(chunk.content, end="", flush=True)
    print()


# ---------------------------------------------------------------------------
# 2. Streaming en una cadena LCEL
# ---------------------------------------------------------------------------

def ejemplo_stream_cadena():
    """Stream de una cadena LCEL completa (prompt | llm | parser)."""
    print("\n=== 2. Streaming en cadena LCEL ===")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un experto en {lenguaje}. Responde de forma breve y clara."),
        ("human", "{pregunta}"),
    ])
    cadena = prompt | llm | StrOutputParser()

    print("Respuesta: ", end="", flush=True)
    for chunk in cadena.stream({
        "lenguaje": "Python",
        "pregunta": "¿Cuál es la diferencia entre una lista y una tupla?",
    }):
        print(chunk, end="", flush=True)
    print()


# ---------------------------------------------------------------------------
# 3. Streaming asíncrono con astream()
# ---------------------------------------------------------------------------

async def ejemplo_astream():
    """Stream asíncrono: ideal para aplicaciones web y chatbots."""
    print("\n=== 3. Streaming asíncrono (astream) ===")
    mensajes = [
        SystemMessage(content="Eres un asistente conciso."),
        HumanMessage(content="Explica en 3 pasos cómo funciona RAG."),
    ]
    print("Respuesta: ", end="", flush=True)
    async for chunk in llm.astream(mensajes):
        print(chunk.content, end="", flush=True)
    print()


# ---------------------------------------------------------------------------
# 4. astream_events() — eventos detallados por tipo
# ---------------------------------------------------------------------------

async def ejemplo_astream_events():
    """Recibe eventos tipados: on_llm_start, on_llm_stream, on_llm_end, etc."""
    print("\n=== 4. Eventos de streaming (astream_events) ===")
    cadena = (
        ChatPromptTemplate.from_template("Resume en una línea: {tema}")
        | llm
        | StrOutputParser()
    )

    token_count = 0
    async for event in cadena.astream_events(
        {"tema": "inteligencia artificial generativa"},
        version="v2",
    ):
        kind = event["event"]
        if kind == "on_llm_start":
            print("[on_llm_start] El modelo ha comenzado a generar.")
        elif kind == "on_llm_stream":
            chunk = event["data"]["chunk"].content
            if chunk:
                print(chunk, end="", flush=True)
                token_count += 1
        elif kind == "on_llm_end":
            print(f"\n[on_llm_end] Tokens recibidos: {token_count}")


# ---------------------------------------------------------------------------
# 5. Streaming en LangGraph
# ---------------------------------------------------------------------------

def construir_grafo():
    """Construye un grafo LangGraph simple con nodo chatbot."""
    def chatbot_node(state: MessagesState):
        return {"messages": [llm.invoke(state["messages"])]}

    grafo = StateGraph(MessagesState)
    grafo.add_node("chatbot", chatbot_node)
    grafo.add_edge(START, "chatbot")
    grafo.add_edge("chatbot", END)
    return grafo.compile(checkpointer=MemorySaver())


def ejemplo_stream_langgraph():
    """Streaming de updates de estado en un grafo LangGraph."""
    print("\n=== 5. Streaming en LangGraph ===")
    app = construir_grafo()
    config = {"configurable": {"thread_id": "stream-demo"}}
    entrada = {"messages": [HumanMessage(content="¿Qué es LangGraph en una frase?")]}

    print("Actualizaciones del grafo:")
    for update in app.stream(entrada, config, stream_mode="updates"):
        for nodo, valores in update.items():
            ultimo = valores["messages"][-1]
            print(f"  [{nodo}] → {ultimo.content}")


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Ejemplos síncronos
    ejemplo_stream_basico()
    ejemplo_stream_cadena()
    ejemplo_stream_langgraph()

    # Ejemplos asíncronos
    asyncio.run(ejemplo_astream())
    asyncio.run(ejemplo_astream_events())
