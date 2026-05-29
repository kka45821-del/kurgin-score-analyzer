from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from excel_output.final_row_mapper import (
    build_analyzer_result_row,
    build_public_catalog_row,
    build_validation_error_row,
)
from excel_output.final_workbook_builder import build_final_workbook
from scripts.smoke_final_excel_contract import (
    FORBIDDEN_PUBLIC_COLUMNS,
    PUBLIC_CATALOG_IMPORT_COLUMNS,
    validate_workbook,
)


def _sample_source() -> dict:
    return {
        "row_id": 1,
        "stone_id": "KRG-MAP-001",
        "Report #": "LG987654321",
        "Lab": "IGI",
        "Stock #": "MAP-STOCK-001",
        "Shape": "Round",
        "Weight": 1.51,
        "Color": "E",
        "Clarity": "VS1",
        "Measurements": "7.30x7.33x4.50",
        "min_diameter": 7.30,
        "max_diameter": 7.33,
        "avg_diameter": 7.315,
        "depth_mm": 4.50,
        "TablePercent": 57.0,
        "DepthPercent": 61.6,
        "CrownAngle": 34.5,
        "CrownPercent": 15.0,
        "PavilionAngle": 40.8,
        "PavilionPercent": 43.0,
        "GirdlePercent": 3.5,
        "Fluorescence": "None",
        "Cut": "Excellent",
        "Polish": "Excellent",
        "Symmetry": "Excellent",
    }


def _sample_analysis() -> dict:
    return {
        "final_score": 89.2,
        "score_band": "high",
        "score_label": "High",
        "summary": "Controlled public-safe mapped summary.",
        "tags": ["balanced", "reviewed"],
        "data_completeness": "complete",
        "validation_status": "ready",
        "admin_review_required": False,
        "class": "controlled",
        "recommendation": "Ready for admin import smoke.",
        "warnings": [],
        "limitations": ["Not a certificate", "Not an appraisal"],
        "report_quality": "good",
        "visual_check": False,
        "critical_risk": False,
    }


def main() -> int:
    source = _sample_source()
    analysis = _sample_analysis()

    public_row = build_public_catalog_row(source, analysis)
    assert set(public_row.keys()).issubset(set(PUBLIC_CATALOG_IMPORT_COLUMNS)), public_row.keys()
    assert set(public_row.keys()) == set(PUBLIC_CATALOG_IMPORT_COLUMNS), public_row.keys()
    for forbidden_column in FORBIDDEN_PUBLIC_COLUMNS:
        assert forbidden_column not in public_row, forbidden_column
    assert public_row["price_status"] == "request_price", public_row
    assert public_row["public_action"] == "request_price", public_row
    assert public_row["availability_status"] == "available_to_request", public_row

    analyzer_row = build_analyzer_result_row(source, analysis)
    validation_row = build_validation_error_row(
        row_id=source["row_id"],
        stone_id=source["stone_id"],
        report_number=source["Report #"],
        field="public_summary",
        error_code="review_note",
        severity="warning",
        message="Example mapper warning.",
        recommended_action="Review mapped public summary before publishing.",
        blocks_catalog_import="no",
    )

    workbook = build_final_workbook(
        public_rows=[public_row],
        analyzer_rows=[analyzer_row],
        validation_rows=[validation_row],
        diagnostics_rows=[],
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        workbook_path = Path(tmpdir) / "final_row_mapper_smoke.xlsx"
        workbook.save(workbook_path)
        errors = validate_workbook(workbook_path)
        if errors:
            print("Final row mapper smoke failed contract validation:")
            for error in errors:
                print(f"- {error}")
            return 1

    print("Final row mapper smoke passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
