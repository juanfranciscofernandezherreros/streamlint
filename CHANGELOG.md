# Changelog

All notable changes merged to `master` are documented automatically.

## 2026-04-06

### Update README.md

- **Author:** Juan Francisco Fernandez Herreros
- **Commit:** [`c7ce072`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/c7ce072e0f851af34e29cd323a818e88445af8ab)

**Changed files (1):**

- 🟡 `README.md`

---

## 2026-04-06

### Merge pull request #32 from juanfranciscofernandezherreros/copilot/organize-project-and-add-comments

- **Author:** Juan Francisco Fernandez Herreros
- **Commit:** [`3750b8a`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/3750b8ad23c22f15bebc1ff581face99ef12f957)

**Changed files (3):**

- 🔴 `init_database_vector.py`
- 🟢 `nivel_6_retrievers/23b_chroma_vector_store.py`
- 🟡 `nivel_6_retrievers/README.md`

---

## 2026-04-06

### Initialize vector database and add search functionality

- **Author:** Juan Francisco Fernandez Herreros
- **Commit:** [`6844126`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/68441266a3de23739e13d150abdf459a2925d07b)

**Changed files (1):**

- 🟢 `init_database_vector.py`

---

## 2026-04-06

### Merge pull request #31 from juanfranciscofernandezherreros/copilot/review-memory-manager

- **Author:** Juan Francisco Fernandez Herreros
- **Commit:** [`678a29b`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/678a29b1b4d031d3cced45bb402ab28705ce8c27)

**Changed files (3):**

- 🟡 `README.md`
- 🔄 `nivel_10_memoria_y_evaluacion/57_memory_manager.py`
- 🟡 `nivel_10_memoria_y_evaluacion/README.md`

---

## 2026-04-06

### Create memory_manager.py

- **Author:** Juan Francisco Fernandez Herreros
- **Commit:** [`0451879`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/0451879e968df2be964675dbb215241f7ab8fbd2)

**Changed files (1):**

- 🟢 `memory_manager.py`

---

## 2026-04-06

### PR #30: Add streaming & tool calling scripts, fix nivel 10 doc gaps, add LinkedIn-ready README sections

- **Author:** Juan Francisco Fernandez Herreros
- **Branch:** `copilot/review-project-for-improvement` → `master`
- **Commit:** [`357f24a`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/357f24a4c445057c939b9e99e67c54b69401ead0)

**Description:**

Project review identified two completely missing foundational topics in the learning path and a documentation inconsistency where the README summary table claimed nivel 10 covered scripts 41–48 while files went up to 54.

## New learning scripts

| Script | Topic |
|--------|-------|
| `55_streaming_responses.py` | `stream()`, `astream()`, `astream_events()`, LangGraph `stream_mode="updates"` |
| `56_tool_calling.py` | `@tool`, `bind_tools()`, `ToolNode`, ReAct loop, `with_structured_output()` + Pydantic |

The `calcular` tool in script 56 uses an AST-based safe evaluator instead of `eval()`:

```python
def _evaluar_nodo(nodo: ast.AST) -> float:
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
        return float(nodo.value)
    if isinstance(nodo, ast.BinOp) and type(nodo.op) in _OPERADORES:
        return _OPERADORES[type(nodo.op)](_evaluar_nodo(nodo.left), _evaluar_nodo(nodo.right))
    ...
```

## README.md

- **Badges**: Python 3.10+, LangChain, LangGraph, OpenAI, Streamlit, script/project counters, MIT license
- **Fixed inconsistency**: summary table `41–48` → `41–56`; file tree and execution section updated to match
- **`🎓 Competencias demostradas`**: skills table organized by area, copy-paste ready for LinkedIn profile
- **`🗺️ Roadmap`**: 8 uncovered topics with priority (LangSmith, RAGAS, multimodal/GPT-4o Vision, LangServe, full async, few-shot, semantic caching, Plan-and-Execute)
- **`📣 Comparte en LinkedIn`**: ready-to-paste Spanish post template with hashtags

## nivel_10/README.md

- Documented scripts 49–54 (previously absent from the file)
- Added concepts sections for streaming and tool calling
- Renamed title from vague "Técnicas Avanzadas" to "Memoria, Evaluación, Streaming y Tool Calling"

**Changed files (4):**

- 🟡 `README.md`
- 🟢 `nivel_10_memoria_y_evaluacion/55_streaming_responses.py`
- 🟢 `nivel_10_memoria_y_evaluacion/56_tool_calling.py`
- 🟡 `nivel_10_memoria_y_evaluacion/README.md`

---

## 2026-04-05

