# Changelog

All notable changes merged to `master` are documented automatically.

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

