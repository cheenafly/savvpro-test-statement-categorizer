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

## Phase 2: taxonomy, domain models and database

- **Asked:** move work to a `candidate-<username>` branch and reset local `main` to upstream;
  add the Schedule C taxonomy (`categories.yaml` + validated, cached loader), pure domain types,
  SQLAlchemy 2.0 models with money stored as integer cents, API schemas that serialize money as
  strings, `GET /api/categories`, and tests that never touch `data/app.db`.
- **What went wrong:**
  - The scaffold commit had been made on `main` instead of a candidate branch.
  - A column named `date` with `Mapped[date]` would shadow the `date` type inside the class body,
    which breaks under Python 3.14's lazily evaluated annotations.
  - A plain `TestClient(create_app())` would run the lifespan `init_db` against the default
    engine and could create `data/app.db` during tests.
  - Starlette warns about `httpx` vs `httpx2` on every test run.
- **How it was fixed:**
  - Branched to `candidate-cheenafly` and pointed local `main` back at `origin/main`.
  - Used `import datetime as dt` and `Mapped[dt.date]` in the ORM and schema modules.
  - `create_app` accepts an `engine`; tests use an in-memory `StaticPool` engine with `get_db`
    overridden, and `conftest.py` sets `DATABASE_URL=sqlite://` before any app import as a backstop.
  - Enabled `PRAGMA foreign_keys=ON` per SQLite connection so `ON DELETE CASCADE` really works
    (covered by a test that deletes via raw SQL).
  - Filtered only that exact Starlette message in pytest config.
