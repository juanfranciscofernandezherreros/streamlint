# Streamlint

Proyecto de aprendizaje práctico de **LangChain + LangGraph + OpenAI + Streamlit**, organizado en **10 niveles de dificultad** (de básico a proyectos integradores).

---

## 🎯 Objetivo del repositorio

Ruta progresiva para dominar el ecosistema LangChain:

1. Aprender fundamentos de prompts y cadenas.
2. Trabajar con salidas estructuradas y ejecución paralela.
3. Cargar documentos de múltiples fuentes.
4. Crear embeddings, vector stores y retrievers.
5. Diseñar workflows con **LangGraph** (grafos de estado).
6. Construir aplicaciones completas en Streamlit.
7. Implementar proyectos integradores reales (**RAG legal**, **Agente IA**, **HelpDesk** y **YouTube Downloader**).
8. Gestionar memoria conversacional y evaluar salidas de modelos de lenguaje.

---

## 🗂️ Estructura completa (ordenada por dificultad)

```text
streamlint/
├── README.md
├── requirements.txt
├── .env.example                               # Plantilla de variables de entorno
├── .gitignore
│
├── nivel_1_basico/                          # ⭐ Nivel 1 — Prompts y plantillas
│   ├── README.md
│   ├── 01_prompt_templates.py
│   ├── 02_chat_prompt_template.py
│   ├── 03_rol_prompt_templates.py
│   └── 04_message_placeholders.py
│
├── nivel_2_intermedio/                      # ⭐⭐ Nivel 2 — Salida estructurada
│   ├── README.md
│   ├── 05_output_parser.py
│   ├── 06_analisis_pydantic.py
│   └── 07_output_parser_parte2.py
│
├── nivel_3_avanzado/                        # ⭐⭐⭐ Nivel 3 — Ejecución paralela
│   ├── README.md
│   ├── 08_analisis_sentimientos.py
│   ├── 09_paralelo.py
│   └── 10_paralelo_batch.py
│
├── nivel_4_document_loaders/                # ⭐⭐⭐ Nivel 4 — Carga de documentos
│   ├── README.md
│   ├── 11_read_from_website.py
│   ├── 12_read_pdf.py
│   ├── 13_directory_loader.py
│   ├── 14_youtube_loader.py
│   ├── 15_unstructured_html_loader.py
│   ├── 16_csv_loader.py
│   ├── 17_selenium_url_loader.py
│   ├── 18_git_loader.py
│   └── 19_google_drive.py
│
├── nivel_5_text_splitters_y_embeddings/     # ⭐⭐⭐⭐ Nivel 5 — Procesamiento de texto
│   ├── README.md
│   ├── 20_text_splitters_parte1.py
│   ├── 21_text_splitters_parte2.py
│   └── 22_embeding_language.py
│
├── nivel_6_retrievers/                      # ⭐⭐⭐⭐ Nivel 6 — Recuperación de información
│   ├── README.md
│   ├── 23_vector_stores.py
│   ├── 24_retriever_langchain.py
│   ├── 25_multi_query_retriever.py
│   ├── 26_contextual_compression_retriever.py
│   ├── 27_ensemble_retriever.py
│   ├── 28_parent_document_retriever.py
│   ├── 29_self_query_retriever.py
│   ├── 30_time_weighted_retriever.py
│   └── 31_advanced_retrievers.py
│
├── nivel_7_langgraph/                       # ⭐⭐⭐⭐⭐ Nivel 7 — Grafos de estado
│   ├── README.md
│   ├── 32_primer_programa_langgraph.py
│   ├── 33_procesador_reuniones.py
│   ├── 34_control_flujo_langgraph.py
│   ├── 35_procesador_reuniones_langgraph.py
│   ├── 36_langgraph_condicional.py
│   └── 37_langgraph_checkpointer.py
│
├── nivel_8_aplicaciones/                    # ⭐⭐⭐⭐⭐ Nivel 8 — Apps con Streamlit
│   ├── README.md
│   ├── 38_all_exercise.py
│   ├── 39_streamlit_chatbox.py
│   └── 40_streamlit_quiz_exam.py
│
├── nivel_9_proyectos_integradores/          # ⭐⭐⭐⭐⭐ Nivel 9 — Proyectos completos
│   ├── README.md
│   ├── asistente_legal/
│   │   ├── README.md
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── ingest.py
│   │   ├── prompt.py
│   │   └── rag_system.py
│   ├── agente_ia/
│   │   ├── README.md
│   │   ├── agent.py
│   │   ├── ask_agent.py
│   │   ├── tools.py
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── requirements.txt
│   │   ├── docs/
│   │   └── tests/
│   ├── helpdesk_system/
│   │   ├── README.md
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── graph.py
│   │   ├── rag_system.py
│   │   ├── setup_rag.py
│   │   └── docs/
│   ├── dif_system/
│   │   ├── README.md
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── setup_rag.py
│   │   └── docs/
│   │       └── enero.json
│   └── youtube_video_downloader/
│       ├── README.md
│       ├── app.py
│       ├── downloader.py
│       └── requirements.txt
│
├── nivel_10_memoria_y_evaluacion/           # ⭐⭐⭐⭐⭐⭐ Nivel 10 — Calidad y persistencia
│   ├── README.md
│   ├── 41_conversacion_con_memoria.py
│   └── 42_evaluacion_llm.py
│
└── datos/                                   # 📁 Recursos y datos de ejemplo
    ├── README.md
    ├── contratos/              # PDFs de contratos para RAG/retrievers
    ├── sesiones/               # Conversaciones persistidas en JSON
    ├── historial_chat.json     # Historial de ejemplo
    ├── cambridge_english_first.pdf
    └── Simulacion_reunion.mp4
```

