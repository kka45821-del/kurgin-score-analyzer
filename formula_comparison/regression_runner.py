from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List

import pandas as pd

from data_models.stone import StoneInput
from excel_processing.column_mapping import apply_column_mapping
from excel_processing.field_enrichment import enrich_dataframe_fields
from excel_processing.upload_quality import add_upload_quality_columns
from formula_modules.measurement_spread.spread_engine import add_measurement_spread_columns
from formula_modules.measurement_spread.diameter_policy import add_diameter_policy_columns
from formula_modules.interpretation.score_band_interpreter import get_score_band_label, get_score_band_key
from validation.input_validator import REQUIRED_COLUMNS, validate_row

from formula_comparison.version_loader import list_versions, load_formula


def _empty(value) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    return text == "" or text.lower() in {"nan", "none", "—", "-"}


def _missing_required(row) -> List[str]:
    return [col for col in REQUIRED_COLUMNS if _empty(row.get(col))]


def _load_table(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported dataset format: {path.suffix}")


def prepare_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    mapped, mapping = apply_column_mapping(df)
    enriched = enrich_dataframe_fields(mapped)
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in enriched.columns]
    for col in missing_cols:
        enriched[col] = None
    enriched = add_upload_quality_columns(enriched, mapping_df=mapping)
    enriched = add_measurement_spread_columns(enriched)
    enriched = add_diameter_policy_columns(enriched)
    if "Report #" not in enriched.columns:
        enriched["Report #"] = [f"row_{i+1}" for i in range(len(enriched))]
    if "Shape" not in enriched.columns:
        enriched["Shape"] = "ROUND"
    return enriched, mapping


def _row_identity(row, index):
    return {
        "row_index": index + 1,
        "case_id": row.get("Case ID", "") or row.get("case_id", "") or f"row_{index+1}",
        "stock": row.get("Stock #", ""),
        "report_number": row.get("Report #", ""),
        "shape": row.get("Shape", ""),
        "weight": row.get("Weight", ""),
        "color": row.get("Color", ""),
        "clarity": row.get("Clarity", ""),
        "measurements": row.get("Measurements", ""),
        "upload_quality_status": row.get("Upload Quality Status", ""),
        "geometry_status": row.get("Geometry Status", ""),
        "measurement_parse_status": row.get("Measurement Parse Status", ""),
        "measurement_warning": row.get("Measurement Warning", ""),
    }


def _status_for_row(row):
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

    errors = validate_row(row)
    if errors:
        return "VALIDATION_ERROR", "; ".join(errors)

    return "OK", ""


