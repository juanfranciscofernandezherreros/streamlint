"""
YouTube Video Downloader — Interfaz Streamlit.

Aplicación web para descargar vídeos y audio de YouTube con
opciones de formato y resolución.

Ejecución:
    streamlit run nivel_9_proyectos_integradores/youtube_video_downloader/app.py
"""

import streamlit as st

from downloader import download_video, get_video_info, is_valid_youtube_url

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="YouTube Downloader", page_icon="📺", layout="centered")
st.title("📺 YouTube Video Downloader")
st.markdown("Descarga vídeos y audio de YouTube de forma sencilla.")

# ── Inicializar estado de sesión ─────────────────────────────────────────────
if "historial" not in st.session_state:
    st.session_state.historial = []

# ── Entrada de URL ───────────────────────────────────────────────────────────
url = st.text_input("🔗 Pega la URL de YouTube:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if not is_valid_youtube_url(url):
        st.error("❌ La URL no parece ser un enlace válido de YouTube.")
    else:
        with st.spinner("Obteniendo información del vídeo…"):
            info = get_video_info(url)

        if info is None:
            st.error("❌ No se pudo obtener información del vídeo. Verifica la URL.")
        else:
            # ── Mostrar metadatos ────────────────────────────────────────────
            col1, col2 = st.columns([1, 2])
            with col1:
                if info.thumbnail:
                    st.image(info.thumbnail, use_container_width=True)
            with col2:
                st.subheader(info.title)
                mins, secs = divmod(info.duration, 60)
                st.write(f"**Canal:** {info.uploader}")
                st.write(f"**Duración:** {mins}:{secs:02d}")

            # ── Opciones de descarga ─────────────────────────────────────────
            st.divider()
            col_fmt, col_type = st.columns(2)

            with col_type:
                modo = st.radio("Tipo de descarga:", ["🎬 Vídeo", "🎵 Solo audio (MP3)"])
                audio_only = modo == "🎵 Solo audio (MP3)"

            with col_fmt:
                if audio_only:
                    st.info("Se descargará en formato MP3 a 192 kbps.")
                    format_id = "best"
                else:
                    format_id = st.selectbox(
                        "Resolución:",
                        options=["best", "1080", "720"],
                        format_func=lambda x: {"best": "Mejor disponible", "1080": "1080p", "720": "720p"}[x],
                    )

            # ── Botón de descarga ────────────────────────────────────────────
            if st.button("⬇️ Descargar", type="primary", use_container_width=True):
                progress_bar = st.progress(0, text="Iniciando descarga…")

                def _progress_hook(d):
                    if d.get("status") == "downloading":
                        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                        downloaded = d.get("downloaded_bytes", 0)
                        if total > 0:
                            pct = min(downloaded / total, 1.0)
                            progress_bar.progress(pct, text=f"Descargando… {pct:.0%}")
                    elif d.get("status") == "finished":
                        progress_bar.progress(1.0, text="Procesando…")

                filepath = download_video(
                    url=url,
                    format_id=format_id,
                    audio_only=audio_only,
                    progress_hook=_progress_hook,
                )

                if filepath:
                    progress_bar.progress(1.0, text="✅ ¡Descarga completada!")
                    st.success(f"Archivo guardado en: `{filepath}`")
                    st.session_state.historial.append(
                        {"titulo": info.title, "archivo": filepath}
                    )
                else:
                    progress_bar.empty()
                    st.error("❌ Error durante la descarga. Intenta de nuevo.")

# ── Historial de descargas ───────────────────────────────────────────────────
if st.session_state.historial:
    st.divider()
    st.subheader("📋 Historial de descargas")
    for i, item in enumerate(reversed(st.session_state.historial), 1):
        st.write(f"{i}. **{item['titulo']}** → `{item['archivo']}`")
