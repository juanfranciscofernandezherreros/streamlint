from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List, TYPE_CHECKING
import os
import sys
import openai

if TYPE_CHECKING:
    from langgraph.graph.state import CompiledStateGraph

# Configuración
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Extensiones de archivos multimedia soportadas
MEDIA_EXTENSIONS = {".mp4", ".mov", ".m4a", ".mp3", ".wav", ".mkv", ".webm"}
# Extensiones de archivos de texto soportadas
TEXT_EXTENSIONS = {".txt", ".md"}

# Definición del Estado
class State(TypedDict):
    notes: str
    participants: List[str]
    topics: List[str]
    action_items: List[str]
    minutes: str
    summary: str

# ============= NODOS DEL WORKFLOW =============

def extract_participants(state: State) -> State:
    """Extrae los participantes de la reunión.

    Analiza las notas y devuelve una lista de nombres propios identificados.
    Si el texto está vacío o no contiene nombres, devuelve una lista vacía.
    """
    notes = state.get("notes", "").strip()
    if not notes:
        print("⚠ No hay notas disponibles para extraer participantes")
        return {"participants": []}

    prompt = f"""
    De las siguientes notas de reunión, extrae SOLO los nombres de los participantes.
    
    Notas: {notes}
    
    Responde ÚNICAMENTE con una lista de nombres separados por comas, sin explicaciones adicionales.
    Si no se identifican participantes, responde con: "Sin participantes"
    Ejemplo: Juan García, María López, Carlos Ruiz
    """

    response = llm.invoke(prompt)
    content = response.content.strip()

    if "Sin participantes" in content or not content:
        participants = []
    else:
        participants = [p.strip() for p in content.split(",") if p.strip()]

    print(f"✓ Participantes extraídos: {len(participants)} personas")

    return {"participants": participants}


def identify_topics(state: State) -> State:
    """Identifica los temas principales discutidos (3-5 elementos).

    Analiza las notas y extrae los temas relevantes evitando categorías
    demasiado generales o demasiado específicas.
    """
    notes = state.get("notes", "").strip()
    if not notes:
        print("⚠ No hay notas disponibles para identificar temas")
        return {"topics": []}

    prompt = f"""
    Identifica los 3-5 temas principales discutidos en esta reunión.
    
    Notas: {notes}
    
    Responde SOLO con los temas separados por punto y coma (;).
    Evita categorías demasiado generales (p. ej. "varios") o demasiado específicas.
    Si no se identifican temas, responde con: "Sin temas identificados"
    Ejemplo: Arquitectura del sistema; Plazos de entrega; Asignación de tareas
    """

    response = llm.invoke(prompt)
    content = response.content.strip()

    if "Sin temas" in content or not content:
        topics = []
    else:
        topics = [t.strip() for t in content.split(";") if t.strip()]

    print(f"✓ Temas identificados: {len(topics)} temas")

    return {"topics": topics}


def extract_actions(state: State) -> State:
    """Extrae las acciones acordadas con responsables asignados.

    Identifica tanto acciones explícitas como implícitas y las devuelve
    separadas por pipe (|).
    """
    notes = state.get("notes", "").strip()
    if not notes:
        print("⚠ No hay notas disponibles para extraer acciones")
        return {"action_items": []}

    prompt = f"""
    Extrae las acciones específicas acordadas en la reunión, incluyendo el responsable si se menciona.
    Identifica tanto acciones explícitas como compromisos implícitos.
    
    Notas: {notes}
    
    Formato de respuesta: Acciones separadas por |
    Ejemplo: María se encargará del backend | Carlos preparará el plan de testing | Próxima reunión el lunes
    
    Si no hay acciones claras, responde con: "No se identificaron acciones específicas"
    """

    response = llm.invoke(prompt)
    content = response.content.strip()

    if "No se identificaron" in content or not content:
        action_items = []
    else:
        action_items = [a.strip() for a in content.split("|") if a.strip()]

    print(f"✓ Acciones extraídas: {len(action_items)} items")

    return {"action_items": action_items}


