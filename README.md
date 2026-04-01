# Streamlint

Proyecto de aprendizaje práctico de **LangChain + OpenAI + Streamlit**, organizado por niveles (de básico a avanzado) y con un proyecto RAG completo adicional.

---

## 🎯 Objetivo del repositorio

Este repositorio está reorganizado como una ruta progresiva para:

1. Aprender fundamentos de prompts y cadenas.
2. Trabajar con salidas estructuradas y ejecución paralela.
3. Cargar documentos de múltiples fuentes.
4. Crear embeddings, vector stores y retrievers.
5. Construir aplicaciones completas en Streamlit.
6. Implementar un caso real de **RAG legal**.

---

## 🗂️ Estructura completa (ordenada)

```text
streamlint/
├── README.md
├── requirements.txt
├── .gitignore
│
├── nivel_1_basico/
│   ├── 01_prompt_templates.py
│   ├── 02_chat_prompt_template.py
│   ├── 03_rol_prompt_templates.py
│   └── 04_message_placeholders.py
│
├── nivel_2_intermedio/
│   ├── 05_output_parser.py
│   ├── 06_analisis_pydantic.py
│   └── 07_output_parser_parte2.py
│
├── nivel_3_avanzado/
│   ├── 08_analisis_sentimientos.py
│   ├── 09_paralelo.py
│   └── 10_paralelo_batch.py
│
├── nivel_4_document_loaders/
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
├── nivel_5_text_splitters_y_embeddings/
│   ├── 20_text_splitters_parte1.py
│   ├── 21_text_splitters_parte2.py
│   └── 22_embeding_language.py
│
├── nivel_6_retrievers/
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
├── nivel_7_aplicaciones/
│   ├── 32_all_exercise.py
│   └── 33_streamlit_chatbox.py
│
├── asistente_legal/
│   ├── app.py
│   ├── config.py
│   ├── ingest.py
│   ├── prompt.py
│   └── rag_system.py
│
├── contratos/                # PDFs de contratos para ejemplos RAG/retrievers
├── sesiones/                 # Conversaciones persistidas en JSON
├── chroma_db/                # Base vectorial local (Chroma)
├── historial_chat.json       # Historial de ejemplo
└── cambridge_english_first.pdf
```

---

## 🧭 Proyectos del repositorio en orden

### 1) Ruta formativa principal (01 → 33)

- **Nivel 1 (01–04):** PromptTemplate y ChatPromptTemplate.
- **Nivel 2 (05–07):** Salida estructurada con Pydantic.
- **Nivel 3 (08–10):** Runnables paralelos y procesamiento por lotes.
- **Nivel 4 (11–19):** Document loaders (web, PDF, carpeta, YouTube, HTML, CSV, Selenium, Git, Google Drive).
- **Nivel 5 (20–22):** Text splitters y embeddings.
- **Nivel 6 (23–31):** Retrievers (similitud, multi-query, compresión contextual, ensemble, parent, self-query, time-weighted, MMR).
- **Nivel 7 (32–33):** Apps finales con Streamlit.

### 2) Proyecto aplicado adicional: `asistente_legal/`

Proyecto RAG legal completo con:

- Ingesta de contratos PDF a Chroma (`ingest.py`).
- Cadena de recuperación y generación (`rag_system.py`).
- Interfaz de chat en Streamlit (`app.py`).

---

## 🛠️ Todo lo que usa el proyecto

### Núcleo

- **Python 3.8+** (recomendado 3.12)
- **LangChain**
- **LangChain OpenAI**
- **LangChain Community**
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
- `chromadb` (persistencia vectorial con Chroma)
- `rank_bm25` (BM25Retriever)
- `faiss-cpu` (FAISS)

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

### Apps Streamlit del curso (32–33)

```bash
streamlit run nivel_7_aplicaciones/32_all_exercise.py
streamlit run nivel_7_aplicaciones/33_streamlit_chatbox.py
```

### Proyecto RAG legal

```bash
# 1) Ingesta de contratos
python asistente_legal/ingest.py

# 2) App de chat legal
streamlit run asistente_legal/app.py
```

---

## 📌 Notas de organización importantes

- La secuencia oficial de aprendizaje es **01 → 33**.
- `asistente_legal/` es un proyecto aplicado independiente sobre la misma base tecnológica.
- Algunos scripts tienen rutas absolutas locales en el código (ej. `/home/usuario/streamlint/...`); si ejecutas en otra máquina, ajusta esas rutas.
- `chroma_db/` y `sesiones/` son datos de ejecución/persistencia del proyecto.

---

## ✅ Resumen

Este repositorio queda documentado y organizado en dos bloques claros:

1. **Curso progresivo por niveles** (fundamentos → aplicaciones).
2. **Proyecto RAG legal completo** para uso práctico real.

Todo el stack, dependencias y formas de ejecución están centralizados en este README.
