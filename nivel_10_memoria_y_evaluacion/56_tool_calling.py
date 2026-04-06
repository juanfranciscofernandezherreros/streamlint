"""
56_tool_calling.py
------------------
**Tool calling** (llamada a funciones) con LangChain y OpenAI.

OpenAI expone una API nativa de *function calling* que permite al modelo
decidir cuándo y cómo invocar herramientas externas. LangChain abstrae
este mecanismo con ``bind_tools()``, ``@tool`` y ``ToolNode`` de LangGraph.

Conceptos demostrados
---------------------
- ``@tool``            — Decorador para convertir una función Python en herramienta.
- ``bind_tools()``     — Vincula herramientas a un modelo para que las use automáticamente.
- Ejecución manual de la herramienta seleccionada por el modelo.
- ``ToolNode``         — Nodo LangGraph que ejecuta herramientas automáticamente.
- Agente ReAct (Reason + Act) básico con LangGraph y ciclo tool → chatbot.
- Respuesta estructurada con ``with_structured_output()`` y Pydantic.

Ejecutar:
    python nivel_10_memoria_y_evaluacion/56_tool_calling.py
"""

import ast
import math
import operator as op
import json
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ---------------------------------------------------------------------------
# Evaluador de expresiones matemáticas seguro (sin eval())
# ---------------------------------------------------------------------------

_OPERADORES = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _evaluar_nodo(nodo: ast.AST) -> float:
    """Recorre el AST de una expresión y devuelve el resultado numérico."""
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
        return float(nodo.value)
    if isinstance(nodo, ast.BinOp) and type(nodo.op) in _OPERADORES:
        return _OPERADORES[type(nodo.op)](
            _evaluar_nodo(nodo.left),
            _evaluar_nodo(nodo.right),
        )
    if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _OPERADORES:
        return _OPERADORES[type(nodo.op)](_evaluar_nodo(nodo.operand))
    raise ValueError(f"Operación no permitida en la expresión: {ast.dump(nodo)}")


# ---------------------------------------------------------------------------
# 1. Definición de herramientas con @tool
# ---------------------------------------------------------------------------

@tool
def calcular(expresion: str) -> str:
    """Evalúa una expresión matemática aritmética y devuelve el resultado numérico.

    Solo se permiten números y los operadores +, -, *, /, ** (sin funciones ni variables).

    Args:
        expresion: Expresión aritmética, p. ej. '2**10' o '(3 + 5) * 4'.
    """
    try:
        arbol = ast.parse(expresion.strip(), mode="eval")
        resultado = _evaluar_nodo(arbol.body)
        return str(resultado)
    except (ValueError, ZeroDivisionError, SyntaxError, KeyError) as exc:
        return f"Error al calcular: {exc}"


@tool
def convertir_temperatura(valor: float, de_unidad: str, a_unidad: str) -> str:
    """Convierte temperaturas entre Celsius, Fahrenheit y Kelvin.

    Args:
        valor:     Temperatura a convertir.
        de_unidad: Unidad de origen ('C', 'F' o 'K').
        a_unidad:  Unidad de destino ('C', 'F' o 'K').
    """
    de_unidad = de_unidad.upper()
    a_unidad = a_unidad.upper()

    # Convertir a Celsius primero
    if de_unidad == "C":
        celsius = valor
    elif de_unidad == "F":
        celsius = (valor - 32) * 5 / 9
    elif de_unidad == "K":
        celsius = valor - 273.15
    else:
        return f"Unidad desconocida: {de_unidad}"

    # Convertir Celsius al destino
    if a_unidad == "C":
        resultado = celsius
    elif a_unidad == "F":
        resultado = celsius * 9 / 5 + 32
    elif a_unidad == "K":
        resultado = celsius + 273.15
    else:
        return f"Unidad desconocida: {a_unidad}"

    return f"{valor}°{de_unidad} = {resultado:.2f}°{a_unidad}"


@tool
def buscar_capital(pais: str) -> str:
    """Devuelve la capital de un país hispanohablante o europeo conocido.

    Args:
        pais: Nombre del país en español.
    """
    capitales = {
        "españa": "Madrid",
        "mexico": "Ciudad de México",
        "argentina": "Buenos Aires",
        "colombia": "Bogotá",
        "chile": "Santiago",
        "peru": "Lima",
        "francia": "París",
        "alemania": "Berlín",
        "italia": "Roma",
        "portugal": "Lisboa",
        "japón": "Tokio",
        "china": "Pekín",
        "brasil": "Brasilia",
        "estados unidos": "Washington D.C.",
    }
    capital = capitales.get(pais.lower())
    return capital if capital else f"Capital de '{pais}' no disponible en este dataset."


