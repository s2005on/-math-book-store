"""Verify the ZIP produced from VERSION contains the runnable app and no local secrets."""
from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
ARCHIVE = ROOT / "dist" / f"Math-Book-Store-v{VERSION}.zip"
PREFIX = "Math-Book-Store/"
REQUIRED = {
    "VERSION", "README.md", "start.py", "RUN-WINDOWS.bat",
    "server/app.py", "server/requirements.txt", "server/web/index.html",
    "server/web/app.js", "server/web/admin.html", "server/web/catalog.json",
}


def main() -> None:
    if not ARCHIVE.is_file():
        raise SystemExit(f"Missing archive: {ARCHIVE}")
    with ZipFile(ARCHIVE) as z:
        if z.testzip() is not None:
            raise SystemExit("ZIP has a corrupt entry")
        names = set(z.namelist())
        if not all(n.startswith(PREFIX) for n in names):
            raise SystemExit("Unexpected file outside the ZIP application folder")
        if {PREFIX + p for p in REQUIRED} - names:
            raise SystemExit("ZIP missing required application files")
        for name in names:
            path = name[len(PREFIX):]
            if (
                path == ".env" or path.startswith(".venv/")
                or path.startswith("server/data/")
                or path.endswith(".sqlite3")
                or "__pycache__" in path
            ):
                raise SystemExit(f"Sensitive/runtime file leaked into ZIP: {name}")
        if z.read(PREFIX + "VERSION").decode("utf-8").strip() != VERSION:
            raise SystemExit("ZIP version does not match VERSION")
    print(f"Verified {ARCHIVE.name} ({len(names)} files)")


if __name__ == "__main__":
    main()
