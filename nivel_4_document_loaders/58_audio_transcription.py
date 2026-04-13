"""
58_audio_transcription.py
--------------------------
Transcripción de archivos de audio MP3/MP4 con la API Whisper de OpenAI.

La API ``openai.audio.transcriptions`` acepta archivos de audio en múltiples
formatos (mp3, mp4, wav, m4a, webm…) y devuelve el texto transcrito.
El resultado se envuelve en un objeto ``Document`` de LangChain, listo para
usarse en cualquier pipeline de RAG.

Flujo:
1. Se lee el archivo de audio/vídeo indicado.
2. Se envía a la API Whisper (modelo ``whisper-1``) para su transcripción.
3. Se crea un ``Document`` con el texto y metadatos (ruta, formato, idioma).
4. Se muestran el texto y las estadísticas básicas por consola.

Dependencias ya incluidas en ``requirements.txt``:
    openai      # cliente de la API de OpenAI (Whisper)

Uso:
    python nivel_4_document_loaders/58_audio_transcription.py <ruta_al_audio>

    # Ejemplos
    python nivel_4_document_loaders/58_audio_transcription.py audio/reunion.mp3
    python nivel_4_document_loaders/58_audio_transcription.py video/conferencia.mp4
"""

import os
import sys

import openai
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

# Extensiones de audio/vídeo soportadas por Whisper
SUPPORTED_EXTENSIONS = {".mp3", ".mp4", ".m4a", ".wav", ".webm", ".mov", ".mkv"}


def transcribe_audio(file_path: str, language: str = "es") -> Document:
    """Transcribe un archivo MP3/MP4 y devuelve un ``Document`` de LangChain.

    Args:
        file_path: Ruta al archivo de audio o vídeo.
        language:  Código de idioma ISO-639-1 (por defecto ``"es"``).

    Returns:
        ``Document`` con la transcripción en ``page_content`` y metadatos.

    Raises:
        ValueError: Si la extensión del archivo no está soportada.
        FileNotFoundError: Si el archivo no existe.
    """
    abs_path = os.path.abspath(file_path)

    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"Archivo no encontrado: {abs_path}")

    ext = os.path.splitext(abs_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(
            f"Extensión '{ext}' no soportada. Formatos válidos: {supported}"
        )

    file_name = os.path.basename(abs_path)
    file_size_kb = os.path.getsize(abs_path) / 1024

    print(f"🎙️  Archivo:  {file_name}")
    print(f"📦  Tamaño:   {file_size_kb:.1f} KB")
    print(f"🌐  Idioma:   {language}")
    print("⏳  Transcribiendo con OpenAI Whisper...")

    client = openai.OpenAI()

    with open(abs_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language,
            response_format="text",
        )

    doc = Document(
        page_content=transcript,
        metadata={
            "source": abs_path,
            "file_name": file_name,
            "format": ext.lstrip("."),
            "language": language,
            "size_kb": round(file_size_kb, 1),
        },
    )

    return doc


def display_document(doc: Document) -> None:
    """Imprime la transcripción y sus estadísticas por consola."""
    text = doc.page_content
    meta = doc.metadata

    words = len(text.split())
    chars = len(text)

    print("\n=== TRANSCRIPCIÓN ===")
    print(text)

    print("\n=== METADATOS ===")
    print(f"Archivo:    {meta['file_name']}")
    print(f"Formato:    {meta['format']}")
    print(f"Idioma:     {meta['language']}")
    print(f"Tamaño:     {meta['size_kb']} KB")
    print(f"Palabras:   {words:,}")
    print(f"Caracteres: {chars:,}")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python nivel_4_document_loaders/58_audio_transcription.py <ruta_al_audio>")
        print(f"Formatos soportados: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
        sys.exit(1)

    audio_path = sys.argv[1]

    try:
        doc = transcribe_audio(audio_path)
        display_document(doc)
    except (FileNotFoundError, ValueError) as exc:
        print(f"❌ {exc}")
        sys.exit(1)
    except openai.AuthenticationError:
        print("❌ Error de autenticación: comprueba que OPENAI_API_KEY esté configurada.")
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        print(f"❌ Error inesperado: {exc}")
        sys.exit(1)