herramientas = [calcular, convertir_temperatura, buscar_capital]


# ---------------------------------------------------------------------------
# 2. bind_tools() y ejecución manual de la herramienta elegida
# ---------------------------------------------------------------------------

def ejemplo_bind_tools_manual():
    """El modelo decide qué herramienta usar; nosotros la ejecutamos."""
    print("\n=== 1. bind_tools() con ejecución manual ===")
    llm_con_tools = llm.bind_tools(herramientas)

    preguntas = [
        "¿Cuánto es 2 elevado a 16?",
        "Convierte 100 grados Fahrenheit a Celsius.",
        "¿Cuál es la capital de Francia?",
    ]

    mapa_tools = {t.name: t for t in herramientas}

    for pregunta in preguntas:
        print(f"\nPregunta: {pregunta}")
        respuesta = llm_con_tools.invoke([HumanMessage(content=pregunta)])

        if respuesta.tool_calls:
            for llamada in respuesta.tool_calls:
                nombre = llamada["name"]
                args = llamada["args"]
                print(f"  → Herramienta elegida: {nombre}({args})")
                resultado = mapa_tools[nombre].invoke(args)
                print(f"  → Resultado: {resultado}")
        else:
            print(f"  → Respuesta directa: {respuesta.content}")


# ---------------------------------------------------------------------------
# 3. Agente ReAct con LangGraph (ciclo automático tool → chatbot)
# ---------------------------------------------------------------------------

def construir_agente():
    """Agente LangGraph con ciclo automático chatbot → tools → chatbot."""
    llm_agente = llm.bind_tools(herramientas)

    def chatbot_node(state: MessagesState):
        return {"messages": [llm_agente.invoke(state["messages"])]}

    grafo = StateGraph(MessagesState)
    grafo.add_node("chatbot", chatbot_node)
    grafo.add_node("tools", ToolNode(herramientas))

    grafo.add_edge(START, "chatbot")
    # tools_condition: si el último mensaje tiene tool_calls → "tools", si no → END
    grafo.add_conditional_edges("chatbot", tools_condition)
    grafo.add_edge("tools", "chatbot")

    return grafo.compile()


def ejemplo_agente_react():
    """Agente que resuelve una consulta encadenando herramientas automáticamente."""
    print("\n=== 2. Agente ReAct con LangGraph ===")
    agente = construir_agente()

    preguntas = [
        "¿Cuántos grados Kelvin son 37°C? Y también, ¿cuál es la capital de Chile?",
        "Si tengo 1024 elementos y quiero saber la raíz cuadrada, ¿cuál es?",
    ]

    for pregunta in preguntas:
        print(f"\nConsulta: {pregunta}")
        resultado = agente.invoke({"messages": [HumanMessage(content=pregunta)]})
        respuesta_final = resultado["messages"][-1].content
        print(f"Respuesta final: {respuesta_final}")


# ---------------------------------------------------------------------------
# 4. Salida estructurada con with_structured_output() y Pydantic
# ---------------------------------------------------------------------------

class ResumenPais(BaseModel):
    """Datos básicos de un país extraídos por el modelo."""
    nombre: str = Field(description="Nombre oficial del país")
    capital: str = Field(description="Capital del país")
    idioma_oficial: str = Field(description="Idioma oficial principal")
    continente: str = Field(description="Continente donde se encuentra")
    curiosidad: str = Field(description="Un dato curioso o interesante")


def ejemplo_structured_output():
    """Usa with_structured_output() para obtener datos validados con Pydantic."""
    print("\n=== 3. Salida estructurada con Pydantic ===")
    llm_estructurado = llm.with_structured_output(ResumenPais)

    paises = ["Japón", "Brasil", "Egipto"]
    for pais in paises:
        datos: ResumenPais = llm_estructurado.invoke(
            f"Dame los datos básicos del país: {pais}"
        )
        print(f"\n{datos.nombre}")
        print(f"  Capital:   {datos.capital}")
        print(f"  Idioma:    {datos.idioma_oficial}")
        print(f"  Continente:{datos.continente}")
        print(f"  Curiosidad:{datos.curiosidad}")


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ejemplo_bind_tools_manual()
    ejemplo_agente_react()
    ejemplo_structured_output()
