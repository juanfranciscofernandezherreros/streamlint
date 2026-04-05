# Streamlint

Proyecto de aprendizaje práctico de **LangChain + LangGraph + OpenAI + Streamlit**, organizado en **10 niveles de dificultad** (de básico a proyectos integradores).

---

## 🎯 Objetivo del repositorio

Este repositorio está organizado como una ruta progresiva para:

1. Aprender fundamentos de prompts y cadenas.
2. Trabajar con salidas estructuradas y ejecución paralela.
3. Cargar documentos de múltiples fuentes.
4. Crear embeddings, vector stores y retrievers.
5. Diseñar workflows con **LangGraph** (grafos de estado).
6. Construir aplicaciones completas en Streamlit.
7. Implementar proyectos integradores reales (**RAG legal** y **Agente IA con herramientas**).
8. Gestionar memoria conversacional y evaluar salidas de modelos de lenguaje.

---

## 🗂️ Estructura completa (ordenada por dificultad)

```text
streamlint/
├── README.md
├── requirements.txt
├── .gitignore
│
├── nivel_1_basico/                          # ⭐ Dificultad 1
│   ├── 01_prompt_templates.py
│   ├── 02_chat_prompt_template.py
│   ├── 03_rol_prompt_templates.py
│   └── 04_message_placeholders.py
│
├── nivel_2_intermedio/                      # ⭐⭐ Dificultad 2
│   ├── 05_output_parser.py
│   ├── 06_analisis_pydantic.py
│   └── 07_output_parser_parte2.py
│
├── nivel_3_avanzado/                        # ⭐⭐⭐ Dificultad 3
│   ├── 08_analisis_sentimientos.py
│   ├── 09_paralelo.py
│   └── 10_paralelo_batch.py
│
├── nivel_4_document_loaders/                # ⭐⭐⭐ Dificultad 4
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
├── nivel_5_text_splitters_y_embeddings/     # ⭐⭐⭐⭐ Dificultad 5
│   ├── 20_text_splitters_parte1.py
│   ├── 21_text_splitters_parte2.py
│   └── 22_embeding_language.py
│
├── nivel_6_retrievers/                      # ⭐⭐⭐⭐ Dificultad 6
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
├── nivel_7_langgraph/                       # ⭐⭐⭐⭐⭐ Dificultad 7
│   ├── 32_primer_programa_langgraph.py
│   ├── 33_procesador_reuniones.py
│   ├── 36_langgraph_condicional.py
│   └── 37_langgraph_checkpointer.py
│
├── nivel_8_aplicaciones/                    # ⭐⭐⭐⭐⭐ Dificultad 8
│   ├── 34_all_exercise.py
│   ├── 35_streamlit_chatbox.py
│   └── 40_streamlit_quiz_exam.py
│
├── nivel_9_proyectos_integradores/          # ⭐⭐⭐⭐⭐ Dificultad 9
│   ├── asistente_legal/
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── ingest.py
│   │   ├── prompt.py
│   │   └── rag_system.py
│   └── agente_ia/
│       ├── agent.py
│       ├── ask_agent.py
│       ├── tools.py
│       ├── Dockerfile
│       ├── docker-compose.yml
│       ├── requirements.txt
│       ├── docs/
│       └── tests/
│
├── nivel_10_memoria_y_evaluacion/           # ⭐⭐⭐⭐⭐⭐ Dificultad 10
│   ├── 38_conversacion_con_memoria.py
│   └── 39_evaluacion_llm.py
│
├── contratos/                # PDFs de contratos para ejemplos RAG/retrievers
├── sesiones/                 # Conversaciones persistidas en JSON
├── faiss_db/                 # Base vectorial local (FAISS)
├── historial_chat.json       # Historial de ejemplo
└── cambridge_english_first.pdf
```

---

## 🧭 Ruta de aprendizaje completa (01 → 40 + proyectos)

### Nivel 1 — Básico (01–04): Prompts y plantillas