### multi chat working

- **Author:** Juan Francisco
- **Commit:** [`55d7907`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/55d7907a90fe3c229ec9034f5563b19fe43a6cf2)

**Changed files (4):**

- 🟡 `nivel_9_proyectos_integradores/multiuser_chat_system/memory_manager.py`
- 🟢 `nivel_9_proyectos_integradores/multiuser_chat_system/users/andony/chats_meta.json`
- 🟢 `nivel_9_proyectos_integradores/multiuser_chat_system/users/andony/chromadb/chroma.sqlite3`
- 🟢 `nivel_9_proyectos_integradores/multiuser_chat_system/users/kiferhe/chromadb/chroma.sqlite3`

---

## 2026-04-05

### PR #29: Update Chroma imports to `import chromadb` + `from langchain_community import Chroma`

- **Author:** Juan Francisco Fernandez Herreros
- **Branch:** `copilot/add-chromadb-imports` → `master`
- **Commit:** [`7aac92f`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/7aac92f19ac91dd2822eead0384c297cd29dc0d5)

**Description:**

Migrates all Chroma vector store imports across the repository to the new import style.

- **5 files** using `from langchain_community.vectorstores import Chroma` → `from langchain_community import Chroma` + `import chromadb`
  - `dif_system/app.py`, `dif_system/setup_rag.py`
  - `helpdesk_system/app.py`, `helpdesk_system/rag_system.py`, `helpdesk_system/setup_rag.py`

- **2 files** using `from langchain_chroma import Chroma` → `from langchain_community import Chroma` (already had `import chromadb`)
  - `nivel_10_memoria_y_evaluacion/48_memoria_vectorial_langgraph.py`
  - `multiuser_chat_system/memory_manager.py`

After:
```python
import chromadb
from langchain_community import Chroma
```

No old-style imports (`langchain_community.vectorstores` or `langchain_chroma`) remain.

**Changed files (7):**

- 🟡 `nivel_10_memoria_y_evaluacion/48_memoria_vectorial_langgraph.py`
- 🟡 `nivel_9_proyectos_integradores/dif_system/app.py`
- 🟡 `nivel_9_proyectos_integradores/dif_system/setup_rag.py`
- 🟡 `nivel_9_proyectos_integradores/helpdesk_system/app.py`
- 🟡 `nivel_9_proyectos_integradores/helpdesk_system/rag_system.py`
- 🟡 `nivel_9_proyectos_integradores/helpdesk_system/setup_rag.py`
- 🟡 `nivel_9_proyectos_integradores/multiuser_chat_system/memory_manager.py`

---

## 2026-04-05

### Merge pull request #28 from juanfranciscofernandezherreros/copilot/explore-memory-management-techniques

- **Author:** Juan Francisco Fernandez Herreros
- **Commit:** [`bf72177`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/bf7217784786dc5c0d9f558751b58359ecb24a60)

**Changed files (7):**

- 🟡 `README.md`
- 🟢 `nivel_10_memoria_y_evaluacion/49_memoria_resumen.py`
- 🟢 `nivel_10_memoria_y_evaluacion/50_memoria_filtrado_inteligente.py`
- 🟢 `nivel_10_memoria_y_evaluacion/51_memoria_limite_tokens.py`
- 🟢 `nivel_10_memoria_y_evaluacion/52_memoria_hibrida_tipo_mensaje.py`
- 🟢 `nivel_10_memoria_y_evaluacion/53_memoria_ventana_adaptativa.py`
- 🟢 `nivel_10_memoria_y_evaluacion/54_memoria_prioridad_contexto.py`

---

## 2026-04-05

### PR #27: Reorganize project after nivel 10 memory course and multiuser chat commit

- **Author:** Juan Francisco Fernandez Herreros
- **Branch:** `copilot/reorganizar-proyecto-ultimo-commit` → `master`
- **Commit:** [`0fa1008`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/0fa10082dfbf3cb0cc0e00fab9198d4f19217afd)

**Description:**

The last commit added `multiuser_chat_system/` at the repo root and 6 unnumbered memory scripts in `nivel_10_memoria_y_evaluacion/`, breaking the established project conventions.

### File moves
- **`multiuser_chat_system/`** → `nivel_9_proyectos_integradores/multiuser_chat_system/` (alongside the other 5 integrating projects)
- **6 unnumbered scripts** in nivel_10 renamed to continue the sequential numbering (43–48):

