from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from excel_output.final_workbook_builder import build_empty_final_workbook
from scripts.smoke_final_excel_contract import validate_workbook


def main() -> int:
    workbook = build_empty_final_workbook()

    with tempfile.TemporaryDirectory() as tmpdir:
        workbook_path = Path(tmpdir) / "final_workbook_builder_smoke.xlsx"
        workbook.save(workbook_path)
        errors = validate_workbook(workbook_path)

    if errors:
        print("Final workbook builder smoke failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Final workbook builder smoke passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
