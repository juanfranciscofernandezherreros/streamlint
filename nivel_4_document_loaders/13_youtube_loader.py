"""
13_youtube_loader.py
--------------------
Ejemplo de extracción de transcripciones de YouTube con ``YoutubeLoader``.

``YoutubeLoader`` descarga la transcripción automática (subtítulos) de un
vídeo de YouTube sin necesidad de la API oficial.  El documento generado
contiene la transcripción completa como ``page_content`` y metadatos como
título, autor, duración y número de vistas.

Parámetros clave:
- ``add_video_info``: incluye metadatos del vídeo (título, autor, etc.).
- ``language``: lista de idiomas preferidos para la transcripción.
- ``translation``: traduce la transcripción al idioma indicado si está disponible.

Dependencia adicional:
    pip install youtube-transcript-api

Ejecutar:
    python nivel_4_document_loaders/13_youtube_loader.py
"""

import re
from collections import Counter
from langchain_community.document_loaders import YoutubeLoader

# Sustituye esta URL por un vídeo que tenga subtítulos disponibles
VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

loader = YoutubeLoader.from_youtube_url(
    VIDEO_URL,
    add_video_info=True,
    language=["es", "en"],  # priorizar español; inglés como alternativa
    translation="es",       # traducir al español si es necesario
)

try:
    docs = loader.load()
    video_info = docs[0].metadata
    transcript = docs[0].page_content

    print("=== INFORMACIÓN DEL VÍDEO ===")
    print(f"Título:              {video_info.get('title', 'N/A')}")
    print(f"Autor:               {video_info.get('author', 'N/A')}")
    print(f"Duración:            {video_info.get('length', 'N/A')} segundos")
    print(f"Fecha publicación:   {video_info.get('publish_date', 'N/A')}")
    print(f"Vistas:              {video_info.get('view_count', 'N/A')}")

    print("\n=== ANÁLISIS DE TRANSCRIPCIÓN ===")
    print(f"Longitud: {len(transcript):,} caracteres")
    print(f"Palabras: {len(transcript.split()):,}")

    # Palabras más frecuentes (≥4 letras)
    words = re.findall(r"\b[a-záéíóúñ]{4,}\b", transcript.lower())
    common_words = Counter(words).most_common(10)
    print("\nPalabras más frecuentes:")
    for word, count in common_words:
        print(f"  {word}: {count} veces")

    print(f"\nPrimeros 500 caracteres de la transcripción:")
    print(transcript[:500] + "...")

except Exception as e:
    print(f"Error al cargar el vídeo: {e}")