---

## 🧭 Ruta de aprendizaje completa (01 → 42 + proyectos)

### Nivel 1 — Básico (01–04): Prompts y plantillas

Introducción a `PromptTemplate`, `ChatPromptTemplate`, roles y placeholders.

| # | Archivo | Descripción |
|---|---------|-------------|
| 01 | `01_prompt_templates.py` | Plantillas básicas con `PromptTemplate` |
| 02 | `02_chat_prompt_template.py` | Plantillas de chat con `ChatPromptTemplate` |
| 03 | `03_rol_prompt_templates.py` | Templates con roles (system, human, AI) |
| 04 | `04_message_placeholders.py` | Uso de `MessagesPlaceholder` |

### Nivel 2 — Intermedio (05–07): Salida estructurada

Parseo de salidas con `OutputParser` y validación con Pydantic.

| # | Archivo | Descripción |
|---|---------|-------------|
| 05 | `05_output_parser.py` | Parseo de salidas de LLM |
| 06 | `06_analisis_pydantic.py` | Validación con modelos Pydantic |
| 07 | `07_output_parser_parte2.py` | Output parsers avanzados |

### Nivel 3 — Avanzado (08–10): Ejecución paralela

`RunnableParallel`, procesamiento por lotes y análisis de sentimientos.

| # | Archivo | Descripción |
|---|---------|-------------|
| 08 | `08_analisis_sentimientos.py` | Análisis de sentimientos con LLM |
| 09 | `09_paralelo.py` | Ejecución paralela con `RunnableParallel` |
| 10 | `10_paralelo_batch.py` | Procesamiento por lotes |

### Nivel 4 — Document Loaders (11–19): Carga de documentos

Loaders para web, PDF, carpetas, YouTube, HTML, CSV, Selenium, Git y Google Drive.

| # | Archivo | Descripción |
|---|---------|-------------|
| 11 | `11_read_from_website.py` | WebBaseLoader — cargar contenido web |
| 12 | `12_read_pdf.py` | PyPDFLoader — leer PDFs |
| 13 | `13_directory_loader.py` | DirectoryLoader — cargar carpetas |
| 14 | `14_youtube_loader.py` | YoutubeLoader — transcripciones de YouTube |
| 15 | `15_unstructured_html_loader.py` | UnstructuredHTMLLoader |
| 16 | `16_csv_loader.py` | CSVLoader — archivos CSV |
| 17 | `17_selenium_url_loader.py` | SeleniumURLLoader — sitios dinámicos |
| 18 | `18_git_loader.py` | GitLoader — repositorios Git |
| 19 | `19_google_drive.py` | GoogleDriveLoader |

### Nivel 5 — Text Splitters y Embeddings (20–22): Procesamiento de texto

Estrategias de splitting y generación de embeddings con modelos de lenguaje.

| # | Archivo | Descripción |
|---|---------|-------------|
| 20 | `20_text_splitters_parte1.py` | Splitting básico de textos |
| 21 | `21_text_splitters_parte2.py` | Splitting avanzado (recursive, semantic) |
| 22 | `22_embeding_language.py` | Embeddings con OpenAI y similitud coseno |

