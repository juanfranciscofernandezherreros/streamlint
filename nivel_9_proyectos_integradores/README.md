# ⭐⭐⭐⭐⭐ Nivel 9 — Proyectos Integradores

**5 proyectos completos** que combinan todas las técnicas aprendidas en los niveles anteriores: RAG, agentes, LangGraph, Streamlit y más.

## Proyectos

| Proyecto | Descripción | Tecnologías principales |
|----------|-------------|------------------------|
| [**asistente_legal/**](asistente_legal/) | Asistente RAG para consulta de contratos legales | FAISS, MultiQueryRetriever, Streamlit |
| [**agente_ia/**](agente_ia/) | Agente conversacional con selección automática de herramientas | LangChain Agents, DuckDuckGo, Docker |
| [**helpdesk_system/**](helpdesk_system/) | Sistema de soporte técnico con routing inteligente | LangGraph, RAG, Streamlit |
| [**dif_system/**](dif_system/) | Asistente de horarios de gimnasio | RAG, FAISS, Streamlit |
| [**youtube_video_downloader/**](youtube_video_downloader/) | Descargador de vídeos y audio de YouTube | Streamlit, yt-dlp, ffmpeg |

## Asistente Legal

Sistema RAG completo para consulta de contratos de arrendamiento. Ingesta PDFs a un índice FAISS, utiliza MultiQueryRetriever para mejorar la recuperación y ofrece una interfaz de chat con Streamlit.

```bash
python nivel_9_proyectos_integradores/asistente_legal/ingest.py
streamlit run nivel_9_proyectos_integradores/asistente_legal/app.py
```

## Agente IA

Agente inteligente que selecciona automáticamente entre herramientas (búsqueda web, calculadora, ejecución de código, fecha/hora). Incluye Docker, tests unitarios y documentación completa.

```bash
cd nivel_9_proyectos_integradores/agente_ia
python agent.py
```

## HelpDesk System

Sistema de soporte técnico con LangGraph que clasifica tickets, los enruta al departamento correcto y responde usando RAG sobre documentación interna (FAQ, manual de usuario, guía de resolución).

```bash
python nivel_9_proyectos_integradores/helpdesk_system/setup_rag.py
streamlit run nivel_9_proyectos_integradores/helpdesk_system/app.py
```

## DIF System — Asistente de Gimnasio

Asistente para consultas de horarios de actividades de gimnasio. Usa RAG sobre un plan de clases en JSON.

```bash
python nivel_9_proyectos_integradores/dif_system/setup_rag.py
streamlit run nivel_9_proyectos_integradores/dif_system/app.py
```

## YouTube Video Downloader

Aplicación web con Streamlit para descargar vídeos y audio de YouTube con yt-dlp. Soporta múltiples resoluciones y descarga de audio MP3.

```bash
streamlit run nivel_9_proyectos_integradores/youtube_video_downloader/app.py
```

## Navegación

⬅️ [Nivel 8 — Aplicaciones](../nivel_8_aplicaciones/) · ➡️ [Nivel 10 — Memoria y Evaluación](../nivel_10_memoria_y_evaluacion/)