Introducción a `PromptTemplate`, `ChatPromptTemplate`, roles y placeholders.

### Nivel 2 — Intermedio (05–07): Salida estructurada

Parseo de salidas con `OutputParser` y validación con Pydantic.

### Nivel 3 — Avanzado (08–10): Ejecución paralela

`RunnableParallel`, procesamiento por lotes y análisis de sentimientos.

### Nivel 4 — Document Loaders (11–19): Carga de documentos

Loaders para web, PDF, carpetas, YouTube, HTML, CSV, Selenium, Git y Google Drive.

### Nivel 5 — Text Splitters y Embeddings (20–22): Procesamiento de texto

Estrategias de splitting y generación de embeddings con modelos de lenguaje.

### Nivel 6 — Retrievers (23–31): Recuperación de información

Vector stores, multi-query, compresión contextual, ensemble, parent document, self-query, time-weighted y MMR.

### Nivel 7 — LangGraph (32–33, 36–37): Grafos de estado

- `32_primer_programa_langgraph.py` — Primer grafo de estado (StateGraph) con nodos secuenciales.
- `33_procesador_reuniones.py` — Workflow completo: transcripción con Whisper, extracción de participantes/temas/acciones y generación de minutas.
- `36_langgraph_condicional.py` — Edges condicionales avanzados: clasificación de sentimiento con routing a tres ramas especializadas.
- `37_langgraph_checkpointer.py` — Persistencia de estado entre turnos con `MemorySaver`; conversación multi-turno sin gestionar el historial manualmente.

### Nivel 8 — Aplicaciones (34–35, 40): Apps con Streamlit

- `34_all_exercise.py` — Aplicación que integra todos los ejercicios del curso.
- `35_streamlit_chatbox.py` — Chatbot completo con interfaz Streamlit.
- `40_streamlit_quiz_exam.py` — Examen tipo test con radio buttons, puntuación y revisión de respuestas.

### Nivel 9 — Proyectos integradores: Sistemas completos

#### `asistente_legal/` — RAG legal

Proyecto RAG completo con ingesta de contratos PDF a FAISS, cadena de recuperación y generación, e interfaz de chat en Streamlit.

#### `agente_ia/` — Agente conversacional con herramientas

Agente inteligente con LangChain que busca en internet (DuckDuckGo), resuelve cálculos, ejecuta código Python y selecciona herramientas automáticamente. Incluye Docker, tests y documentación.

### Nivel 10 — Memoria y Evaluación (38–39): Calidad y persistencia

- `38_conversacion_con_memoria.py` — Los tres tipos principales de memoria conversacional: `ConversationBufferMemory` (historial completo), `ConversationBufferWindowMemory` (ventana deslizante) y `ConversationSummaryMemory` (resumen automático con LLM).
- `39_evaluacion_llm.py` — Evaluación de salidas de modelos con `CriteriaEvalChain` (criterios estándar), `QAEvalChain` (comparación con ground truth) y criterios personalizados.

---

## 🛠️ Todo lo que usa el proyecto

### Núcleo

- **Python 3.10+** (recomendado 3.12)
- **LangChain** + **LangChain OpenAI** + **LangChain Community**
- **LangGraph**
- **OpenAI API**
- **Streamlit**
- **Pydantic**

### Utilidades y procesamiento

- `python-dotenv`
- `numpy`
- `langchain-text-splitters`
- `beautifulsoup4`
- `pypdf`

### Tecnologías usadas en módulos específicos (instalación según uso)

- `unstructured` (DirectoryLoader / UnstructuredHTMLLoader)
- `youtube-transcript-api` (YoutubeLoader)
- `selenium` + ChromeDriver (SeleniumURLLoader)
- `gitpython` (GitLoader)
- `langchain-google-community`, `google-auth-oauthlib`, `google-api-python-client` (GoogleDriveLoader)
- `faiss-cpu` (FAISS — persistencia vectorial)
- `rank_bm25` (BM25Retriever)
- `duckduckgo-search` (Agente IA — búsqueda web)
- `langchain-classic` (Agente IA — AgentExecutor legacy)

