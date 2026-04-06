from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import chromadb
from langchain_community import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

class DocumentProcessor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
        # Para CSVs de filas cortas, el splitter suele ser menos crítico, 
        # pero lo mantenemos para el contenido JSON o descripciones largas.
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200
        )

    def _load_csv_file(self, filepath: Path) -> List[Document]:
        """Convierte cada fila del CSV en un documento descriptivo."""
        documents = []
        try:
            # Leemos el CSV (usando pandas es más robusto con los encodings)
            df = pd.read_csv(filepath)
            
            for _, row in df.iterrows():
                # Creamos una descripción natural para que el embedding sea más preciso
                # Ejemplo: "En TURKEY (Super Lig), el partido Turk Telekom vs Esenler... "
                content = (
                    f"País: {row.get('País', 'N/A')}\n"
                    f"Liga: {row.get('Liga', 'N/A')}\n"
                    f"Partido: {row.get('Partido', 'N/A')}\n"
                    f"Resultado: {row.get('Resultado', '---')}\n"
                    f"Estado: {row.get('Estado', 'N/A')}\n"
                    f"Hora: {row.get('Hora', 'N/A')}\n"
                    f"Link: {row.get('Link Partido', '')}"
                )
                
                # Metadatos para poder filtrar luego por país o liga en Chroma
                metadata = {
                    "source": filepath.name,
                    "pais": str(row.get('País', '')),
                    "liga": str(row.get('Liga', '')),
                    "tipo": "resultado_baloncesto"
                }
                
                documents.append(Document(page_content=content, metadata=metadata))
        except Exception as e:
            print(f"❌ Error procesando {filepath.name}: {e}")
            
        return documents

    def _load_json_file(self, filepath: Path) -> List[Document]:
        # Mantenemos tu lógica original para los planes del gimnasio
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        
        plan = data.get("plan_maestro", data)
        mes = plan.get("mes", "Enero")
        gimnasio = plan.get("gimnasio", "DIF")
        documents = []

        for entry in plan.get("calendario_diario", []):
            fecha_iso = entry.get("fecha", "")
            content = f"Gimnasio: {gimnasio}\nFecha: {fecha_iso}\n"
            content += f"Sala A: {entry.get('sala_a')}\nSala B: {entry.get('sala_b')}\nSala C: {entry.get('sala_c')}"
            documents.append(Document(page_content=content, metadata={"tipo": "calendario", "fecha": fecha_iso}))

        # (He omitido el resto del glosario para abreviar, pero mantén tu código ahí)
        return documents

    def run_setup(self):
        print(f"🚀 Iniciando procesamiento en: {DOCS_PATH}")
        all_docs = []

        # 1. Cargar JSONs
        for f in Path(DOCS_PATH).glob("*.json"):
            print(f"📄 Cargando JSON: {f.name}")
            all_docs.extend(self._load_json_file(f))

        # 2. Cargar CSVs
        for f in Path(DOCS_PATH).glob("*.csv"):
            print(f"📊 Cargando CSV: {f.name}")
            all_docs.extend(self._load_csv_file(f))
        
        if not all_docs:
            print("⚠️ No se encontraron documentos para indexar.")
            return

        # Dividir en fragmentos (principalmente para los JSON o notas largas)
        chunks = self.text_splitter.split_documents(all_docs)
        
        # Guardar en ChromaDB
        print(f"🧠 Generando embeddings para {len(chunks)} fragmentos...")
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=CHROMADB_PATH
        )
        
        print(f"✅ Base de datos vectorial actualizada en {CHROMADB_PATH}")

if __name__ == "__main__":
    # Asegúrate de que en config.py DOCS_PATH sea "/python/basketball-data"
    DocumentProcessor().run_setup()