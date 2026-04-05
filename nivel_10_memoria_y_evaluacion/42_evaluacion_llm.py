"""
42_evaluacion_llm.py
--------------------
Evaluación básica de salidas de modelos de lenguaje con LangChain.

Evaluar si un LLM produce respuestas correctas, relevantes y bien formateadas
es esencial antes de desplegar una aplicación.  LangChain incluye evaluadores
listos para usar en ``langchain.evaluation``.

Este módulo demuestra tres evaluadores:

1. **CriteriaEvalChain** — puntúa la respuesta según criterios predefinidos
   (relevancia, concisión, corrección gramatical…).
2. **QAEvalChain** — compara la respuesta del modelo con una respuesta
   esperada (ground truth) para medir la exactitud.
3. **Evaluador personalizado** — muestra cómo construir criterios a medida.

Ejecutar:
    python nivel_10_memoria_y_evaluacion/42_evaluacion_llm.py
"""

from langchain_openai import ChatOpenAI
from langchain.evaluation import load_evaluator, EvaluatorType

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ---------------------------------------------------------------------------
# Datos de prueba
# ---------------------------------------------------------------------------

PREGUNTA = "¿Cuál es la capital de Francia y cuántos habitantes tiene?"

RESPUESTA_CORRECTA = (
    "La capital de Francia es París, con una población de aproximadamente "
    "2,1 millones de habitantes en la ciudad y más de 12 millones en el área metropolitana."
)

RESPUESTA_INCORRECTA = (
    "La capital de Francia es Lyon, una ciudad conocida por su gastronomía."
)

RESPUESTA_INCOMPLETA = "París."


# ---------------------------------------------------------------------------
# 1. Evaluación por criterios predefinidos
# ---------------------------------------------------------------------------

def evaluar_por_criterios(respuesta: str, etiqueta: str) -> None:
    """Evalúa *respuesta* según criterios estándar de LangChain."""
    evaluador = load_evaluator(
        EvaluatorType.CRITERIA,
        llm=llm,
        criteria="relevance",   # mide si la respuesta aborda realmente la pregunta formulada
    )
    resultado = evaluador.evaluate_strings(
        prediction=respuesta,
        input=PREGUNTA,
    )
    print(f"\n[{etiqueta}]")
    print(f"  Respuesta  : {respuesta[:80]}{'…' if len(respuesta) > 80 else ''}")
    print(f"  Puntuación : {resultado.get('score')}")
    print(f"  Razonamiento: {resultado.get('reasoning', '').strip()}")


# ---------------------------------------------------------------------------
# 2. Evaluación QA (respuesta vs. ground truth)
# ---------------------------------------------------------------------------

def evaluar_qa(respuesta: str, etiqueta: str) -> None:
    """Compara *respuesta* con la respuesta esperada."""
    evaluador = load_evaluator(EvaluatorType.QA, llm=llm)
    resultado = evaluador.evaluate_strings(
        prediction=respuesta,
        reference=RESPUESTA_CORRECTA,
        input=PREGUNTA,
    )
    print(f"\n[{etiqueta}] QA")
    print(f"  Respuesta  : {respuesta[:80]}{'…' if len(respuesta) > 80 else ''}")
    print(f"  Resultado  : {resultado.get('results', resultado.get('score'))}")


# ---------------------------------------------------------------------------
# 3. Evaluación con criterio personalizado
# ---------------------------------------------------------------------------

def evaluar_criterio_personalizado(respuesta: str) -> None:
    """Evalúa si la respuesta incluye tanto la capital como la población."""
    criterio_custom = {
        "completitud": (
            "¿La respuesta menciona tanto el nombre de la capital como "
            "datos de población? Responde Y si es así, N si no."
        )
    }
    evaluador = load_evaluator(
        EvaluatorType.CRITERIA,
        llm=llm,
        criteria=criterio_custom,
    )
    resultado = evaluador.evaluate_strings(
        prediction=respuesta,
        input=PREGUNTA,
    )
    print(f"\n[Criterio personalizado — completitud]")
    print(f"  Respuesta  : {respuesta[:80]}{'…' if len(respuesta) > 80 else ''}")
    print(f"  Puntuación : {resultado.get('score')}")
    print(f"  Razonamiento: {resultado.get('reasoning', '').strip()}")


# ---------------------------------------------------------------------------
# Ejecución
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Evaluación de salidas LLM con LangChain")
    print("=" * 60)

    # Evaluación por criterio de relevancia
    for etiqueta, respuesta in [
        ("Correcta", RESPUESTA_CORRECTA),
        ("Incorrecta", RESPUESTA_INCORRECTA),
        ("Incompleta", RESPUESTA_INCOMPLETA),
    ]:
        evaluar_por_criterios(respuesta, etiqueta)

    print("\n" + "-" * 60)

    # Evaluación QA
    for etiqueta, respuesta in [
        ("Correcta", RESPUESTA_CORRECTA),
        ("Incorrecta", RESPUESTA_INCORRECTA),
    ]:
        evaluar_qa(respuesta, etiqueta)

    print("\n" + "-" * 60)

    # Criterio personalizado
    for respuesta in [RESPUESTA_CORRECTA, RESPUESTA_INCOMPLETA]:
        evaluar_criterio_personalizado(respuesta)
