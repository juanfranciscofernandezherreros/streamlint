# Changelog

All notable changes merged to `master` are documented automatically.

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