| Before | After |
|--------|-------|
| `fundamentos_memoria.py` | `43_fundamentos_memoria.py` |
| `fundamentos_memoria_langchain.py` | `44_fundamentos_memoria_langchain.py` |
| `memoria_simple_langraph.py` | `45_memoria_simple_langgraph.py` |
| `memoria_ventana_deslizante.py` | `46_memoria_ventana_deslizante.py` |
| `memoria_persistence_langraph.py` | `47_memoria_persistence_langgraph.py` |
| `memoria_vectorial_langraph.py` | `48_memoria_vectorial_langgraph.py` |

### README updates
- **Root README** — structure tree, learning path (01→48), execution commands, summary table; added missing `dif_system` and new `multiuser_chat_system` project descriptions
- **nivel_9 README** — 5→6 projects, new multiuser_chat_system section
- **nivel_10 README** — 2→8 scripts with full concept documentation for all memory types (LangChain, LangGraph, sliding window, SQLite persistence, vectorial/ChromaDB)

### Note
CodeQL flagged 6 pre-existing `py/path-injection` alerts in `memory_manager.py` — these are unchanged files that were only moved via `git mv`.

**Changed files (14):**

- 🟡 `README.md`
- 🔄 `nivel_10_memoria_y_evaluacion/43_fundamentos_memoria.py`
- 🔄 `nivel_10_memoria_y_evaluacion/44_fundamentos_memoria_langchain.py`
- 🔄 `nivel_10_memoria_y_evaluacion/45_memoria_simple_langgraph.py`
- 🔄 `nivel_10_memoria_y_evaluacion/46_memoria_ventana_deslizante.py`
- 🔄 `nivel_10_memoria_y_evaluacion/47_memoria_persistence_langgraph.py`
- 🔄 `nivel_10_memoria_y_evaluacion/48_memoria_vectorial_langgraph.py`
- 🟡 `nivel_10_memoria_y_evaluacion/README.md`
- 🟡 `nivel_9_proyectos_integradores/README.md`
- 🔄 `nivel_9_proyectos_integradores/multiuser_chat_system/app.py`
- 🔄 `nivel_9_proyectos_integradores/multiuser_chat_system/chatbot.py`
- 🔄 `nivel_9_proyectos_integradores/multiuser_chat_system/config.py`
- 🔄 `nivel_9_proyectos_integradores/multiuser_chat_system/memory_manager.py`
- 🔄 `nivel_9_proyectos_integradores/multiuser_chat_system/utils.py`

---

## 2026-04-05

### nivel 10 memory course and multiuser chat

- **Author:** Juan Francisco
- **Commit:** [`2834d8c`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/2834d8c48269da5ec135f000087179c77413347f)

**Changed files (11):**

- 🟢 `multiuser_chat_system/app.py`
- 🟢 `multiuser_chat_system/chatbot.py`
- 🟢 `multiuser_chat_system/config.py`
- 🟢 `multiuser_chat_system/memory_manager.py`
- 🟢 `multiuser_chat_system/utils.py`
- 🟢 `nivel_10_memoria_y_evaluacion/fundamentos_memoria.py`
- 🟢 `nivel_10_memoria_y_evaluacion/fundamentos_memoria_langchain.py`
- 🟢 `nivel_10_memoria_y_evaluacion/memoria_persistence_langraph.py`
- 🟢 `nivel_10_memoria_y_evaluacion/memoria_simple_langraph.py`
- 🟢 `nivel_10_memoria_y_evaluacion/memoria_vectorial_langraph.py`
- 🟢 `nivel_10_memoria_y_evaluacion/memoria_ventana_deslizante.py`

---

## 2026-04-05

### PR #26: Add GitHub Actions workflow to auto-update CHANGELOG on merge to master

- **Author:** Juan Francisco Fernandez Herreros
- **Branch:** `copilot/update-changes-on-merge` → `master`
- **Commit:** [`44af23b`](https://github.com/juanfranciscofernandezherreros/streamlint/commit/44af23bac8819cf9f3e1f4e06ecb1718fabfac00)

**Description:**

Adds a workflow that triggers on every push to `master` and automatically generates a `CHANGELOG.md` entry with merge metadata.

### What it does
- Detects the associated merged PR (falls back to raw commit info for direct pushes)
- Extracts author, source/target branch, commit link, PR description, and changed files list
- Prepends the entry to `CHANGELOG.md` (creates the file if missing)
- Commits with `[skip ci]` to prevent recursive workflow triggers

### Entry format
Each entry includes:
- Date, PR title/number (or commit message), author, branch flow
- Changed files with status icons (🟢 added, 🟡 modified, 🔴 removed, 🔄 renamed), capped at 20

**Changed files (1):**

- 🟢 `.github/workflows/update-changelog-on-merge.yml`

---

