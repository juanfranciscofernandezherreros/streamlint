"""
19_google_drive.py
------------------
Ejemplo de carga de documentos desde Google Drive con ``GoogleDriveLoader``.

``GoogleDriveLoader`` accede a una carpeta de Google Drive mediante la API
oficial y descarga todos los documentos que contiene (Google Docs, hojas de
cálculo, PDFs, etc.), devolviéndolos como objetos ``Document`` de LangChain.

Requisitos previos:
1. Crear un proyecto en Google Cloud Console y habilitar la API de Google Drive.
2. Generar credenciales OAuth 2.0 (tipo «Aplicación de escritorio») y
   descargar el archivo ``credentials.json``.
3. En el primer uso se abrirá el navegador para autorizar el acceso; el token
   se guardará en ``token.json`` para usos posteriores.

Instalación de dependencias:
    pip install langchain-google-community google-auth-oauthlib google-api-python-client

Variables a configurar antes de ejecutar:
    credentials_path  ← ruta absoluta al archivo credentials.json
    token_path        ← ruta absoluta donde se guardará/leerá el token.json
    folder_id         ← ID de la carpeta de Google Drive a cargar

Ejecutar:
    python nivel_4_document_loaders/19_google_drive.py
"""

from langchain_community.document_loaders import GoogleDriveLoader

credentials_path = "credentials.json"
token_path = "token.json"

loader = GoogleDriveLoader(
    folder_id="17DDwGPRjhjZhR6NRpegkFEmA4Wo6M_l3",
    credentials_path=credentials_path,
    token_path=token_path,
    recursive=True
)

documents = loader.load()

print(f"Documentos cargados: {len(documents)}")
print(f"Metadatos: {documents[0].metadata}")
print(f"Contenido: {documents[0].page_content}")

