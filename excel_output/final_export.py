from __future__ import annotations

from io import BytesIO
from pathlib import Path

from excel_output.final_mapper_bridge import build_final_workbook_from_analysis_rows


def export_final_excel(rows: list[tuple[dict, dict]], output_path: str | Path) -> Path:
    """Export final Analyzer Excel workbook to a filesystem path.

    This entrypoint only uses already prepared source rows and sanitized/mock
    analysis rows. It does not run the formula, alter the legacy Excel generator,
    touch PDF/report generation, or connect to UI.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook = build_final_workbook_from_analysis_rows(rows)
    workbook.save(path)
    return path


def build_final_excel_bytes(rows: list[tuple[dict, dict]]) -> bytes:
    """Build final Analyzer Excel workbook bytes for future controlled download flows."""
    workbook = build_final_workbook_from_analysis_rows(rows)
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()
