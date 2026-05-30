from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd

from data_models.stone import StoneInput
from excel_processing.column_mapping import apply_column_mapping
from excel_processing.field_enrichment import enrich_dataframe_fields
from excel_processing.upload_quality import add_upload_quality_columns
from formula_client.cloud_client import calculate_stone_cloud
from formula_client.local_client import calculate_stone_local
from formula_modules.measurement_spread.diameter_policy import add_diameter_policy_columns
from formula_modules.measurement_spread.spread_engine import add_measurement_spread_columns
from validation.input_validator import REQUIRED_COLUMNS, validate_row


SKIP_MESSAGE = "Local-vs-cloud equivalence skipped: FORMULA_API_URL or FORMULA_API_KEY not configured"
GOLDEN_DATASET_PATH = Path("golden_dataset/golden_dataset_template.csv")

TOLERANCE_FINAL_SCORE = 0.01
TOLERANCE_TRIPLE_SCORE = 0.01
TOLERANCE_STRUCTURE_MODIFIER = 0.0001


def _empty(value) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    return text == "" or text.lower() in {"nan", "none", "—", "-"}


def _missing_required(row) -> list[str]:
    return [col for col in REQUIRED_COLUMNS if _empty(row.get(col))]


def _input_status(row) -> tuple[str, str]:
    shape = str(row.get("Shape", "ROUND")).upper()
    if shape != "ROUND":
        return "UNSUPPORTED_SHAPE", f"Shape {shape} is not supported by current ROUND model"

    missing = _missing_required(row)
    if len(missing) == len(REQUIRED_COLUMNS):
        return "CATALOG_DATA_ONLY", "Missing all required geometry fields: " + ", ".join(missing)
    if missing:
        return "MISSING_GEOMETRY", "Missing required geometry fields: " + ", ".join(missing)

    possible_scale = str(row.get("Possible Scale Issues", "") or "").strip()
    if possible_scale:
        return "POSSIBLE_SCALE_ISSUE", possible_scale

    validation_errors = validate_row(row)
    if validation_errors:
        return "VALIDATION_ERROR", "; ".join(validation_errors)

    return "OK", ""


def _prepare_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Golden dataset not found: {path}")

    df = pd.read_csv(path)
    mapped, mapping = apply_column_mapping(df)
    enriched = enrich_dataframe_fields(mapped)

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in enriched.columns]
    for col in missing_cols:
        enriched[col] = None

    enriched = add_upload_quality_columns(enriched, mapping_df=mapping)
    enriched = add_measurement_spread_columns(enriched)
    enriched = add_diameter_policy_columns(enriched)

    if "Report #" not in enriched.columns:
        enriched["Report #"] = [f"row_{i + 1}" for i in range(len(enriched))]
    if "Shape" not in enriched.columns:
        enriched["Shape"] = "ROUND"

    return enriched


def _row_identity(row, index: int) -> dict:
    return {
        "row_index": index + 1,
        "case_id": row.get("Case ID", "") or row.get("case_id", "") or f"row_{index + 1}",
        "stock": row.get("Stock #", ""),
        "report_number": row.get("Report #", ""),
        "shape": row.get("Shape", ""),
    }


def _float_delta(left, right) -> float:
    return abs(float(left) - float(right))