### Nivel 6 — Retrievers (23–31): Recuperación de información

Vector stores, multi-query, compresión contextual, ensemble, parent document, self-query, time-weighted y MMR.

| # | Archivo | Descripción |
|---|---------|-------------|
| 23 | `23_vector_stores.py` | Vector stores con FAISS |
| 24 | `24_retriever_langchain.py` | Retriever básico de LangChain |
| 25 | `25_multi_query_retriever.py` | MultiQueryRetriever |
| 26 | `26_contextual_compression_retriever.py` | ContextualCompressionRetriever |
| 27 | `27_ensemble_retriever.py` | EnsembleRetriever (FAISS + BM25) |
| 28 | `28_parent_document_retriever.py` | ParentDocumentRetriever |
| 29 | `29_self_query_retriever.py` | SelfQueryRetriever |
| 30 | `30_time_weighted_retriever.py` | TimeWeightedVectorStoreRetriever |
| 31 | `31_advanced_retrievers.py` | Retrievers avanzados y combinados |

### Nivel 7 — LangGraph (32–37): Grafos de estado

| # | Archivo | Descripción |
|---|---------|-------------|
| 32 | `32_primer_programa_langgraph.py` | Primer grafo de estado (`StateGraph`) con nodos secuenciales |
| 33 | `33_procesador_reuniones.py` | Workflow: transcripción Whisper, extracción de participantes/temas/acciones, minutas |
| 34 | `34_control_flujo_langgraph.py` | Control de flujo condicional con `StateGraph` |
| 35 | `35_procesador_reuniones_langgraph.py` | Procesador de reuniones con interfaz gráfica (tkinter) |
| 36 | `36_langgraph_condicional.py` | Edges condicionales: clasificación de sentimiento con routing a ramas especializadas |
| 37 | `37_langgraph_checkpointer.py` | Persistencia de estado con `MemorySaver`; conversación multi-turno |

### Nivel 8 — Aplicaciones (38–40): Apps con Streamlit

| # | Archivo | Descripción |
|---|---------|-------------|
| 38 | `38_all_exercise.py` | Aplicación que integra todos los ejercicios del curso |
| 39 | `39_streamlit_chatbox.py` | Chatbot completo con interfaz Streamlit y persistencia de sesiones |
| 40 | `40_streamlit_quiz_exam.py` | Examen tipo test con radio buttons, puntuación y revisión |

### Nivel 9 — Proyectos integradores: Sistemas completos

#### 🔹 `asistente_legal/` — RAG legal

Proyecto RAG completo con ingesta de contratos PDF a FAISS, cadena de recuperación y generación, e interfaz de chat en Streamlit.

| Archivo | Descripción |
|---------|-------------|
| `ingest.py` | Ingesta de PDFs y creación del índice FAISS |
| `rag_system.py` | Cadena RAG con MultiQueryRetriever |
| `app.py` | Interfaz de chat Streamlit |
| `config.py` | Configuración del proyecto |
| `prompt.py` | Templates de prompts legales |

#### 🔹 `agente_ia/` — Agente conversacional con herramientas

Agente inteligente con LangChain que busca en internet (DuckDuckGo), resuelve cálculos, ejecuta código Python y selecciona herramientas automáticamente. Incluye Docker, tests y documentación.

| Archivo | Descripción |
|---------|-------------|
| `agent.py` | Agente principal con selección de herramientas |
| `ask_agent.py` | CLI para consultas batch |
| `tools.py` | Herramientas personalizadas (búsqueda, cálculo, código) |
| `Dockerfile` | Contenedor Docker |
| `tests/` | Tests unitarios del agente |

#### 🔹 `helpdesk_system/` — Sistema de soporte HelpDesk

Sistema de soporte técnico con LangGraph que gestiona tickets, clasifica consultas y responde usando RAG sobre documentación interna.

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Interfaz principal Streamlit |
| `graph.py` | Grafo LangGraph para workflow de soporte |
| `rag_system.py` | Sistema RAG sobre documentación |
| `setup_rag.py` | Configuración e ingesta de docs |
| `config.py` | Configuración del sistema |
| `docs/` | Documentación interna (FAQ, manual, guía) |

#### 🔹 `youtube_video_downloader/` — Descargador de vídeos YouTube

