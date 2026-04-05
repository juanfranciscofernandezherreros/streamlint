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
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200
        )

    def _load_json_file(self, filepath: Path) -> List[Document]:
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        
        plan = data.get("plan_maestro", data)
        mes = plan.get("mes", "Enero")
        gimnasio = plan.get("gimnasio", "DIF")
        documents = []

        # Procesar calendario con fechas legibles para el buscador
        for entry in plan.get("calendario_diario", []):
            fecha_iso = entry.get("fecha", "")
            # Convertir 2026-01-21 -> 21 de Enero
            dia_num = fecha_iso.split("-")[-1]
            fecha_texto = f"{dia_num} de {mes}"
            
            content = f"Gimnasio: {gimnasio}\nFecha: {fecha_iso} ({fecha_texto})\n"
            content += f"Sala A: {entry.get('sala_a')}\n"
            content += f"Sala B: {entry.get('sala_b')}\n"
            content += f"Sala C: {entry.get('sala_c')}\n"
            if entry.get("observaciones"):
                content += f"Notas: {entry.get('observaciones')}"
            
            documents.append(Document(page_content=content, metadata={"tipo": "calendario", "fecha": fecha_iso}))

        # Procesar glosario
        for mod in plan.get("glosario_modalidades", []):
            text = f"Modalidad: {mod.get('nombre')}\nTipo: {mod.get('tipo')}\nDetalles: {mod.get('detalles')}\nDuración: {mod.get('duracion')}"
            if mod.get("nombre_completo"):
                text += f"\nNombre completo: {mod.get('nombre_completo')}"
            documents.append(Document(page_content=text, metadata={"tipo": "modalidad"}))

        # Procesar actividades fijas de Sala C
        for act in plan.get("actividades_fijas_sala_c", []):
            text = (
                f"Actividad fija Sala C: {act.get('actividad')}\n"
                f"Días: {act.get('dias')}\n"
                f"Horario: {act.get('horario')}"
            )
            documents.append(Document(page_content=text, metadata={"tipo": "actividad_fija"}))

        return documents

    def run_setup(self):
        print("🚀 Procesando documentos...")
        docs = []
        for f in Path(DOCS_PATH).glob("*.json"):
            docs.extend(self._load_json_file(f))
        
        chunks = self.text_splitter.split_documents(docs)
        Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=CHROMADB_PATH
        )
        print(f"✅ Vectorstore creado con {len(chunks)} fragmentos.")

if __name__ == "__main__":
    DocumentProcessor().run_setup()