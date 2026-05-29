from __future__ import annotations

from pathlib import Path

EXCLUDE_DIRS = {".git", ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache"}

errors = []
for path in Path(".").rglob("*.py"):
    if any(part in EXCLUDE_DIRS for part in path.parts):
        continue
    try:
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
    except Exception as exc:
        errors.append(f"{path}: {exc}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print("Python compile OK")
