# Streamlint — Chatbot con LangChain y Streamlit

Proyecto de aprendizaje y demostración que combina **LangChain**, **OpenAI** y **Streamlit** para construir aplicaciones conversacionales modernas. Incluye ejemplos progresivos que van desde plantillas de prompts básicas hasta pipelines paralelos y carga de documentos.

---

## 📋 Índice

- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Ejecución de la Aplicación Principal](#-ejecución-de-la-aplicación-principal)
- [Módulos de Aprendizaje](#-módulos-de-aprendizaje)
- [Pila Tecnológica](#-pila-tecnológica)

---

## ✨ Características

- 🤖 **Chatbot interactivo** con interfaz web, historial persistente y soporte multiconversación.
- 💬 **Streaming** de respuestas en tiempo real (efecto de escritura progresiva).
- 🧩 **Ejemplos paso a paso** de LangChain: prompts, cadenas LCEL, parsers y runnables.
- ⚡ **Procesamiento paralelo** con `RunnableParallel` y ejecución en lote con `.batch()`.
- 📊 **Salidas estructuradas** con modelos Pydantic para respuestas tipadas.
- 📚 **Carga de documentos**: páginas web y archivos PDF.

---

## 🗂 Estructura del Proyecto

```
streamlint/
│
├── 📱 Aplicaciones Streamlit
│   ├── streamlit_chatbox.py      # App principal: chatbot con gestión de sesiones
│   └── all_exercise.py           # Chatbot básico con selector de personalidad y modelo
│
├── 🧩 Módulos LangChain (Aprendizaje Progresivo)
│   ├── prompt_templates.py       # PromptTemplate básico (texto plano)
│   ├── chat_prompt_template.py   # ChatPromptTemplate con mensajes de sistema y usuario
│   ├── rol_prompt_tempaltes.py   # Plantillas con rol dinámico (SystemMessagePromptTemplate)
│   ├── message_placeholders.py   # MessagesPlaceholder para historial de conversación
│   ├── output_parser2.py         # Salida estructurada con Pydantic (básico)
│   └── analisis_pydantic.py      # Análisis completo con cadena LCEL + Pydantic
│
├── ⚡ Procesamiento Avanzado
│   ├── analisis_sentimientos.py  # Pipeline paralelo con RunnableLambda y batch
│   ├── paralelo.py               # RunnableParallel: 3 ramas simultáneas
│   └── paralelo_batch.py         # Batch + RunnableParallel: múltiples entradas
│
├── 📚 Carga de Documentos
│   ├── read_from_website.py      # WebBaseLoader: extracción de contenido web
│   ├── read_fiel.py              # PyPDFLoader: lectura de archivos PDF
│   └── document_loader.py        # Placeholder para loaders adicionales
│
├── 💾 Persistencia
│   ├── sesiones/                 # Sesiones de chat guardadas en JSON
│   └── historial_chat.json       # Historial principal de ejemplo
│
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Este archivo
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

### 4. Configurar la API Key de OpenAI

**Opción A — Variable de entorno** (recomendado para scripts de consola):

```bash
export OPENAI_API_KEY="sk-..."      # macOS/Linux
set OPENAI_API_KEY=sk-...           # Windows CMD
```

**Opción B — Interfaz web** (para las apps Streamlit):  
Introduce la API Key directamente en la barra lateral de la aplicación cuando se te solicite.

---

## ▶️ Ejecución de la Aplicación Principal

### Chatbot con gestión de sesiones (`streamlit_chatbox.py`)

```bash
streamlit run streamlit_chatbox.py
```

La aplicación se abrirá en `http://localhost:8501`. Desde la barra lateral podrás:
- Introducir tu API Key de OpenAI.
- Crear nuevas conversaciones.
- Cargar conversaciones previas guardadas en `sesiones/`.

### Chatbot básico con opciones (`all_exercise.py`)

```bash
streamlit run all_exercise.py
```

Permite seleccionar modelo, temperatura y personalidad del asistente desde la barra lateral.

---

## 📘 Módulos de Aprendizaje

Todos los módulos de consola se ejecutan con `python <nombre_archivo>.py` (requieren `OPENAI_API_KEY` en el entorno salvo los que sólo demuestran formateo de prompts).

| Archivo | Concepto principal | Requiere API Key |
|---|---|---|
| `prompt_templates.py` | `PromptTemplate` básico | No |
| `chat_prompt_template.py` | `ChatPromptTemplate` con roles | No |
| `rol_prompt_tempaltes.py` | Plantillas de rol dinámico | No |
| `message_placeholders.py` | `MessagesPlaceholder` para historial | No |
| `output_parser2.py` | Salida estructurada Pydantic (básico) | Sí |
| `analisis_pydantic.py` | Cadena LCEL + salida estructurada completa | Sí |
| `analisis_sentimientos.py` | Pipeline paralelo + `.batch()` | Sí |
| `paralelo.py` | `RunnableParallel` con 3 ramas | Sí |
| `paralelo_batch.py` | `RunnableParallel` + `.batch()` | Sí |
| `read_from_website.py` | `WebBaseLoader` (carga web) | No |
| `read_fiel.py` | `PyPDFLoader` (carga PDF) | No |

### Conceptos de LangChain cubiertos

| Categoría | Clases / Métodos |
|---|---|
| **Prompts** | `PromptTemplate`, `ChatPromptTemplate`, `SystemMessagePromptTemplate`, `MessagesPlaceholder` |
| **Mensajes** | `SystemMessage`, `HumanMessage`, `AIMessage` |
| **Modelos** | `ChatOpenAI` (gpt-4o-mini, gpt-4.1-mini, gpt-4.1) |
| **Cadenas LCEL** | Operador `|`, `.invoke()`, `.stream()`, `.batch()` |
| **Runnables** | `RunnableParallel`, `RunnableLambda` |
| **Parsers** | `StrOutputParser`, `with_structured_output()` |
| **Validación** | `pydantic.BaseModel`, `pydantic.Field` |
| **Loaders** | `WebBaseLoader`, `PyPDFLoader` |

---

## 🛠 Pila Tecnológica

| Capa | Tecnología |
|---|---|
| Interfaz web | [Streamlit](https://streamlit.io/) |
| Framework LLM | [LangChain](https://python.langchain.com/) |
| Proveedor LLM | [OpenAI](https://platform.openai.com/) |
| Validación de datos | [Pydantic v2](https://docs.pydantic.dev/) |
| Variables de entorno | [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Lenguaje | Python 3.8+ |