def run_regression(df: pd.DataFrame, versions: Iterable[str] | None = None) -> pd.DataFrame:
    prepared, mapping = prepare_dataset(df)
    if versions is None:
        versions = list_versions(active_only=True)
    versions = list(versions)

    loaded = {version: load_formula(version) for version in versions}
    rows = []

    for index, row in prepared.iterrows():
        base = _row_identity(row, index)
        status, reason = _status_for_row(row)
        result_row = dict(base)
        result_row["input_status"] = status
        result_row["input_issue"] = reason

        if status == "OK":
            stone = StoneInput.from_row(row)
            engine_kwargs = stone.to_engine_kwargs()
            for version, module in loaded.items():
                try:
                    if hasattr(module, "calculate_with_row"):
                        result = module.calculate_with_row(row, engine_kwargs)
                    else:
                        result = module.calculate(engine_kwargs)
                    score = result.get("final_score")
                    verdict = result.get("final_verdict")
                    result_row[f"{version}_status"] = "OK"
                    result_row[f"{version}_score"] = score
                    result_row[f"{version}_band_ru"] = get_score_band_label(score, language="RU")
                    result_row[f"{version}_band_key"] = get_score_band_key(score)
                    result_row[f"{version}_verdict"] = verdict
                    result_row[f"{version}_triple_score"] = result.get("triple_score")
                    result_row[f"{version}_structure_modifier"] = result.get("structure_modifier")
                    result_row[f"{version}_visual_check"] = result.get("visual_check")
                    result_row[f"{version}_critical_risk"] = result.get("critical_risk")
                    result_row[f"{version}_tags"] = ", ".join(result.get("structure_tags", []))
                    result_row[f"{version}_engine_version"] = result.get("engine_version")
                    # Candidate/experimental metadata, when available.
                    for extra_key in [
                        "candidate_mode",
                        "candidate_base_score",
                        "candidate_public_score",
                        "candidate_public_band_key",
                        "candidate_public_band_ru",
                        "candidate_class_cap",
                        "candidate_class_cap_ru",
                        "candidate_cap_reason",
                        "candidate_cap_applied",
                    ]:
                        if extra_key in result:
                            result_row[f"{version}_{extra_key}"] = result.get(extra_key)
                except Exception as exc:
                    result_row[f"{version}_status"] = "ERROR"
                    result_row[f"{version}_error"] = str(exc)
        else:
            for version in versions:
                result_row[f"{version}_status"] = status
                result_row[f"{version}_score"] = None
                result_row[f"{version}_band_ru"] = ""
                result_row[f"{version}_band_key"] = ""
                result_row[f"{version}_verdict"] = reason

        rows.append(result_row)

    report = pd.DataFrame(rows)

    # Comparison columns when current + another version exist.
    if "current" in versions:
        for version in versions:
            if version == "current":
                continue
            if f"{version}_score" in report.columns:
                report[f"delta_{version}_vs_current"] = report[f"{version}_score"] - report["current_score"]
                report[f"band_changed_{version}_vs_current"] = report[f"{version}_band_key"] != report["current_band_key"]
                report[f"verdict_changed_{version}_vs_current"] = report[f"{version}_verdict"] != report["current_verdict"]

    return report


def summarize_regression(report: pd.DataFrame, versions: Iterable[str]) -> pd.DataFrame:
    rows = []
    total = len(report)
    rows.append({"Metric": "Total rows", "Value": total, "Notes": ""})
    rows.append({"Metric": "OK input rows", "Value": int((report["input_status"] == "OK").sum()), "Notes": ""})
    rows.append({"Metric": "Non-OK input rows", "Value": int((report["input_status"] != "OK").sum()), "Notes": ""})

    if "current_score" in report.columns:
        ok = report[report["current_status"] == "OK"]
        rows.append({"Metric": "Current average score", "Value": round(ok["current_score"].mean(), 3) if not ok.empty else "", "Notes": ""})
        rows.append({"Metric": "Current Elite/Premium count", "Value": int(ok["current_band_key"].isin(["elite", "premium"]).sum()), "Notes": ""})

    for col in report.columns:
        if col.startswith("delta_") and col.endswith("_vs_current"):
            rows.append({"Metric": f"{col} avg", "Value": round(report[col].dropna().mean(), 4) if report[col].notna().any() else "", "Notes": ""})
        if col.startswith("band_changed_"):
            rows.append({"Metric": col, "Value": int(report[col].fillna(False).sum()), "Notes": "band changed count"})
        if col.startswith("verdict_changed_"):
            rows.append({"Metric": col, "Value": int(report[col].fillna(False).sum()), "Notes": "verdict changed count"})

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description="Run KURGIN formula regression comparison.")
    parser.add_argument("--input", required=True, help="Path to golden dataset .xlsx/.csv")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument("--summary", default=None, help="Optional summary CSV path")
    parser.add_argument("--versions", nargs="*", default=None, help="Formula version ids from registry")
    args = parser.parse_args()

    df = _load_table(args.input)
    versions = args.versions or list_versions(active_only=True)
    report = run_regression(df, versions=versions)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(args.output, index=False)

    if args.summary:
        summary = summarize_regression(report, versions=versions)
        summary.to_csv(args.summary, index=False)

    print(json.dumps({
        "input": args.input,
        "output": args.output,
        "summary": args.summary,
        "rows": len(report),
        "versions": versions,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
