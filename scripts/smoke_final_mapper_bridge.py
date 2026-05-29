from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from excel_output.final_mapper_bridge import (
    build_final_rows_from_analysis,
    build_final_workbook_from_analysis_rows,
)
from scripts.smoke_final_excel_contract import validate_workbook

INTERNAL_FIELDS = {
    "raw_formula",
    "weights",
    "diagnostics",
    "breakdown",
    "debug_trace",
    "formula_thresholds",
}


def _sample_source() -> dict:
    return {
        "row_id": 1,
        "stone_id": "KRG-BRIDGE-001",
        "Report #": "LG1122334455",
        "Lab": "IGI",
        "Stock #": "BRIDGE-STOCK-001",
        "Shape": "Round",
        "Weight": 1.4,
        "Color": "E",
        "Clarity": "VS1",
        "Measurements": "7.10x7.12x4.38",
        "min_diameter": 7.10,
        "max_diameter": 7.12,
        "avg_diameter": 7.11,
        "depth_mm": 4.38,
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
        "final_score": 90.1,
        "score_band": "high",
        "score_label": "High",
        "summary": "Bridge public-safe summary.",
        "tags": ["balanced", "bridge-smoke"],
        "data_completeness": "complete",
        "validation_status": "ready",
        "admin_review_required": False,
        "class": "controlled",
        "recommendation": "Ready for bridge smoke.",
        "warnings": [],
        "limitations": ["Not a certificate", "Not an appraisal"],
        "report_quality": "good",
        "visual_check": False,
        "critical_risk": False,
        "triple_score": 91.0,
        "structure_modifier": 0.99,
        "diagnostics": "internal diagnostics must stay internal",
        "breakdown": "internal breakdown must stay internal",
        "engine_version": "bridge-smoke",
        "calculation_status": "mock",
        "internal_warnings": "internal only",
        "raw_formula": "must not reach public row",
        "weights": {"secret": 1},
        "debug_trace": ["secret"],
        "formula_thresholds": {"secret": 1},
    }


def main() -> int:
    source = _sample_source()
    analysis = _sample_analysis()
    final_rows = build_final_rows_from_analysis(source, analysis)

    public_row = final_rows["public_row"]
    diagnostics_row = final_rows["diagnostics_row"]

    for field in INTERNAL_FIELDS:
        assert field not in public_row, f"Internal field leaked into public_row: {field}"

    assert diagnostics_row["diagnostics"] == analysis["diagnostics"], diagnostics_row
    assert diagnostics_row["breakdown"] == analysis["breakdown"], diagnostics_row
    assert diagnostics_row["triple_score"] == analysis["triple_score"], diagnostics_row
    assert diagnostics_row["structure_modifier"] == analysis["structure_modifier"], diagnostics_row

    workbook = build_final_workbook_from_analysis_rows([(source, analysis)])
    with tempfile.TemporaryDirectory() as tmpdir:
        workbook_path = Path(tmpdir) / "final_mapper_bridge_smoke.xlsx"
        workbook.save(workbook_path)
        errors = validate_workbook(workbook_path)
        if errors:
            print("Final mapper bridge smoke failed contract validation:")
            for error in errors:
                print(f"- {error}")
            return 1

    print("Final mapper bridge smoke passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