def generate_minutes(state: State) -> State:
    """Genera una minuta formal de la reunión (máx. 150 palabras).

    Combina la información de participantes, temas y acciones ya extraídas
    con las notas originales para producir un documento formal.
    """
    participants = state.get("participants", [])
    topics = state.get("topics", [])
    action_items = state.get("action_items", [])
    notes = state.get("notes", "").strip()

    participants_str = ", ".join(participants) if participants else "No identificados"
    topics_str = "\n• ".join(topics) if topics else "No identificados"
    actions_str = (
        "\n• ".join(action_items)
        if action_items
        else "No se definieron acciones específicas"
    )

    prompt = f"""
    Genera una minuta formal y profesional basándote en la siguiente información:
    
    PARTICIPANTES: {participants_str}
    
    TEMAS DISCUTIDOS:
    • {topics_str}
    
    ACCIONES ACORDADAS:
    • {actions_str}
    
    NOTAS ORIGINALES: {notes}
    
    Genera una minuta profesional de máximo 150 palabras que incluya:
    1. Encabezado con tipo de reunión
    2. Lista de asistentes
    3. Puntos principales discutidos
    4. Acuerdos y próximos pasos
    
    Usa un tono formal y estructura clara.
    """

    response = llm.invoke(prompt)

    print(f"✓ Minuta generada: {len(response.content.split())} palabras")

    return {"minutes": response.content}


def create_summary(state: State) -> State:
    """Crea un resumen ejecutivo ultra-conciso (máx. 30 palabras).

    Sintetiza participantes, tema principal y número de acciones en una
    frase ejecutiva breve.
    """
    participants = state.get("participants", [])
    topics = state.get("topics", [])
    action_items = state.get("action_items", [])

    participants_preview = ", ".join(participants[:3])
    if len(participants) > 3:
        participants_preview += "..."

    main_topic = topics[0] if topics else "General"
    num_actions = len(action_items)

    prompt = f"""
    Crea un resumen ejecutivo de MÁXIMO 30 palabras que capture la esencia de esta reunión.
    
    Participantes: {participants_preview}
    Tema principal: {main_topic}
    Acciones clave: {num_actions} acciones definidas
    
    El resumen debe ser conciso y directo al punto.
    """

    response = llm.invoke(prompt)

    print("✓ Resumen creado")

    return {"summary": response.content}

# ============= CONSTRUCCIÓN DEL GRAFO =============

def create_workflow():
    """Crea y configura el workflow de LangGraph.

    Flujo: START → extract_participants → identify_topics → extract_actions
           → generate_minutes → create_summary → END
    """
    workflow = StateGraph(State)

    # Agregar todos los nodos
    workflow.add_node("extract_participants", extract_participants)
    workflow.add_node("identify_topics", identify_topics)
    workflow.add_node("extract_actions", extract_actions)
    workflow.add_node("generate_minutes", generate_minutes)
    workflow.add_node("create_summary", create_summary)

    # Configurar flujo secuencial
    workflow.add_edge(START, "extract_participants")
    workflow.add_edge("extract_participants", "identify_topics")
    workflow.add_edge("identify_topics", "extract_actions")
    workflow.add_edge("extract_actions", "generate_minutes")
    workflow.add_edge("generate_minutes", "create_summary")
    workflow.add_edge("create_summary", END)

    return workflow.compile()

# ============= FUNCIONES DE PROCESAMIENTO =============

def transcribe_media(file_path: str) -> str:
    """Transcribe un archivo de audio/vídeo usando la API Whisper de OpenAI.

    Args:
        file_path: Ruta absoluta al archivo multimedia.

    Returns:
        Texto transcrito o mensaje de error si falla la transcripción.
    """
    try:
        print("🎙️ Transcribiendo con OpenAI Whisper API...")

        client = openai.OpenAI()  # Usa OPENAI_API_KEY del entorno

        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="es",
                response_format="text",
            )

        print(f"✓ Transcripción completada: {len(transcript)} caracteres")
        return transcript

    except openai.AuthenticationError:
        print("❌ Error de autenticación: asegúrate de que OPENAI_API_KEY esté configurada en el entorno")
        return ""
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {file_path}")
        return ""
    except Exception as e:
        print(f"❌ Error en transcripción: {e}")
        return ""