Aplicación Streamlit para descargar vídeos y audio de YouTube con yt-dlp. Soporta múltiples resoluciones, descarga solo audio MP3 y muestra progreso en tiempo real.

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Interfaz Streamlit con progreso de descarga |
| `downloader.py` | Motor de descarga con yt-dlp |
| `requirements.txt` | Dependencias del proyecto |
| `README.md` | Documentación detallada |

### Nivel 10 — Memoria y Evaluación (41–42): Calidad y persistencia

| # | Archivo | Descripción |
|---|---------|-------------|
| 41 | `41_conversacion_con_memoria.py` | Tres tipos de memoria: `Buffer`, `BufferWindow` y `SummaryMemory` |
| 42 | `42_evaluacion_llm.py` | Evaluación con `CriteriaEvalChain`, `QAEvalChain` y criterios personalizados |

---

## 🛠️ Tecnologías y dependencias

### Núcleo

| Paquete | Uso |
|---------|-----|
| **Python 3.10+** | Recomendado 3.12 |
| **LangChain** | Framework principal |
| **LangChain OpenAI** | Integración con GPT |
| **LangChain Community** | Loaders y herramientas |
| **LangGraph** | Grafos de estado |
| **OpenAI API** | LLM y embeddings |
| **Streamlit** | Interfaces web |
| **Pydantic** | Validación de datos |

### Utilidades

| Paquete | Uso |
|---------|-----|
| `python-dotenv` | Variables de entorno |
| `numpy` | Similitud coseno |
| `beautifulsoup4` | Parsing HTML |
| `pypdf` | Lectura de PDFs |
| `faiss-cpu` | Vector store local |
| `rank_bm25` | BM25Retriever |
| `duckduckgo-search` | Búsqueda web (Agente IA) |
| `yt-dlp` | Descarga de vídeos YouTube |

### Opcionales (según módulo)

```bash
pip install unstructured          # DirectoryLoader / UnstructuredHTMLLoader (13, 15)
pip install youtube-transcript-api # YoutubeLoader (14)
pip install selenium               # SeleniumURLLoader (17)
pip install gitpython              # GitLoader (18)
pip install langchain-google-community google-auth-oauthlib google-api-python-client  # GoogleDriveLoader (19)
```

---

## ⚙️ Requisitos previos

| Requisito | Versión mínima | Notas |
|-----------|----------------|-------|
| **Python** | 3.10+ | Recomendado 3.12 |
| **pip** | 21+ | Para instalar dependencias |
| **ffmpeg** | cualquiera | Solo para YouTube Video Downloader |
| **API Key de OpenAI** | — | Obligatoria para todos los scripts |

---

## ⚙️ Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/juanfranciscofernandezherreros/streamlint.git
cd streamlint

# 2. Crear y activar entorno virtual
python3 -m venv env
source env/bin/activate   # Linux/macOS
# .\env\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. (Opcional) Instalar dependencias de módulos específicos
pip install unstructured          # DirectoryLoader / UnstructuredHTMLLoader (13, 15)
pip install youtube-transcript-api # YoutubeLoader (14)
pip install selenium               # SeleniumURLLoader (17)
pip install gitpython              # GitLoader (18)
pip install langchain-google-community google-auth-oauthlib google-api-python-client  # GoogleDriveLoader (19)
```

---

## 🔐 Configuración de la API Key de OpenAI

### Opción 1 — Archivo `.env` (recomendado)

```bash
# Copiar la plantilla y rellenar tu clave
cp .env.example .env
```

Edita el archivo `.env` y añade tu clave:

```env
OPENAI_API_KEY=sk-...
```

### Opción 2 — Variable de entorno

```bash
export OPENAI_API_KEY="sk-..."    # Linux/macOS
set OPENAI_API_KEY=sk-...         # Windows CMD
$env:OPENAI_API_KEY="sk-..."      # Windows PowerShell
```

> **Nota:** En las aplicaciones Streamlit (nivel 8) también puedes introducir la clave desde la barra lateral.

---

## ▶️ Ejecución

> **Importante:** Todos los scripts deben ejecutarse desde la raíz del proyecto (`streamlint/`).

### Scripts de niveles 1–6 (01–31): Fundamentos de LangChain

```bash
# Nivel 1 — Prompts y plantillas
python nivel_1_basico/01_prompt_templates.py
python nivel_1_basico/02_chat_prompt_template.py
python nivel_1_basico/03_rol_prompt_templates.py
python nivel_1_basico/04_message_placeholders.py

