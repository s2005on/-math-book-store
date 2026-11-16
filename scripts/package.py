from __future__ import annotations
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
if not VERSION or any(ch not in "0123456789." for ch in VERSION):
    raise ValueError("VERSION không hợp lệ")
ARCHIVE = DIST / f"LTDs-Book-Store-v{VERSION}.zip"
EXCLUDED_DIRS = {".git", ".venv", "__pycache__", "node_modules", "dist", ".pytest_cache"}
EXCLUDED_FILES = {".env", "shop.sqlite3"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}

def main() -> None:
    DIST.mkdir(exist_ok=True)
    if ARCHIVE.exists():
        ARCHIVE.unlink()
    count = 0
    with ZipFile(ARCHIVE, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            if any(part in EXCLUDED_DIRS for part in rel.parts):
                continue
            if path.name in EXCLUDED_FILES or path.suffix in EXCLUDED_SUFFIXES:
                continue
            if rel.parts and rel.parts[0] == "server" and len(rel.parts) > 1 and rel.parts[1] == "data":
                continue
            archive.write(path, Path("LTDs-Book-Store") / rel)
            count += 1
    print(f"Created {ARCHIVE} with {count} files ({ARCHIVE.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
