# ⭐ Nivel 1 — Básico: Prompts y Plantillas

Introducción a los fundamentos de **LangChain**: creación de prompts, plantillas de chat, roles y placeholders para gestionar conversaciones.

## Scripts

| # | Archivo | Descripción |
|---|---------|-------------|
| 01 | `01_prompt_templates.py` | Plantillas básicas con `PromptTemplate`. Genera prompts de texto plano a partir de cadenas con variables. |
| 02 | `02_chat_prompt_template.py` | Plantillas de chat con `ChatPromptTemplate`. Crea mensajes de sistema y usuario parametrizados. |
| 03 | `03_rol_prompt_templates.py` | Templates con roles dinámicos (`SystemMessagePromptTemplate` + `HumanMessagePromptTemplate`). |
| 04 | `04_message_placeholders.py` | Uso de `MessagesPlaceholder` para insertar historial de conversación dinámicamente. |

## Conceptos clave

- **`PromptTemplate`** — Genera prompts de texto plano con variables entre llaves.
- **`ChatPromptTemplate`** — Genera listas de mensajes de chat (system, human, AI).
- **`SystemMessagePromptTemplate`** / **`HumanMessagePromptTemplate`** — Templates específicos por rol.
- **`MessagesPlaceholder`** — Permite inyectar una lista de mensajes en un punto del template.

## Ejecución

```bash
python nivel_1_basico/01_prompt_templates.py
python nivel_1_basico/02_chat_prompt_template.py
python nivel_1_basico/03_rol_prompt_templates.py
python nivel_1_basico/04_message_placeholders.py
```

## Requisitos

- `langchain`, `langchain-openai`, `python-dotenv`
- Variable de entorno `OPENAI_API_KEY` configurada.

## Siguiente nivel

➡️ [Nivel 2 — Intermedio: Salida estructurada](../nivel_2_intermedio/)
