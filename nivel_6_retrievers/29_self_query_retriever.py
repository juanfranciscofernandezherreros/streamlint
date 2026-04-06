from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_classic.chains.query_constructor.base import AttributeInfo
from langchain_classic.retrievers.self_query.base import SelfQueryRetriever
from langchain.schema import Document

# 1. Crear documentos de ejemplo con metadatos ricos
# En un caso real estos vendrían de tus PDFs o base de datos
documentos = [
    Document(
        page_content="Contrato de arrendamiento de local comercial en Madrid, zona centro, 200 m².",
        metadata={"tipo": "arrendamiento", "ciudad": "Madrid", "año": 2022, "importe": 1500.0}
    ),
    Document(
        page_content="Contrato de compraventa de vivienda en Barcelona con hipoteca incluida.",
        metadata={"tipo": "compraventa", "ciudad": "Barcelona", "año": 2023, "importe": 250000.0}
    ),
    Document(
        page_content="Contrato de arrendamiento de piso residencial en Sevilla, 85 m².",
        metadata={"tipo": "arrendamiento", "ciudad": "Sevilla", "año": 2021, "importe": 850.0}
    ),
    Document(
        page_content="Contrato de compraventa de garaje en Valencia, con plaza de aparcamiento.",
        metadata={"tipo": "compraventa", "ciudad": "Valencia", "año": 2020, "importe": 18000.0}
    ),
    Document(
        page_content="Contrato de arrendamiento de oficina en Madrid, edificio de negocios, planta 5.",
        metadata={"tipo": "arrendamiento", "ciudad": "Madrid", "año": 2023, "importe": 3200.0}
    ),
    Document(
        page_content="Contrato de compraventa de local comercial en Bilbao, planta baja.",
        metadata={"tipo": "compraventa", "ciudad": "Bilbao", "año": 2022, "importe": 120000.0}
    ),
]

# 2. Crear el vector store con los documentos de ejemplo
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = FAISS.from_documents(documentos, embeddings)

# 3. Definir los metadatos disponibles en los documentos
metadata_field_info = [
    AttributeInfo(
        name="tipo",
        description="El tipo de contrato. Puede ser 'arrendamiento' o 'compraventa'",
        type="string"
    ),
    AttributeInfo(
        name="ciudad",
        description="La ciudad donde se ubica el inmueble del contrato",
        type="string"
    ),
    AttributeInfo(
        name="año",
        description="El año en que se firmó el contrato",
        type="integer"
    ),
    AttributeInfo(
        name="importe",
        description="El importe mensual (arrendamiento) o precio de venta (compraventa) en euros",
        type="float"
    ),
]

document_content_description = "Contrato inmobiliario con descripción del inmueble y condiciones"

# 4. Configurar el SelfQueryRetriever
# El LLM convierte la consulta en lenguaje natural en filtros estructurados automáticamente
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_content_description=document_content_description,
    metadata_field_info=metadata_field_info,
    verbose=True  # Muestra los filtros generados por el LLM
)

# 5. Ejecutar consultas que se convertirán en filtros estructurados
consultas = [
    "contratos de arrendamiento en Madrid",
    "contratos firmados después de 2021 con importe superior a 1000 euros",
    "contratos de compraventa en Barcelona o Valencia",
]

for consulta in consultas:
    print(f"=== Consulta: '{consulta}' ===\n")
    resultados = retriever.invoke(consulta)
    print(f"Resultados encontrados: {len(resultados)}")
    for i, doc in enumerate(resultados, start=1):
        print(f"  {i}. {doc.page_content[:200]}")
        print(f"     Metadatos: {doc.metadata}")
    print()