---

## ⚙️ Instalación

```bash
git clone https://github.com/juanfranciscofernandezherreros/streamlint.git
cd streamlint

python3 -m venv env
source env/bin/activate   # Linux/macOS
# .\env\Scripts\activate  # Windows

pip install -r requirements.txt
```

Si vas a ejecutar loaders o retrievers avanzados, instala también sus extras (sección anterior).

---

## 🔐 Configuración de OpenAI

```bash
export OPENAI_API_KEY="sk-..."    # Linux/macOS
set OPENAI_API_KEY=sk-...         # Windows CMD
```

En las aplicaciones Streamlit también puedes introducirla desde la barra lateral.

---

## ▶️ Ejecución por tipo de proyecto

### Scripts de niveles (01–31)

```bash
python nivel_1_basico/01_prompt_templates.py
python nivel_4_document_loaders/12_read_pdf.py
python nivel_6_retrievers/23_vector_stores.py
```

### Scripts LangGraph (32–33, 36–37)

```bash
python nivel_7_langgraph/32_primer_programa_langgraph.py
python nivel_7_langgraph/33_procesador_reuniones.py
python nivel_7_langgraph/36_langgraph_condicional.py
python nivel_7_langgraph/37_langgraph_checkpointer.py
```

### Apps Streamlit del curso (34–35, 40)

```bash
streamlit run nivel_8_aplicaciones/34_all_exercise.py
streamlit run nivel_8_aplicaciones/35_streamlit_chatbox.py
streamlit run nivel_8_aplicaciones/40_streamlit_quiz_exam.py
```

### Proyecto RAG legal

```bash
# 1) Ingesta de contratos
python nivel_9_proyectos_integradores/asistente_legal/ingest.py

# 2) App de chat legal
streamlit run nivel_9_proyectos_integradores/asistente_legal/app.py
```

### Proyecto Agente IA

```bash
cd nivel_9_proyectos_integradores/agente_ia

# Modo interactivo
python agent.py

# Modo batch
python agent.py --questions "¿Cuánto es 2+2?" "¿Qué día es hoy?"

# Con Docker
docker compose run --rm agente-ia
```

### Nivel 10 — Memoria y Evaluación (38–39)

```bash
python nivel_10_memoria_y_evaluacion/38_conversacion_con_memoria.py
python nivel_10_memoria_y_evaluacion/39_evaluacion_llm.py
```

---

## 📌 Notas de organización importantes

- La secuencia oficial de aprendizaje es **01 → 40**, seguida de los proyectos integradores.
- Los niveles 1–6 cubren fundamentos de LangChain puro.
- El nivel 7 introduce **LangGraph** (grafos de estado, workflows y checkpointers).
- El nivel 8 agrupa las aplicaciones completas con **Streamlit**.
- El nivel 9 contiene **proyectos integradores** independientes y completos.
- El nivel 10 cubre **memoria conversacional** y **evaluación de LLMs**.
- El archivo `22_embeding_language.py` conserva ese nombre por compatibilidad histórica del repositorio.
- Algunos scripts tienen rutas absolutas locales en el código; si ejecutas en otra máquina, ajusta esas rutas.
- `faiss_db/` y `sesiones/` son datos de ejecución/persistencia del proyecto.

---

## ✅ Resumen

Este repositorio queda organizado en **10 niveles de dificultad creciente**:

1. **Niveles 1–6:** Curso progresivo de LangChain (prompts → retrievers).
2. **Nivel 7:** LangGraph — grafos de estado, edges condicionales y checkpointers.
3. **Nivel 8:** Aplicaciones completas con Streamlit.
4. **Nivel 9:** Proyectos integradores reales (RAG legal + Agente IA).
5. **Nivel 10:** Memoria conversacional y evaluación de salidas LLM.

Todo el stack, dependencias y formas de ejecución están centralizados en este README.
