import hashlib
import json
from typing import List
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config import *


class DocumentProcessor:
    """Procesador de documentos para el sistema RAG."""

    def __init__(self, docs_path: str = "docs", chroma_path: str = "./chroma_db"):
        self.docs_path = Path(docs_path)
        self.chroma_path = Path(chroma_path)
        self.embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        )

    def load_documents(self) -> List[Document]:
        """Carga documentos markdown y JSON del directorio docs."""
        print(f"📚 Cargando documentos desde {self.docs_path}")

        documents: List[Document] = []

        # Cargar archivos markdown
        md_files = list(self.docs_path.glob("*.md"))
        if md_files:
            loader = DirectoryLoader(
                str(self.docs_path),
                glob="*.md",
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"},
            )
            documents.extend(loader.load())

        # Cargar archivos JSON
        json_files = list(self.docs_path.glob("*.json"))
        for json_file in json_files:
            print(f"📄 Procesando JSON: {json_file.name}")
            json_docs = self._load_json_file(json_file)
            documents.extend(json_docs)

        # Enriquecer metadatos
        for doc in documents:
            source = doc.metadata.get("source", "")
            filename = Path(source).stem if source else "unknown"
            doc.metadata.setdefault("filename", filename)
            doc.metadata.setdefault("doc_type", self._get_doc_type(filename))
            doc.metadata.setdefault("doc_id", self._generate_doc_id(doc.page_content))

        print(f"✅ Cargados {len(documents)} documentos")
        return documents

    def _load_json_file(self, filepath: Path) -> List[Document]:
        """Convierte un archivo JSON estructurado en documentos de texto."""
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)

        source = str(filepath)
        documents: List[Document] = []

        plan = data.get("plan_maestro", data)

        mes = plan.get("mes", "")
        gimnasio = plan.get("gimnasio", "")
        base_meta = {"source": source, "mes": mes, "gimnasio": gimnasio}

        # --- Calendario diario ---
        for entry in plan.get("calendario_diario", []):
            fecha = entry.get("fecha", "")
            lines = [f"Fecha: {fecha}"]
            for sala in ("sala_a", "sala_b", "sala_c"):
                actividad = entry.get(sala)
                if actividad:
                    sala_label = sala.replace("_", " ").title()
                    lines.append(f"  {sala_label}: {actividad}")
            obs = entry.get("observaciones")
            if obs:
                lines.append(f"  Observaciones: {obs}")

            text = (
                f"Plan {gimnasio} - {mes}\n"
                f"Calendario diario\n" + "\n".join(lines)
            )
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        **base_meta,
                        "doc_type": "calendario",
                        "fecha": fecha,
                        "filename": Path(source).stem,
                    },
                )
            )

        # --- Glosario de modalidades ---
        for mod in plan.get("glosario_modalidades", []):
            nombre = mod.get("nombre", "")
            nombre_completo = mod.get("nombre_completo", "")
            header = f"{nombre}" + (f" ({nombre_completo})" if nombre_completo else "")
            text = (
                f"Modalidad: {header}\n"
                f"Tipo: {mod.get('tipo', '')}\n"
                f"Detalles: {mod.get('detalles', '')}\n"
                f"Duración: {mod.get('duracion', '')}"
            )
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        **base_meta,
                        "doc_type": "modalidad",
                        "modalidad": nombre,
                        "filename": Path(source).stem,
                    },
                )
            )

        # --- Actividades fijas Sala C ---
        for act in plan.get("actividades_fijas_sala_c", []):
            text = (
                f"Actividad fija Sala C - {gimnasio} {mes}\n"
                f"Actividad: {act.get('actividad', '')}\n"
                f"Días: {act.get('dias', '')}\n"
                f"Horario: {act.get('horario', '')}"
            )
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        **base_meta,
                        "doc_type": "actividad_fija",
                        "actividad": act.get("actividad", ""),
                        "filename": Path(source).stem,
                    },
                )
            )

        print(f"  ✅ Generados {len(documents)} documentos desde {filepath.name}")
        return documents

    def _get_doc_type(self, filename: str) -> str:
        """Determina el tipo de documento basado en el nombre."""
        if "faq" in filename.lower():
            return "faq"
        elif "manual" in filename.lower():
            return "manual"
        elif "troubleshooting" in filename.lower():
            return "troubleshooting"
        else:
            return "general"
    
    def _generate_doc_id(self, content: str) -> str:
        """Genera un ID único para el documento."""
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Divide documentos en chunks más pequeños."""
        print("✂️  Dividiendo documentos en chunks...")
        
        chunks = self.text_splitter.split_documents(documents)
        
        # Agregar metadatos de chunk
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "chunk_id": i,
                "chunk_size": len(chunk.page_content)
            })
        
        print(f"✅ Creados {len(chunks)} chunks")
        return chunks
    
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """Crea el vectorstore con ChromaDB."""
        print("🔄 Creando vectorstore con ChromaDB...")
        
        # Limpiar directorio anterior si existe
        if self.chroma_path.exists():
            import shutil
            shutil.rmtree(self.chroma_path)
        
        # Crear vectorstore
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=str(self.chroma_path),
            collection_name="helpdesk_knowledge"
        )
        
        print(f"✅ Vectorstore creado en {self.chroma_path}")
        print(f"📊 Total de vectores: {len(documents)}")
        
        return vectorstore
    
    def load_existing_vectorstore(self) -> Chroma:
        """Carga vectorstore existente."""
        if not self.chroma_path.exists():
            raise FileNotFoundError(f"Vectorstore no encontrado en {self.chroma_path}")
        
        vectorstore = Chroma(
            persist_directory=str(self.chroma_path),
            embedding_function=self.embeddings,
            collection_name="helpdesk_knowledge"
        )
        
        return vectorstore
    
    def setup_rag_system(self, force_rebuild: bool = False):
        """Configura el sistema RAG completo."""
        print("🚀 Configurando sistema RAG...")
        
        # Verificar si ya existe y no forzar rebuild
        if self.chroma_path.exists() and not force_rebuild:
            print("📦 Vectorstore existente encontrado")
            return self.load_existing_vectorstore()
        
        # Cargar y procesar documentos
        documents = self.load_documents()
        if not documents:
            print("⚠️  No se encontraron documentos para procesar")
            return None
        
        # Dividir documentos
        chunks = self.split_documents(documents)
        
        # Crear vectorstore
        vectorstore = self.create_vectorstore(chunks)
        
        print("✅ Sistema RAG configurado exitosamente")
        return vectorstore
    
    def test_search(self, vectorstore: Chroma, query: str = "resetear contraseña"):
        """Prueba la funcionalidad de búsqueda."""
        print(f"\n🔍 Probando búsqueda: '{query}'")
        
        results = vectorstore.similarity_search(query, k=3)
        
        for i, doc in enumerate(results, 1):
            print(f"\n📄 Resultado {i}:")
            print(f"Tipo: {doc.metadata.get('doc_type', 'unknown')}")
            print(f"Archivo: {doc.metadata.get('filename', 'unknown')}")
            print(f"Contenido: {doc.page_content[:200]}...")
        
        return results


def main():
    """Función principal para configurar RAG."""
    print("🎧 Configuración RAG - Helpdesk 2.0")
    print("=" * 40)
    
    # Configurar procesador
    processor = DocumentProcessor(docs_path=DOCS_PATH, chroma_path=CHROMADB_PATH)
    
    # Configurar sistema RAG
    vectorstore = processor.setup_rag_system(force_rebuild=True)
    
    if vectorstore:
        # Probar búsquedas relevantes al DIF
        test_queries = [
            "¿Qué clase de GAP hay en enero?",
            "¿Qué actividad hay el 21 de enero en la Sala A?",
            "¿Qué es la modalidad Strong?",
            "¿Cuándo hay Pilates?",
        ]
        
        for query in test_queries:
            processor.test_search(vectorstore, query)
    
    print("\n✅ Configuración completada")


if __name__ == "__main__":
    main()