from __future__ import annotations

from pathlib import Path

bad = []

for path in Path(".").rglob("*"):
    parts = set(path.parts)
    if ".git" in parts:
        continue
    if "__pycache__" in parts:
        bad.append(str(path))
    if path.suffix in {".pyc", ".pyo", ".pyd"}:
        bad.append(str(path))

# Generated outputs should not be committed to repository root.
for pattern in ["*.zip", "*.xlsx", "*.xls", "*.pdf", "*.csv"]:
    for path in Path(".").glob(pattern):
        bad.append(str(path))

if bad:
    print("Repository hygiene issues:")
    for item in bad[:200]:
        print(" -", item)
    raise SystemExit(1)

print("Repository hygiene OK")
