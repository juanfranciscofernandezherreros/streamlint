# 📁 datos/

Recursos y datos de ejemplo utilizados por los scripts del curso.

## Contenido

| Archivo / Carpeta | Descripción | Usado en |
|-------------------|-------------|----------|
| `cambridge_english_first.pdf` | PDF de ejemplo para document loaders y text splitters | Niveles 4–5 (scripts 12, 20, 21) |
| `Simulacion_reunion.mp4` | Vídeo de simulación de reunión para transcripción con Whisper | Nivel 7 (scripts 33, 35) |
| `historial_chat.json` | Historial de conversación de ejemplo | Nivel 1 (script 04) |
| `contratos/` | 5 PDFs de contratos de arrendamiento para ejemplos RAG | Nivel 6 (scripts 23, 27, 28) y Nivel 9 (asistente_legal) |
| `sesiones/` | Sesiones de chat persistidas en JSON | Nivel 8 (script 39) |

## Carpeta `contratos/`

Contiene contratos en formato PDF para pruebas de RAG y retrievers:

- `CONTRATO DE ARRENDAMIENTO DE LOCAL DE NEGOCIO.pdf`
- `CONTRATO DE ARRENDAMIENTO DE LOCAL DE NEGOCIO 2.pdf`
- `CONTRATO DE ARRENDAMIENTO DE PLAZA DE GARAJE.pdf`
- `CONTRATO DE ARRENDAMIENTO DE VIVIENDA 1.pdf`
- `CONTRATO DE ARRENDAMIENTO DE VIVIENDA 2.pdf`

## Carpeta `sesiones/`

Archivos JSON con conversaciones guardadas por la app de chatbot (`39_streamlit_chatbox.py`).

## Notas

- Estos archivos son necesarios para la ejecución de varios scripts del curso.
- El índice FAISS generado por `23_vector_stores.py` se guarda en `faiss_db/` (en la raíz del proyecto, no aquí).
