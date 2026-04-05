# Changelog

All notable changes merged to `master` are documented automatically.

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

