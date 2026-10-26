import subprocess
import sys

FORBIDDEN = ("sqlalchemy", "fastapi", "starlette", "app.db", "app.api")


def test_parsing_imports_no_db_or_web_modules() -> None:
    # A fresh interpreter, so modules imported by other tests do not leak in.
    code = (
        "import sys, app.parsing; "
        f"bad = [m for m in sys.modules if m.startswith({FORBIDDEN!r})]; "
        "print(','.join(bad))"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )

    assert result.stdout.strip() == ""