def _compare_result(local_result: dict, cloud_result: dict, identity: dict) -> list[dict]:
    discrepancies = []

    comparisons = [
        ("final_score", TOLERANCE_FINAL_SCORE, "SCORE_DELTA"),
        ("triple_score", TOLERANCE_TRIPLE_SCORE, "TRIPLE_DELTA"),
        ("structure_modifier", TOLERANCE_STRUCTURE_MODIFIER, "MODIFIER_DELTA"),
    ]
    for field, tolerance, issue_type in comparisons:
        delta = _float_delta(local_result.get(field), cloud_result.get(field))
        if delta > tolerance:
            discrepancies.append({
                **identity,
                "issue_type": issue_type,
                "field": field,
                "local": local_result.get(field),
                "cloud": cloud_result.get(field),
                "delta": delta,
                "tolerance": tolerance,
            })

    exact_fields = [
        ("final_verdict", "VERDICT_CHANGED"),
        ("visual_check", "FLAG_CHANGED"),
        ("critical_risk", "FLAG_CHANGED"),
        ("structure_tags", "TAG_CHANGED"),
    ]
    for field, issue_type in exact_fields:
        if local_result.get(field) != cloud_result.get(field):
            discrepancies.append({
                **identity,
                "issue_type": issue_type,
                "field": field,
                "local": local_result.get(field),
                "cloud": cloud_result.get(field),
                "delta": "",
                "tolerance": "exact",
            })

    return discrepancies


def _safe_summary(summary: dict) -> str:
    return json.dumps(summary, ensure_ascii=False, sort_keys=True)


def main() -> int:
    endpoint = os.getenv("FORMULA_API_URL", "").strip()
    api_key = os.getenv("FORMULA_API_KEY", "").strip()

    if not endpoint or not api_key:
        print(SKIP_MESSAGE)
        return 0

    df = _prepare_dataset(GOLDEN_DATASET_PATH)

    rows_checked = 0
    rows_skipped = 0
    max_score_delta = 0.0
    max_triple_delta = 0.0
    max_modifier_delta = 0.0
    discrepancies: list[dict] = []

    for index, row in df.iterrows():
        identity = _row_identity(row, index)
        status, reason = _input_status(row)
        if status != "OK":
            rows_skipped += 1
            continue

        try:
            engine_kwargs = StoneInput.from_row(row).to_engine_kwargs()
            local_result = calculate_stone_local(engine_kwargs)
            cloud_result = calculate_stone_cloud(engine_kwargs, endpoint=endpoint, api_key=api_key)
        except Exception as exc:
            discrepancies.append({
                **identity,
                "issue_type": "EXECUTION_ERROR",
                "field": "calculation",
                "local": "",
                "cloud": "",
                "delta": "",
                "tolerance": "",
                "error": str(exc),
            })
            continue

        rows_checked += 1
        score_delta = _float_delta(local_result.get("final_score"), cloud_result.get("final_score"))
        triple_delta = _float_delta(local_result.get("triple_score"), cloud_result.get("triple_score"))
        modifier_delta = _float_delta(local_result.get("structure_modifier"), cloud_result.get("structure_modifier"))

        max_score_delta = max(max_score_delta, score_delta)
        max_triple_delta = max(max_triple_delta, triple_delta)
        max_modifier_delta = max(max_modifier_delta, modifier_delta)

        discrepancies.extend(_compare_result(local_result, cloud_result, identity))

    summary = {
        "status": "ok" if not discrepancies else "failed",
        "dataset": str(GOLDEN_DATASET_PATH),
        "rows_checked": rows_checked,
        "rows_skipped": rows_skipped,
        "max_score_delta": round(max_score_delta, 6),
        "max_triple_delta": round(max_triple_delta, 6),
        "max_modifier_delta": round(max_modifier_delta, 8),
        "discrepancies": len(discrepancies),
        "tolerance": {
            "final_score": TOLERANCE_FINAL_SCORE,
            "triple_score": TOLERANCE_TRIPLE_SCORE,
            "structure_modifier": TOLERANCE_STRUCTURE_MODIFIER,
            "final_verdict": "exact",
            "visual_check": "exact",
            "critical_risk": "exact",
            "structure_tags": "exact",
        },
    }

    print("Local-vs-cloud formula equivalence summary")
    print(_safe_summary(summary))

    if discrepancies:
        preview = discrepancies[:20]
        print("Local-vs-cloud discrepancies preview")
        print(_safe_summary({"items": preview, "truncated": len(discrepancies) > len(preview)}))
        return 1

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Local-vs-cloud equivalence failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
