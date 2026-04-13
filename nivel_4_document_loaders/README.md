# ⭐⭐⭐ Nivel 4 — Document Loaders: Carga de Documentos

Carga de documentos desde **9 fuentes diferentes**: web, PDF, carpetas, YouTube, HTML, CSV, Selenium, repositorios Git y Google Drive.

## Scripts

| # | Archivo | Descripción | Loader |
|---|---------|-------------|--------|
| 11 | `11_read_from_website.py` | Cargar contenido web | `WebBaseLoader` |
| 12 | `12_read_pdf.py` | Leer archivos PDF | `PyPDFLoader` |
| 13 | `13_directory_loader.py` | Cargar carpetas completas de forma recursiva | `DirectoryLoader` |
| 14 | `14_youtube_loader.py` | Extraer transcripciones de YouTube | `YoutubeLoader` |
| 15 | `15_unstructured_html_loader.py` | Procesar HTML local por elementos | `UnstructuredHTMLLoader` |
| 16 | `16_csv_loader.py` | Cargar datos tabulares CSV | `CSVLoader` |
| 17 | `17_selenium_url_loader.py` | Cargar sitios con JavaScript (SPAs) | `SeleniumURLLoader` |
| 18 | `18_git_loader.py` | Cargar código fuente desde repositorios Git | `GitLoader` |
| 19 | `19_google_drive.py` | Cargar documentos desde Google Drive | `GoogleDriveLoader` |
| 58 | `58_audio_transcription.py` | Transcribir audio MP3/MP4 con Whisper | `openai.audio.transcriptions` |

## Conceptos clave

- Cada loader devuelve una lista de objetos `Document` con `page_content` y `metadata`.
- Los documentos cargados son el punto de partida para pipelines de **RAG** (Retrieval-Augmented Generation).
- Algunos loaders requieren dependencias opcionales (ver más abajo).

## Ejecución

```bash
python nivel_4_document_loaders/11_read_from_website.py
python nivel_4_document_loaders/12_read_pdf.py
python nivel_4_document_loaders/13_directory_loader.py
python nivel_4_document_loaders/14_youtube_loader.py
python nivel_4_document_loaders/15_unstructured_html_loader.py
python nivel_4_document_loaders/16_csv_loader.py
python nivel_4_document_loaders/17_selenium_url_loader.py
python nivel_4_document_loaders/18_git_loader.py
python nivel_4_document_loaders/19_google_drive.py
python nivel_4_document_loaders/58_audio_transcription.py audio/reunion.mp3
```

## Dependencias opcionales

```bash
pip install beautifulsoup4         # WebBaseLoader (11)
pip install pypdf                  # PyPDFLoader (12)
pip install unstructured           # DirectoryLoader / UnstructuredHTMLLoader (13, 15)
pip install youtube-transcript-api # YoutubeLoader (14)
pip install selenium               # SeleniumURLLoader (17)
pip install gitpython              # GitLoader (18)
pip install langchain-google-community google-auth-oauthlib google-api-python-client  # GoogleDriveLoader (19)
# pip install openai   # ya incluido en requirements.txt — Whisper transcription (58)
```

## Navegación

⬅️ [Nivel 3 — Avanzado](../nivel_3_avanzado/) · ➡️ [Nivel 5 — Text Splitters y Embeddings](../nivel_5_text_splitters_y_embeddings/)
