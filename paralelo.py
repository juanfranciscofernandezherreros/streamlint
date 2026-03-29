import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser

# 1. Configuración del modelo
# Asegúrate de tener tu API Key en las variables de entorno
os.environ["OPENAI_API_KEY"] = "tu_api_key_aquí"
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. Definimos los diferentes "caminos" o ramas
# Rama 1: Generar la respuesta principal
prompt_respuesta = ChatPromptTemplate.from_template("Responde de forma concisa: {tema}")
cadena_respuesta = prompt_respuesta | model | StrOutputParser()

# Rama 2: Detectar el sentimiento (enojado, feliz, neutral...)
prompt_sentimiento = ChatPromptTemplate.from_template("¿Cuál es el sentimiento predominante en este mensaje? Responde con una sola palabra: {tema}")
cadena_sentimiento = prompt_sentimiento | model | StrOutputParser()

# Rama 3: Extraer 3 etiquetas (hashtags)
prompt_tags = ChatPromptTemplate.from_template("Genera 3 hashtags para este tema: {tema}")
cadena_tags = prompt_tags | model | StrOutputParser()

# 3. Unimos todo en un RunnableParallel
# El diccionario define las "llaves" que tendrá el resultado final
cadena_final = RunnableParallel({
    "respuesta": cadena_respuesta,
    "análisis_sentimiento": cadena_sentimiento,
    "etiquetas": cadena_tags
})

# 4. Ejecución
print("--- Iniciando ejecución paralela ---")
entrada = {"tema": "Me encanta cómo la inteligencia artificial está cambiando el desarrollo de software"}

# .invoke() lanzará las 3 llamadas a OpenAI simultáneamente
resultado = cadena_final.invoke(entrada)

# 5. Mostrar resultados
print(f"Respuesta: {resultado['respuesta']}")
print(f"Sentimiento: {resultado['análisis_sentimiento']}")
print(f"Hashtags: {resultado['etiquetas']}")