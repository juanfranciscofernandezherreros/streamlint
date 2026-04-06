"""
57_memory_manager.py
--------------------
Gestor de memoria híbrido que combina tres estrategias en una sola clase.

Este módulo integra en un único ``MemoryManager`` las tres estrategias
de memoria más habituales en agentes conversacionales:

1. **SlidingWindowMemory** — ventana deslizante de los últimos N mensajes.
2. **SummaryMemory**       — resumen progresivo generado por el LLM.
3. **VectorMemory**        — búsqueda semántica sobre el historial con ChromaDB.

El método ``get_context()`` construye el contexto óptimo para cada turno
combinando las tres fuentes y recortando al límite de tokens configurado.

Ejecutar:
    python nivel_10_memoria_y_evaluacion/57_memory_manager.py
"""

from typing import List, Dict
from collections import deque
import os

from dotenv import load_dotenv

# =========================
# LLM + Embeddings
# =========================

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import chromadb
from langchain_community.vectorstores import Chroma

import tiktoken

load_dotenv()


# =========================
# Utils
# =========================

def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))


# =========================
# Sliding Window Memory
# =========================

class SlidingWindowMemory:
    def __init__(self, max_messages: int = 10):
        self.messages = deque(maxlen=max_messages)

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get(self) -> List[Dict]:
        return list(self.messages)


# =========================
# Summary Memory (LLM)
# =========================

class SummaryMemory:
    def __init__(self, llm):
        self.summary = ""
        self.llm = llm

    def update(self, new_messages: List[Dict]):
        text = "\n".join([f"{m['role']}: {m['content']}" for m in new_messages])

        prompt = f"""
Actualiza este resumen de conversación:

Resumen actual:
{self.summary}

Nueva información:
{text}

Devuelve un resumen actualizado, corto y claro.
"""

        response = self.llm.invoke(prompt)
        self.summary = response.content

    def get(self) -> str:
        return self.summary


# =========================
# Vector Memory (Chroma)
# =========================

class VectorMemory:
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.embeddings = OpenAIEmbeddings()
        self.db = Chroma(
            persist_directory=persist_dir,
            embedding_function=self.embeddings
        )

    def add(self, text: str):
        self.db.add_texts([text])

    def search(self, query: str, k: int = 3) -> List[str]:
        docs = self.db.similarity_search(query, k=k)
        return [d.page_content for d in docs]


# =========================
# Memory Manager
# =========================

class MemoryManager:
    def __init__(
        self,
        max_tokens: int = 1500,
        window_size: int = 10,
    ):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        self.short_term = SlidingWindowMemory(window_size)
        self.long_term = VectorMemory()
        self.summary = SummaryMemory(self.llm)

        self.max_tokens = max_tokens

    # -------------------------
    # Update memory
    # -------------------------
    def update(self, user_input: str, ai_output: str):
        # Short-term
        self.short_term.add("user", user_input)
        self.short_term.add("assistant", ai_output)

        # Long-term
        self.long_term.add(user_input)

        # Summary
        self.summary.update([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": ai_output},
        ])

    # -------------------------
    # Build context
    # -------------------------
    def get_context(self, query: str) -> List[Dict]:
        context = []

        # 1. Summary (alta prioridad)
        summary_text = self.summary.get()
        if summary_text:
            context.append({
                "role": "system",
                "content": f"Resumen conversación: {summary_text}"
            })

        # 2. Short-term
        context.extend(self.short_term.get())

        # 3. Long-term (semantic search)
        results = self.long_term.search(query)
        for r in results:
            context.append({
                "role": "system",
                "content": f"Contexto relevante: {r}"
            })

        # 4. Trim tokens
        return self._trim_to_token_limit(context)

    # -------------------------
    # Token trimming
    # -------------------------
    def _trim_to_token_limit(self, messages: List[Dict]) -> List[Dict]:
        total_tokens = 0
        trimmed = []

        for msg in reversed(messages):
            tokens = count_tokens(msg["content"])
            if total_tokens + tokens > self.max_tokens:
                break
            trimmed.append(msg)
            total_tokens += tokens

        return list(reversed(trimmed))


# =========================
# Example usage
# =========================

if __name__ == "__main__":
    mm = MemoryManager(max_tokens=800, window_size=6)

    # Simulación conversación
    mm.update(
        "Estoy construyendo un agente con memoria",
        "Perfecto, ¿qué tipo de memoria estás usando?"
    )

    mm.update(
        "Uso LangChain y LangGraph",
        "Buena combinación para memoria avanzada"
    )

    mm.update(
        "Quiero optimizar el contexto",
        "Puedes usar resumen + vector + ventana"
    )

    # Nueva pregunta
    context = mm.get_context("memoria")

    print("\n=== CONTEXT ===\n")
    for msg in context:
        print(f"{msg['role'].upper()}: {msg['content']}\n")
