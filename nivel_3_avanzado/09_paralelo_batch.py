"""
paralelo_batch.py
-----------------
Ejemplo de procesamiento en lote y paralelo con ``RunnableParallel`` y LangChain.

Extiende el ejemplo de ``paralelo.py`` procesando múltiples entradas a la vez
con ``.batch()``.  Las mismas tres ramas (respuesta, sentimiento, hashtags) se
ejecutan concurrentemente para cada tema de la lista de entradas.

El parámetro ``config={"max_concurrency": 5}`` permite limitar el número de
peticiones simultáneas a la API.

Requiere la variable de entorno ``OPENAI_API_KEY`` configurada (o asignada
directamente en ``os.environ``).

Ejecutar:
    python nivel_3_avanzado/09_paralelo_batch.py
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser

# 1. Configuración del modelo
os.environ["OPENAI_API_KEY"] = "tu_api_key_aquí"
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. Definición de ramas (Igual que antes)
prompt_respuesta = ChatPromptTemplate.from_template("Responde de forma concisa: {tema}")
cadena_respuesta = prompt_respuesta | model | StrOutputParser()

prompt_sentimiento = ChatPromptTemplate.from_template("¿Cuál es el sentimiento? Responde con una sola palabra: {tema}")
cadena_sentimiento = prompt_sentimiento | model | StrOutputParser()

prompt_tags = ChatPromptTemplate.from_template("Genera 3 hashtags: {tema}")
cadena_tags = prompt_tags | model | StrOutputParser()

# 3. Unión en RunnableParallel
cadena_final = RunnableParallel({
    "respuesta": cadena_respuesta,
    "análisis_sentimiento": cadena_sentimiento,
    "etiquetas": cadena_tags
})

# 4. PREPARACIÓN PARA BATCH (Lote de entradas)
entradas = [
    {"tema": "Me encanta la IA en el software"},
    {"tema": "Odio cuando el código no compila a la primera"},
    {"tema": "El clima está muy nublado hoy en la ciudad"}
]

# 5. Ejecución en BATCH y PARALELO
print(f"--- Procesando {len(entradas)} entradas en paralelo y batch ---")

# .batch() lanzará todas las ramas para todas las entradas de forma concurrente
# Puedes configurar el límite de hilos con config={"max_concurrency": 5}
resultados = cadena_final.batch(entradas)

# 6. Mostrar resultados
for i, res in enumerate(resultados):
    print(f"\n--- Resultado Entrada {i+1} ---")
    print(f"Tema original: {entradas[i]['tema']}")
    print(f"Respuesta: {res['respuesta']}")
    print(f"Sentimiento: {res['análisis_sentimiento']}")
    print(f"Hashtags: {res['etiquetas']}")