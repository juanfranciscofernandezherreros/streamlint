# Streamlint — Chatbot con LangChain y Streamlit

Proyecto de aprendizaje y demostración que combina **LangChain**, **OpenAI** y **Streamlit** para construir aplicaciones conversacionales modernas. Los módulos están organizados de **lo más sencillo a lo más avanzado**, permitiendo seguir un itinerario de aprendizaje progresivo.

---

## 📋 Índice

- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Itinerario de Aprendizaje](#-itinerario-de-aprendizaje)
- [Ejecución de las Aplicaciones](#-ejecución-de-las-aplicaciones)
- [Pila Tecnológica](#-pila-tecnológica)

---

## ✨ Características

- 🤖 **Chatbot interactivo** con interfaz web, historial persistente y soporte multiconversación.
- 💬 **Streaming** de respuestas en tiempo real (efecto de escritura progresiva).
- 🧩 **Ejemplos paso a paso** de LangChain: prompts, cadenas LCEL, parsers y runnables.
- ⚡ **Procesamiento paralelo** con `RunnableParallel` y ejecución en lote con `.batch()`.
- 📊 **Salidas estructuradas** con modelos Pydantic para respuestas tipadas.
- 📚 **Document Loaders**: web, PDF, directorios, YouTube, HTML, CSV, Selenium, Git y Google Drive.

---

## 🗂 Estructura del Proyecto

```
streamlint/
│
├── nivel_1_basico/                    ← Sin API Key · Solo formateo de prompts
│   ├── 01_prompt_templates.py         # PromptTemplate básico (texto plano)
│   ├── 02_chat_prompt_template.py     # ChatPromptTemplate con roles
│   ├── 03_rol_prompt_templates.py     # Plantillas con rol dinámico
│   └── 04_message_placeholders.py    # MessagesPlaceholder para historial
│
├── nivel_2_intermedio/                ← Requiere API Key · Salidas estructuradas
│   ├── 05_output_parser.py            # Salida estructurada Pydantic (básico)
│   └── 06_analisis_pydantic.py        # Cadena LCEL + salida estructurada completa
│
├── nivel_3_avanzado/                  ← Requiere API Key · Procesamiento paralelo
│   ├── 07_analisis_sentimientos.py    # Pipeline paralelo con RunnableLambda + batch
│   ├── 08_paralelo.py                 # RunnableParallel con 3 ramas simultáneas
│   └── 09_paralelo_batch.py           # RunnableParallel + .batch() con varias entradas
│
├── nivel_4_document_loaders/          ← Carga de documentos de múltiples fuentes
│   ├── 10_read_from_website.py        # WebBaseLoader: extracción de contenido web
│   ├── 11_read_pdf.py                 # PyPDFLoader: lectura de archivos PDF
│   ├── 12_directory_loader.py         # DirectoryLoader: procesamiento masivo de archivos
│   ├── 13_youtube_loader.py           # YoutubeLoader: transcripciones de vídeos
│   ├── 14_unstructured_html_loader.py # UnstructuredHTMLLoader: HTML local con estructura
│   ├── 15_csv_loader.py               # CSVLoader: datos tabulares como documentos
│   ├── 16_selenium_url_loader.py      # SeleniumURLLoader: páginas con JavaScript
│   └── 17_git_loader.py               # GitLoader: código fuente desde repositorios Git
│
├── nivel_5_aplicaciones/              ← Streamlit · Aplicaciones completas
│   ├── 18_all_exercise.py             # Chatbot básico con selector de modelo y personalidad
│   └── 19_streamlit_chatbox.py        # Chatbot avanzado con gestión de sesiones persistentes
│
├── sesiones/                          # Sesiones de chat guardadas en JSON
├── google_drive.py                    # Ejemplo de GoogleDriveLoader (requiere credenciales OAuth)
├── historial_chat.json                # Historial de ejemplo
├── cambridge_english_first.pdf        # PDF de prueba para los ejemplos de PyPDFLoader
├── requirements.txt                   # Dependencias del proyecto
└── README.md                          # Este archivo
```

---

## ⚙️ Requisitos

- Python 3.8 o superior (se recomienda Python 3.12)
- Cuenta y **API Key de OpenAI** con acceso a `gpt-4o-mini` (o superior)
- Conexión a internet (para llamadas a la API y, opcionalmente, carga web)

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/juanfranciscofernandezherreros/streamlint.git
cd streamlint
```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv env

# macOS / Linux:
source env/bin/activate

# Windows:
.\env\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> **Dependencias opcionales** para los loaders del Nivel 4:
>
> | Loader | Paquete a instalar |
> |---|---|
> | `DirectoryLoader` + `UnstructuredHTMLLoader` | `pip install unstructured` |
> | `YoutubeLoader` | `pip install youtube-transcript-api` |
> | `SeleniumURLLoader` | `pip install selenium` + ChromeDriver en el PATH |
> | `GitLoader` | `pip install gitpython` |
> | `GoogleDriveLoader` (`google_drive.py`) | `pip install langchain-google-community google-auth-oauthlib google-api-python-client` |

### 4. Configurar la API Key de OpenAI

**Opción A — Variable de entorno** (recomendado para scripts de consola):

```bash
export OPENAI_API_KEY="sk-..."      # macOS/Linux
set OPENAI_API_KEY=sk-...           # Windows CMD
```

**Opción B — Interfaz web** (para las apps Streamlit):  
Introduce la API Key directamente en la barra lateral de la aplicación cuando se te solicite.

---

## 📘 Itinerario de Aprendizaje

Todos los módulos de consola se ejecutan con `python <ruta/archivo.py>`.

### Nivel 1 — Básico (sin API Key)

| Archivo | Concepto principal |
|---|---|
| `nivel_1_basico/01_prompt_templates.py` | `PromptTemplate` básico (texto plano) |
| `nivel_1_basico/02_chat_prompt_template.py` | `ChatPromptTemplate` con roles de sistema y usuario |
| `nivel_1_basico/03_rol_prompt_templates.py` | Plantillas con rol y especialidad dinámicos |
| `nivel_1_basico/04_message_placeholders.py` | `MessagesPlaceholder` para gestionar historial |

### Nivel 2 — Intermedio (requiere API Key)

| Archivo | Concepto principal |
|---|---|
| `nivel_2_intermedio/05_output_parser.py` | Salida estructurada con Pydantic y `with_structured_output()` |
| `nivel_2_intermedio/06_analisis_pydantic.py` | Cadena LCEL + salida estructurada con 3 campos (resumen, sentimiento, palabras clave) |

### Nivel 3 — Avanzado (requiere API Key)

| Archivo | Concepto principal |
|---|---|
| `nivel_3_avanzado/07_analisis_sentimientos.py` | Pipeline paralelo (`RunnableParallel` + `RunnableLambda`) con `.batch()` |
| `nivel_3_avanzado/08_paralelo.py` | `RunnableParallel` con 3 ramas: respuesta, sentimiento y hashtags |
| `nivel_3_avanzado/09_paralelo_batch.py` | `RunnableParallel` + `.batch()` con control de concurrencia (`max_concurrency`) |

### Nivel 4 — Document Loaders

| Archivo | Loader | Fuente | Req. extra |
|---|---|---|---|
| `nivel_4_document_loaders/10_read_from_website.py` | `WebBaseLoader` | Páginas web (ej. Wikipedia, LangChain docs) | `beautifulsoup4` |
| `nivel_4_document_loaders/11_read_pdf.py` | `PyPDFLoader` | Archivos PDF (estadísticas por página y búsqueda) | `pypdf` |
| `nivel_4_document_loaders/12_directory_loader.py` | `DirectoryLoader` | Carpetas locales (`.md` recursivo, multihilo) | `unstructured` |
| `nivel_4_document_loaders/13_youtube_loader.py` | `YoutubeLoader` | Vídeos de YouTube (transcripción + metadatos) | `youtube-transcript-api` |
| `nivel_4_document_loaders/14_unstructured_html_loader.py` | `UnstructuredHTMLLoader` | HTML local con `mode="elements"` | `unstructured` |
| `nivel_4_document_loaders/15_csv_loader.py` | `CSVLoader` | Archivos CSV (columnas como metadatos) | — |
| `nivel_4_document_loaders/16_selenium_url_loader.py` | `SeleniumURLLoader` | Páginas con contenido JS (Chrome headless) | `selenium` + ChromeDriver |
| `nivel_4_document_loaders/17_git_loader.py` | `GitLoader` | Repositorios Git (filtrado por extensión) | `gitpython` |

### Google Drive (script independiente)

| Archivo | Loader | Descripción |
|---|---|---|
| `google_drive.py` | `GoogleDriveLoader` | Carga documentos desde una carpeta de Google Drive usando credenciales OAuth 2.0 |

### Nivel 5 — Aplicaciones Streamlit

| Archivo | Descripción |
|---|---|
| `nivel_5_aplicaciones/18_all_exercise.py` | Chatbot con selector de modelo (`gpt-4o-mini`, `gpt-4.1-mini`, `gpt-4.1`), temperatura y personalidad; streaming activado |
| `nivel_5_aplicaciones/19_streamlit_chatbox.py` | Chatbot avanzado «Chat Manager Pro»: múltiples conversaciones con persistencia JSON en `sesiones/`, carga y guardado automático |

### Conceptos de LangChain cubiertos

| Categoría | Clases / Métodos |
|---|---|
| **Prompts** | `PromptTemplate`, `ChatPromptTemplate`, `SystemMessagePromptTemplate`, `HumanMessagePromptTemplate`, `MessagesPlaceholder` |
| **Mensajes** | `SystemMessage`, `HumanMessage`, `AIMessage` |
| **Modelos** | `ChatOpenAI` (`gpt-4o-mini`, `gpt-4.1-mini`, `gpt-4.1`) |
| **Cadenas LCEL** | Operador `\|`, `.invoke()`, `.stream()`, `.batch()` |
| **Runnables** | `RunnableParallel`, `RunnableLambda` |
| **Parsers** | `StrOutputParser`, `with_structured_output()` |
| **Validación** | `pydantic.BaseModel`, `pydantic.Field` |
| **Loaders** | `WebBaseLoader`, `PyPDFLoader`, `DirectoryLoader`, `YoutubeLoader`, `UnstructuredHTMLLoader`, `CSVLoader`, `SeleniumURLLoader`, `GitLoader`, `GoogleDriveLoader` |

---

## ▶️ Ejecución de las Aplicaciones

### Chatbot con gestión de sesiones (recomendado)

```bash
streamlit run nivel_5_aplicaciones/19_streamlit_chatbox.py
```

La aplicación se abrirá en `http://localhost:8501`. Desde la barra lateral podrás:
- Introducir tu API Key de OpenAI.
- Crear nuevas conversaciones con el botón **➕ Nueva Conversación**.
- Cargar conversaciones previas guardadas automáticamente en `sesiones/`.

### Chatbot básico con opciones

```bash
streamlit run nivel_5_aplicaciones/18_all_exercise.py
```

Permite seleccionar modelo, temperatura (0.0–1.0) y personalidad del asistente desde la barra lateral.

### Scripts de consola (Niveles 1–4)

```bash
# Ejemplo nivel 1 (no requiere API Key):
python nivel_1_basico/01_prompt_templates.py

# Ejemplo nivel 4:
python nivel_4_document_loaders/11_read_pdf.py
```

---

## 🛠 Pila Tecnológica

| Capa | Tecnología |
|---|---|
| Interfaz web | [Streamlit](https://streamlit.io/) |
| Framework LLM | [LangChain](https://python.langchain.com/) + [LangChain Community](https://pypi.org/project/langchain-community/) |
| Proveedor LLM | [OpenAI](https://platform.openai.com/) (`gpt-4o-mini`, `gpt-4.1-mini`, `gpt-4.1`) |
| Validación de datos | [Pydantic v2](https://docs.pydantic.dev/) |
| Parseo de HTML | [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) |
| Lectura de PDF | [pypdf](https://pypdf.readthedocs.io/) |
| Variables de entorno | [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Lenguaje | Python 3.8+ (recomendado 3.12) |