def read_text_file(file_path: str) -> str:
    """Lee un archivo de texto (.txt o .md) y devuelve su contenido.

    Args:
        file_path: Ruta absoluta al archivo de texto.

    Returns:
        Contenido del archivo o cadena vacía si falla la lectura.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if not content.strip():
            print("⚠ El archivo de texto está vacío")
            return ""
        print(f"✓ Archivo leído: {len(content)} caracteres")
        return content
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {file_path}")
        return ""
    except UnicodeDecodeError:
        print("⚠ Error de codificación, intentando con latin-1...")
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error al leer archivo: {e}")
            return ""


def load_input(file_path: str) -> str:
    """Carga y devuelve el texto de entrada según el tipo de archivo.

    Soporta archivos multimedia (transcripción con Whisper) y de texto.

    Args:
        file_path: Ruta absoluta al archivo de entrada.

    Returns:
        Texto extraído del archivo.

    Raises:
        ValueError: Si la extensión del archivo no es soportada.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext in MEDIA_EXTENSIONS:
        return transcribe_media(file_path)
    elif ext in TEXT_EXTENSIONS:
        return read_text_file(file_path)
    else:
        supported = ", ".join(sorted(MEDIA_EXTENSIONS | TEXT_EXTENSIONS))
        raise ValueError(
            f"Extensión '{ext}' no soportada. Extensiones válidas: {supported}"
        )


def process_meeting_notes(notes: str, app: "CompiledStateGraph") -> State:
    """Procesa una nota de reunión a través del workflow completo.

    Args:
        notes: Texto de las notas de la reunión.
        app: Workflow compilado de LangGraph.

    Returns:
        Estado final con todos los campos procesados.
    """
    initial_state: State = {
        "notes": notes,
        "participants": [],
        "topics": [],
        "action_items": [],
        "minutes": "",
        "summary": "",
    }

    print("\n" + "=" * 60)
    print("🔄 Procesando nota de reunión...")
    print("=" * 60)

    result = app.invoke(initial_state)
    return result


def display_results(result: State, meeting_num: int = 1) -> None:
    """Muestra los resultados de forma estructurada en consola.

    Args:
        result: Estado final del workflow con toda la información procesada.
        meeting_num: Número de reunión para el encabezado.
    """
    print(f"\n📋 RESULTADOS - REUNIÓN #{meeting_num}")
    print("-" * 60)

    print(f"\n👥 Participantes ({len(result['participants'])}):")
    for p in result["participants"]:
        print(f"   • {p}")

    print(f"\n📍 Temas tratados ({len(result['topics'])}):")
    for t in result["topics"]:
        print(f"   • {t}")

    print(f"\n✅ Acciones acordadas ({len(result['action_items'])}):")
    if result["action_items"]:
        for a in result["action_items"]:
            print(f"   • {a}")
    else:
        print("   • No se definieron acciones específicas")

    print("\n📄 MINUTA FORMAL:")
    print("-" * 40)
    print(result["minutes"])
    print("-" * 40)

    print("\n💡 RESUMEN EJECUTIVO:")
    print(f"   {result['summary']}")

    print("\n" + "=" * 60)


def select_file() -> str:
    """Abre un diálogo gráfico para seleccionar un archivo de entrada.

    Returns:
        Ruta absoluta al archivo seleccionado o cadena vacía si se cancela.
    """
    try:
        from tkinter import Tk, filedialog

        Tk().withdraw()
        file_path = filedialog.askopenfilename(
            title="Selecciona un vídeo o transcripción",
            filetypes=[
                ("Vídeo/Audio", "*.mp4 *.mov *.m4a *.mp3 *.wav *.mkv *.webm"),
                ("Texto", "*.txt *.md"),
            ],
        )
        return file_path or ""
    except ImportError:
        print("⚠ tkinter no disponible. Pasa la ruta del archivo como argumento:")
        print("  python 33_procesador_reuniones.py <ruta_al_archivo>")
        return ""
    except Exception:
        print("⚠ No se pudo abrir el diálogo de archivos.")
        print("  Pasa la ruta del archivo como argumento:")
        print("  python 33_procesador_reuniones.py <ruta_al_archivo>")
        return ""

# ============= DEMOSTRACIÓN =============

if __name__ == "__main__":
    app = create_workflow()

    # Aceptar ruta de archivo por argumento o mediante diálogo gráfico
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = select_file()

    if not file_path:
        print("No se seleccionó archivo.")
        raise SystemExit(0)

    if not os.path.isfile(file_path):
        print(f"❌ El archivo no existe: {file_path}")
        raise SystemExit(1)

    notes = load_input(file_path)

    if not notes:
        raise SystemExit(1)

    result = process_meeting_notes(notes, app)
    display_results(result, 1)