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

## Phase 3: statement parser and fake samples

- **Asked:** a pure parser (no DB/web imports) for CSV and XLSX bank and card statements. It had
  to cover header and synonym detection below junk lines, Decimal-only amount parsing, a
  per-column date order, sign normalization (debit/credit, DR/CR type, card auto-detect with an
  override), summary/blank/pending rows and row-level errors. Also a deterministic generator
  for four invented sample statements, plus tests.
- **What went wrong:**
  - `\u` escapes I wrote (unicode minus, non-breaking space, BOM) were turned into literal
    invisible characters on the way into the files. That gave unreadable source and ruff
    ambiguous-character errors.
  - The first summary-row check would have treated any row with a "TOTAL" cell as a footer.
    That would drop real purchases at merchants named "TOTAL ...".
  - The skipped-row warning named the `OPENING BALANCE` row by its date cell, not the matched text.
  - The CR/DR regex used `\b`, so it missed `45.00CR` written without a space.
  - My own header test expected `Amount ($)` to be unmapped, but it correctly maps to `amount`.
  - The xlsx sample looked deterministic in two quick runs but was not: openpyxl writes the
    current time into `docProps/core.xml` on save.
  - zsh aborted a command because of an unquoted `--include=*.py` glob.
- **How it was fixed:**
  - Rewrote the affected characters as ASCII `\uXXXX` escapes (or `codecs.BOM_UTF8`) with a
    script that builds the backslash via `chr(92)`, and checked with `grep -P '[^\x00-\x7F]'`.
  - TOTAL rows are only skipped when the date cell is blank or invalid. Balance rows must match
    the whole cell. A test keeps a dated `TOTAL WINE` purchase.
  - The warning now reports the matched cell, and the marker regex anchors on a digit or `)`.
  - Fixed the test expectation and used `Amt` as the unknown-header case.
  - The generator now pins both the zip entry times and `dcterms:modified`. A test regenerates
    the samples into a temp dir and compares bytes with the committed files.
  - Added a subprocess test that importing `app.parsing` loads no SQLAlchemy/FastAPI modules.
    pandas turned out to be unused and was removed from the dependencies.
