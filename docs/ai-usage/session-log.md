# AI session log

One entry per phase: what was asked, what went wrong, how it was fixed.

## Phase 1: repo hygiene and scaffold

- **Asked:** add a `.gitignore` (Python, Node, env, SQLite, OS/editor and local working files),
  keep `docs/ai-usage/` tracked, write local assistant rules, and scaffold the backend
  (FastAPI app with `/api/health`, pydantic-settings config, structured logging, ruff and
  pytest config, health test) plus empty `samples/` and `frontend/` folders.
- **What went wrong:** nothing blocking. The machine only has Python 3.14, so the venv uses
  3.14; the project still declares `>=3.11`.
- **How it was fixed:** n/a. Verified with `git check-ignore -v` that `docs/ai-usage/` is not
  ignored and that the working files are, then ran ruff and pytest until green.
