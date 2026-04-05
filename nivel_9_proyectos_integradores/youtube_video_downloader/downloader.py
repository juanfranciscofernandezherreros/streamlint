"""
downloader.py — Lógica de descarga de vídeos de YouTube con yt-dlp.

Proporciona funciones para validar URLs, obtener metadatos y
descargar vídeos o audio desde YouTube.
"""

import os
import re
from dataclasses import dataclass
from typing import Optional

import yt_dlp


# Patrón para validar URLs de YouTube
_YOUTUBE_REGEX = re.compile(
    r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)[\w-]+"
)


@dataclass
class VideoInfo:
    """Metadatos básicos de un vídeo de YouTube."""

    title: str
    duration: int  # segundos
    thumbnail: str
    uploader: str
    url: str


def is_valid_youtube_url(url: str) -> bool:
    """Comprueba si la URL corresponde a un vídeo de YouTube válido."""
    return bool(_YOUTUBE_REGEX.match(url.strip()))


def get_video_info(url: str) -> Optional[VideoInfo]:
    """Obtiene los metadatos de un vídeo sin descargarlo.

    Args:
        url: URL del vídeo de YouTube.

    Returns:
        VideoInfo con los metadatos o None si falla.
    """
    opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info is None:
                return None
            return VideoInfo(
                title=info.get("title", "Sin título"),
                duration=info.get("duration", 0),
                thumbnail=info.get("thumbnail", ""),
                uploader=info.get("uploader", "Desconocido"),
                url=url,
            )
    except yt_dlp.utils.DownloadError:
        return None


def download_video(
    url: str,
    output_dir: str = "descargas",
    format_id: str = "best",
    audio_only: bool = False,
    progress_hook: Optional[object] = None,
) -> Optional[str]:
    """Descarga un vídeo o audio de YouTube.

    Args:
        url: URL del vídeo.
        output_dir: Carpeta de destino.
        format_id: Formato de descarga (best, 720, 1080).
        audio_only: Si True, descarga solo audio MP3.
        progress_hook: Callable que recibe un dict con el progreso.

    Returns:
        Ruta del archivo descargado o None si falla.
    """
    os.makedirs(output_dir, exist_ok=True)
    outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")

    if audio_only:
        opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": outtmpl,
            "quiet": True,
            "no_warnings": True,
        }
    else:
        fmt = _resolve_format(format_id)
        opts = {
            "format": fmt,
            "outtmpl": outtmpl,
            "quiet": True,
            "no_warnings": True,
        }

    if progress_hook is not None:
        opts["progress_hooks"] = [progress_hook]

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                return None
            filename = ydl.prepare_filename(info)
            if audio_only:
                filename = os.path.splitext(filename)[0] + ".mp3"
            return filename
    except yt_dlp.utils.DownloadError:
        return None


def _resolve_format(format_id: str) -> str:
    """Convierte un identificador amigable a un selector de formato yt-dlp."""
    formats = {
        "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "720": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
        "1080": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
    }
    return formats.get(format_id, formats["best"])
