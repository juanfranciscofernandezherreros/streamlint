# YouTube Video Downloader

Aplicación web con **Streamlit** para descargar vídeos y audio de YouTube usando **yt-dlp**.

## Funcionalidades

- Descargar vídeo en múltiples resoluciones (720p, 1080p, mejor disponible).
- Descargar solo audio en formato MP3.
- Interfaz intuitiva con barra de progreso.
- Validación de URLs de YouTube.
- Historial de descargas en la sesión.

## Requisitos

```bash
pip install -r requirements.txt
```

También necesitas **ffmpeg** instalado en tu sistema:

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows (con chocolatey)
choco install ffmpeg
```

## Ejecución

```bash
streamlit run app.py
```

## Estructura

```
youtube_video_downloader/
├── app.py              # Interfaz Streamlit
├── downloader.py       # Lógica de descarga con yt-dlp
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación
```

## Tecnologías

- **Streamlit** — Interfaz web.
- **yt-dlp** — Motor de descarga de vídeos.
- **ffmpeg** — Conversión y procesamiento de audio/vídeo.
