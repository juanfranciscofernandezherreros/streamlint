"""
36_langgraph_condicional.py
---------------------------
Edges condicionales avanzados en LangGraph.

Demuestra cómo construir grafos con múltiples ramas de ejecución basadas en
el estado del flujo.  Se modela un clasificador de texto que deriva cada entrada
a un nodo especializado (positivo, negativo o neutro) antes de generar una
respuesta final.

Conceptos clave:
- ``add_conditional_edges`` con función de routing
- Múltiples ramas que convergen en un nodo final
- Estado intermedio compartido entre nodos

Ejecutar:
    python nivel_7_langgraph/36_langgraph_condicional.py
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


# ---------------------------------------------------------------------------
# 1. Esquema del estado
# ---------------------------------------------------------------------------

class State(TypedDict):
    texto: str
    sentimiento: str   # "positivo" | "negativo" | "neutro"
    respuesta: str


# ---------------------------------------------------------------------------
# 2. Nodos
# ---------------------------------------------------------------------------

def clasificar_sentimiento(state: State) -> State:
    """Clasifica el sentimiento del texto como positivo, negativo o neutro."""
    prompt = (
        "Clasifica el sentimiento del siguiente texto con UNA sola palabra: "
        "positivo, negativo o neutro.\n\n"
        f"Texto: {state['texto']}\n\n"
        "Responde únicamente con la palabra elegida."
    )
    try:
        resultado = llm.invoke(prompt).content.strip().lower()
    except Exception:
        return {"sentimiento": "neutro"}
    # Normalizar la respuesta por si el modelo añade puntuación
    for opcion in ("positivo", "negativo", "neutro"):
        if opcion in resultado:
            return {"sentimiento": opcion}
    return {"sentimiento": "neutro"}


def responder_positivo(state: State) -> State:
    """Genera una respuesta entusiasta para texto con sentimiento positivo."""
    prompt = (
        f"El usuario ha escrito algo positivo: '{state['texto']}'. "
        "Respóndele con entusiasmo y ánimo en una frase corta."
    )
    return {"respuesta": llm.invoke(prompt).content.strip()}


def responder_negativo(state: State) -> State:
    """Genera una respuesta empática para texto con sentimiento negativo."""
    prompt = (
        f"El usuario ha escrito algo negativo: '{state['texto']}'. "
        "Respóndele con empatía y palabras de apoyo en una frase corta."
    )
    return {"respuesta": llm.invoke(prompt).content.strip()}


def responder_neutro(state: State) -> State:
    """Genera una respuesta informativa para texto con sentimiento neutro."""
    prompt = (
        f"El usuario ha escrito algo neutro: '{state['texto']}'. "
        "Respóndele de forma amable e informativa en una frase corta."
    )
    return {"respuesta": llm.invoke(prompt).content.strip()}


# ---------------------------------------------------------------------------
# 3. Función de routing
# ---------------------------------------------------------------------------

def elegir_rama(state: State) -> str:
    """Devuelve el nombre del nodo al que debe dirigirse el flujo."""
    return state["sentimiento"]


# ---------------------------------------------------------------------------
# 4. Construcción del grafo
# ---------------------------------------------------------------------------

graph = StateGraph(State)

graph.add_node("Clasificar", clasificar_sentimiento)
graph.add_node("positivo", responder_positivo)
graph.add_node("negativo", responder_negativo)
graph.add_node("neutro", responder_neutro)

graph.add_edge(START, "Clasificar")

# El nodo "Clasificar" enruta a tres ramas distintas según el sentimiento
graph.add_conditional_edges(
    "Clasificar",
    elegir_rama,
    {"positivo": "positivo", "negativo": "negativo", "neutro": "neutro"},
)

graph.add_edge("positivo", END)
graph.add_edge("negativo", END)
graph.add_edge("neutro", END)

compiled = graph.compile()


# ---------------------------------------------------------------------------
# 5. Ejemplos de ejecución
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ejemplos = [
        "¡Hoy ha sido un día increíble, conseguí el trabajo que quería!",
        "Me siento muy triste, nada me sale bien últimamente.",
        "Mañana tengo una reunión a las diez de la mañana.",
    ]

    for texto in ejemplos:
        print(f"\nTexto  : {texto}")
        resultado = compiled.invoke({"texto": texto})
        print(f"Sentimiento: {resultado['sentimiento']}")
        print(f"Respuesta  : {resultado['respuesta']}")
