"""
16_csv_loader.py
----------------
Ejemplo de carga de datos tabulares con ``CSVLoader`` de LangChain.

``CSVLoader`` convierte cada fila de un archivo CSV en un objeto ``Document``
independiente.  El ``page_content`` contiene todos los campos como texto libre
(``campo: valor``) y ``metadata`` puede incluir columnas seleccionadas como
atributos adicionales.

Parámetros clave:
- ``source_column``: columna que se usa como identificador del documento.
- ``metadata_columns``: columnas que se incluyen en los metadatos.
- ``csv_args``: opciones de ``csv.DictReader`` (delimitador, comillas, etc.).

Ejecutar:
    python nivel_4_document_loaders/16_csv_loader.py
"""

import csv
import os
import tempfile
from langchain_community.document_loaders import CSVLoader

# Creamos un CSV de ejemplo para la demostración
SAMPLE_CSV = """fecha,producto,cantidad,precio,cliente
2024-01-15,Laptop Pro,2,1200.00,Empresa ABC
2024-01-16,Monitor 4K,5,350.00,Empresa XYZ
2024-01-17,Teclado Mecánico,10,85.00,Empresa ABC
2024-01-18,Ratón Ergonómico,8,45.00,Freelancer Juan
2024-01-19,Laptop Pro,1,1200.00,Freelancer María
"""

tmp = tempfile.NamedTemporaryFile(
    suffix=".csv", mode="w", encoding="utf-8", delete=False
)
tmp.write(SAMPLE_CSV)
tmp.close()

try:
    loader = CSVLoader(
        file_path=tmp.name,
        csv_args={
            "delimiter": ",",
            "quotechar": '"',
            "fieldnames": ["fecha", "producto", "cantidad", "precio", "cliente"],
        },
        encoding="utf-8",
        source_column="producto",
        metadata_columns=["fecha", "cliente"],
    )

    docs = loader.load()
    # El primer registro corresponde a la cabecera; lo omitimos si es necesario
    data_docs = [d for d in docs if d.metadata.get("cliente") != "cliente"]

    print(f"Registros cargados: {len(data_docs)}")

    # Mostrar los primeros 3 registros
    for doc in data_docs[:3]:
        print(f"\nContenido:\n{doc.page_content}")
        print(f"Metadatos: {doc.metadata}")

    # Estadísticas rápidas
    clientes = {d.metadata.get("cliente") for d in data_docs}
    fechas = {d.metadata.get("fecha") for d in data_docs}

    print(f"\nResumen de datos:")
    print(f"  Clientes únicos:     {len(clientes)}")
    print(f"  Fechas con ventas:   {len(fechas)}")
    print(f"  Promedio ventas/día: {len(data_docs) / max(len(fechas), 1):.1f}")

finally:
    os.unlink(tmp.name)
