"""
08_analisis_sentimientos.py
------------------------
Pipeline de análisis de sentimientos con procesamiento paralelo y en lote.

Arquitectura de la cadena:

1. **Preprocesador** (``RunnableLambda``): limpia el texto y lo trunca a 500
   caracteres.
2. **Análisis paralelo** (``RunnableParallel``):
   - Rama ``resumen``: genera un resumen de una sola oración.
   - Rama ``sentimiento_data``: analiza el sentimiento y devuelve un JSON con
     ``sentimiento`` y ``razon``.
3. **Fusión** (``RunnableLambda``): combina ambos resultados en un único
   diccionario con las claves ``resumen``, ``sentimiento`` y ``razon``.

El pipeline procesa una lista de reseñas de ejemplo mediante ``.batch()``,
que ejecuta cada entrada de forma concurrente.

Requiere la variable de entorno ``OPENAI_API_KEY`` configurada.

Ejecutar:
    python nivel_3_avanzado/08_analisis_sentimientos.py
"""

from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
import json

# Configuración del modelo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Preprocesador: limpia espacios y limita a 500 caracteres
def preprocess_text(text):
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

# Generación de resumen
def generate_summary(text):
    """Genera un resumen conciso del texto"""
    prompt = f"Resume en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content

summary_branch = RunnableLambda(generate_summary)

# Análisis de sentimiento con formato JSON
def analyze_sentiment(text):
    """Analiza el sentimiento y devuelve resultado estructurado"""
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde ÚNICAMENTE en formato JSON válido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
    
    Texto: {text}"""
    
    response = llm.invoke(prompt)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en análisis"}
    
sentiment_branch = RunnableLambda(analyze_sentiment)

# Combinación de resultados
def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

merger = RunnableLambda(merge_results)

parallel_analysis = RunnableParallel({
    "resumen": summary_branch,
    "sentimiento_data": sentiment_branch
})

# Cadena completa
chain = preprocessor | parallel_analysis | merger

reviews_batch = [
    "Excelente producto, muy satisfecho con la compra",
    "Terrible calidad, no lo recomiendo para nada",
    "Está bien, cumple su función básica pero nada especial"
]

resultado_batch = chain.batch(reviews_batch)

print(resultado_batch)