# Nivel 2 — Salida estructurada
python nivel_2_intermedio/05_output_parser.py
python nivel_2_intermedio/06_analisis_pydantic.py
python nivel_2_intermedio/07_output_parser_parte2.py

# Nivel 3 — Ejecución paralela
python nivel_3_avanzado/08_analisis_sentimientos.py
python nivel_3_avanzado/09_paralelo.py
python nivel_3_avanzado/10_paralelo_batch.py

# Nivel 4 — Document Loaders
python nivel_4_document_loaders/11_read_from_website.py
python nivel_4_document_loaders/12_read_pdf.py
python nivel_4_document_loaders/13_directory_loader.py
python nivel_4_document_loaders/14_youtube_loader.py
python nivel_4_document_loaders/15_unstructured_html_loader.py
python nivel_4_document_loaders/16_csv_loader.py
python nivel_4_document_loaders/17_selenium_url_loader.py
python nivel_4_document_loaders/18_git_loader.py
python nivel_4_document_loaders/19_google_drive.py

# Nivel 5 — Text Splitters y Embeddings
python nivel_5_text_splitters_y_embeddings/20_text_splitters_parte1.py
python nivel_5_text_splitters_y_embeddings/21_text_splitters_parte2.py
python nivel_5_text_splitters_y_embeddings/22_embeding_language.py

# Nivel 6 — Retrievers (requieren datos en datos/contratos/ o FAISS index previo)
python nivel_6_retrievers/23_vector_stores.py         # Crea el índice FAISS
python nivel_6_retrievers/24_retriever_langchain.py    # Requiere índice FAISS previo
python nivel_6_retrievers/25_multi_query_retriever.py
python nivel_6_retrievers/26_contextual_compression_retriever.py
python nivel_6_retrievers/27_ensemble_retriever.py
python nivel_6_retrievers/28_parent_document_retriever.py
python nivel_6_retrievers/29_self_query_retriever.py
python nivel_6_retrievers/30_time_weighted_retriever.py
python nivel_6_retrievers/31_advanced_retrievers.py
```

### Scripts LangGraph — Nivel 7 (32–37)

```bash
python nivel_7_langgraph/32_primer_programa_langgraph.py
python nivel_7_langgraph/33_procesador_reuniones.py          # Requiere datos/Simulacion_reunion.mp4
python nivel_7_langgraph/34_control_flujo_langgraph.py
python nivel_7_langgraph/35_procesador_reuniones_langgraph.py # Interfaz gráfica con tkinter
python nivel_7_langgraph/36_langgraph_condicional.py
python nivel_7_langgraph/37_langgraph_checkpointer.py
```

### Apps Streamlit — Nivel 8 (38–40)

```bash
streamlit run nivel_8_aplicaciones/38_all_exercise.py        # Todos los ejercicios integrados
streamlit run nivel_8_aplicaciones/39_streamlit_chatbox.py   # Chatbot con persistencia
streamlit run nivel_8_aplicaciones/40_streamlit_quiz_exam.py # Examen tipo test
```

### Memoria y Evaluación — Nivel 10 (41–42)

```bash
python nivel_10_memoria_y_evaluacion/41_conversacion_con_memoria.py
python nivel_10_memoria_y_evaluacion/42_evaluacion_llm.py
```

### Proyecto RAG Legal (nivel 9)

```bash
# 1. Primero indexar los contratos (solo la primera vez)
python nivel_9_proyectos_integradores/asistente_legal/ingest.py

# 2. Lanzar la interfaz de chat
streamlit run nivel_9_proyectos_integradores/asistente_legal/app.py
```

### Proyecto Agente IA (nivel 9)

```bash
cd nivel_9_proyectos_integradores/agente_ia

# Modo interactivo (chat en terminal)
python agent.py

# Modo batch (procesar varias preguntas de golpe)
python agent.py --questions "¿Cuánto es 2+2?" "¿Qué día es hoy?"

# Con Docker
docker compose run --rm agente-ia
```

### Proyecto HelpDesk (nivel 9)

```bash
# 1. Indexar la documentación de soporte (solo la primera vez)
python nivel_9_proyectos_integradores/helpdesk_system/setup_rag.py

# 2. Lanzar la interfaz de soporte
streamlit run nivel_9_proyectos_integradores/helpdesk_system/app.py
```

### Proyecto YouTube Video Downloader (nivel 9)

```bash
# Requiere ffmpeg instalado en el sistema
# Linux: sudo apt install ffmpeg
# macOS: brew install ffmpeg
# Windows: descargar desde https://ffmpeg.org

streamlit run nivel_9_proyectos_integradores/youtube_video_downloader/app.py
```

### Proyecto DIF System — Asistente de Gimnasio (nivel 9)

```bash
# 1. Indexar el plan maestro de entrenamiento (solo la primera vez)
python nivel_9_proyectos_integradores/dif_system/setup_rag.py

# 2. Lanzar el asistente de horarios
streamlit run nivel_9_proyectos_integradores/dif_system/app.py
```

Preguntas de ejemplo que puede responder:

- ¿Qué clases hay el 21 de enero?
- ¿Qué actividad hay en la Sala A el 3 de enero?
- ¿Qué días hay GAP en enero?
- ¿Cuándo hay DEKA-DIF?
- ¿Qué es Strong?
- ¿Cuánto dura Power Play?
- ¿Qué significa GAP?
- ¿Qué horario tiene DIF Senior?
- ¿Cuándo hay fútbol?
- ¿Hay Pilates entre semana?
- ¿Qué talleres hay en enero?
- ¿Está abierto el gimnasio el 1 de enero?

---

## 📁 Carpeta `datos/`

Recursos y datos de ejemplo utilizados por los scripts:

| Archivo/Carpeta | Descripción |
|-----------------|-------------|
| `contratos/` | PDFs de contratos de arrendamiento para ejemplos RAG |
| `sesiones/` | Sesiones de chat persistidas en JSON |
| `historial_chat.json` | Historial de conversación de ejemplo |
| `cambridge_english_first.pdf` | PDF de ejemplo para document loaders |
| `Simulacion_reunion.mp4` | Vídeo de ejemplo para procesador de reuniones |

---

## 📌 Notas de organización

- La secuencia oficial de aprendizaje es **01 → 42**, seguida de los proyectos integradores.
- Los niveles 1–6 cubren fundamentos de LangChain puro.
- El nivel 7 introduce **LangGraph** (grafos de estado, workflows y checkpointers).
- El nivel 8 agrupa las aplicaciones completas con **Streamlit**.
- El nivel 9 contiene **4 proyectos integradores** independientes y completos.
- El nivel 10 cubre **memoria conversacional** y **evaluación de LLMs**.
- Los datos y recursos de ejemplo están centralizados en la carpeta `datos/`.
- El archivo `22_embeding_language.py` conserva ese nombre por compatibilidad histórica.
- Todas las rutas se calculan dinámicamente a partir de la ubicación de cada script.

---

## 🔧 Solución de problemas

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: No module named 'langchain_openai'` | Ejecuta `pip install -r requirements.txt` |
| `openai.AuthenticationError` | Revisa que `OPENAI_API_KEY` esté configurada en `.env` o como variable de entorno |
| `FileNotFoundError` en scripts del nivel 6 | Ejecuta primero `23_vector_stores.py` para crear el índice FAISS, y asegúrate de tener PDFs en `datos/contratos/` |
| `ffmpeg not found` en YouTube Downloader | Instala ffmpeg: `sudo apt install ffmpeg` (Linux) / `brew install ffmpeg` (macOS) |
| Error en `helpdesk_system` | Ejecuta primero `setup_rag.py` para indexar la documentación |
| Error en `asistente_legal` | Ejecuta primero `ingest.py` para crear el índice FAISS |

---

## ✅ Resumen

Este repositorio está organizado en **10 niveles de dificultad creciente**:

| Nivel | Contenido | Scripts |
|-------|-----------|---------|
| 1 | Prompts y plantillas | 01–04 |
| 2 | Salida estructurada | 05–07 |
| 3 | Ejecución paralela | 08–10 |
| 4 | Document Loaders | 11–19 |
| 5 | Text Splitters y Embeddings | 20–22 |
| 6 | Retrievers | 23–31 |
| 7 | LangGraph | 32–37 |
| 8 | Aplicaciones Streamlit | 38–40 |
| 9 | Proyectos integradores | Asistente Legal, Agente IA, HelpDesk, YouTube Downloader |
| 10 | Memoria y Evaluación | 41–42 |

Todo el stack, dependencias y formas de ejecución están centralizados en este README.
