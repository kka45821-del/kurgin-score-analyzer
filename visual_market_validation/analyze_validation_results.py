from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

import pandas as pd


REQUIRED_REVIEW_FIELDS = [
    "Review ID",
    "Report #",
    "Reviewer",
    "Media Available",
    "Visual Size Rating",
    "Brightness Rating",
    "Fire Rating",
    "Pattern/Symmetry Rating",
    "Marketability",
    "Jeweler Decision",
    "Candidate Cap Decision",
    "Recommended Public Class",
]

CONTROL_QUEUE_REASONS = {"HIGH_SCORE_CONTROL"}
CAP_QUEUE_REASONS = {"CAP_APPLIED"}


def _norm(value):
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "none", "—", "-"}:
        return ""
    return text


def _read_validation_form(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    df = pd.read_excel(path, sheet_name="Validation Form")
    return df.where(pd.notna(df), "")


def _read_review_queue(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    try:
        df = pd.read_excel(path, sheet_name="Review Queue")
        return df.where(pd.notna(df), "")
    except Exception:
        return pd.DataFrame()


def validate_required_fields(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        missing = [field for field in REQUIRED_REVIEW_FIELDS if not _norm(row.get(field))]
        rows.append({
            "Review ID": row.get("Review ID", ""),
            "Report #": row.get("Report #", ""),
            "Missing Required Fields": ", ".join(missing),
            "Is Complete": len(missing) == 0,
        })
    return pd.DataFrame(rows)


def merge_queue_context(form_df: pd.DataFrame, queue_df: pd.DataFrame) -> pd.DataFrame:
    if queue_df.empty or "Review ID" not in queue_df.columns:
        out = form_df.copy()
        if "Queue Reason" not in out.columns:
            out["Queue Reason"] = ""
        return out

    context_cols = [
        col for col in [
            "Review ID", "Priority", "Queue Reason", "Current Score", "Current Class",
            "Candidate Score", "Candidate Class", "Delta", "Band Changed",
            "Cap Applied", "Cap Reason", "Measurement Status", "Measurement Warning"
        ] if col in queue_df.columns
    ]
    merged = form_df.merge(queue_df[context_cols], on="Review ID", how="left", suffixes=("", "_Queue"))
    return merged.where(pd.notna(merged), "")


def compute_summary(merged: pd.DataFrame, completeness: pd.DataFrame) -> pd.DataFrame:
    total = len(merged)
    complete = int(completeness["Is Complete"].sum()) if "Is Complete" in completeness.columns else 0
    incomplete = total - complete

    cap_decisions = merged.get("Candidate Cap Decision", pd.Series(dtype=str)).astype(str).str.strip()
    agree = int((cap_decisions == "Agree").sum())
    disagree = int((cap_decisions == "Disagree").sum())
    needs = int((cap_decisions == "Needs more data").sum())

    queue_reason = merged.get("Queue Reason", pd.Series(dtype=str)).astype(str)
    cap_rows = merged[queue_reason.isin(CAP_QUEUE_REASONS)]
    control_rows = merged[queue_reason.isin(CONTROL_QUEUE_REASONS)]

    cap_completed = cap_rows[cap_rows.get("Candidate Cap Decision", pd.Series(dtype=str)).astype(str).str.strip() != ""]
    control_completed = control_rows[control_rows.get("Candidate Cap Decision", pd.Series(dtype=str)).astype(str).str.strip() != ""]

    cap_agree_rate = ""
    if len(cap_completed):
        cap_agree_rate = round(float((cap_completed["Candidate Cap Decision"].astype(str).str.strip() == "Agree").mean()), 3)

    control_false_concern = ""
    if len(control_completed):
        # False concern for controls means reviewer thinks cap should be applied/recommended public class lower than current
        control_false_concern = int((control_completed["Candidate Cap Decision"].astype(str).str.strip() == "Agree").sum())

    rows = [
        ("Total review rows", total, "All rows in Validation Form"),
        ("Complete rows", complete, "Rows with all required review fields"),
        ("Incomplete rows", incomplete, "Rows needing completion"),
        ("Candidate cap Agree", agree, "Reviewer agrees with cap"),
        ("Candidate cap Disagree", disagree, "Reviewer disagrees with cap"),
        ("Needs more data", needs, "Cannot decide without better media"),
        ("Cap rows completed", len(cap_completed), "CAP_APPLIED queue rows with a decision"),
        ("Cap agree rate", cap_agree_rate, "Share of completed cap rows where reviewer agrees"),
        ("Control rows completed", len(control_completed), "HIGH_SCORE_CONTROL rows with a decision"),
        ("Control false concern count", control_false_concern, "Controls where cap concern appears incorrectly supported"),
    ]
    return pd.DataFrame(rows, columns=["Metric", "Value", "Notes"])


def decision_recommendation(summary_df: pd.DataFrame) -> Dict[str, Any]:
    lookup = {str(row["Metric"]): row["Value"] for _, row in summary_df.iterrows()}

    total = int(lookup.get("Total review rows", 0) or 0)
    complete = int(lookup.get("Complete rows", 0) or 0)
    incomplete = int(lookup.get("Incomplete rows", 0) or 0)
    cap_completed = int(lookup.get("Cap rows completed", 0) or 0)
    cap_agree_rate = lookup.get("Cap agree rate", "")
    needs_more = int(lookup.get("Needs more data", 0) or 0)
    control_false = lookup.get("Control false concern count", "")
    control_false = int(control_false) if str(control_false).strip() not in {"", "nan"} else 0

    if total == 0:
        return {
            "Decision": "NO DATA",
            "Recommendation": "Fill validation workbook before making formula decision.",
            "Reason": "Validation Form is empty.",
        }

    if complete < max(5, int(total * 0.6)):
        return {
            "Decision": "INSUFFICIENT DATA",
            "Recommendation": "Continue visual/market review.",
            "Reason": f"Only {complete}/{total} rows are complete.",
        }

    if cap_completed == 0:
        return {
            "Decision": "INSUFFICIENT CAP REVIEW",
            "Recommendation": "Review cap-applied cases before formula decision.",
            "Reason": "No completed CAP_APPLIED rows.",
        }

    if needs_more > max(2, int(total * 0.25)):
        return {
            "Decision": "NEEDS MORE MEDIA",
            "Recommendation": "Collect better photos/videos before deciding.",
            "Reason": "Too many rows marked Needs more data.",
        }

    try:
        cap_rate = float(cap_agree_rate)
    except Exception:
        cap_rate = None

    if cap_rate is not None and cap_rate >= 0.70 and control_false == 0:
        return {
            "Decision": "PASS FOR PUBLIC CLASS CAP",
            "Recommendation": "Candidate v2 class-cap logic can move to final regression/promotion review.",
            "Reason": f"Cap agree rate is {cap_rate:.0%}, controls show no false concern.",
        }

    if cap_rate is not None and cap_rate < 0.50:
        return {
            "Decision": "REVISE CANDIDATE",
            "Recommendation": "Class-cap rules appear too strict or wrong.",
            "Reason": f"Cap agree rate is only {cap_rate:.0%}.",
        }

    return {
        "Decision": "MIXED REVIEW",
        "Recommendation": "Inspect disagree/needs-more-data rows and adjust rules before promotion.",
        "Reason": "Validation signal is not strong enough for promotion.",
    }


def analyze_validation_workbook(path: str | Path) -> Dict[str, pd.DataFrame]:
    form_df = _read_validation_form(path)
    queue_df = _read_review_queue(path)
    completeness = validate_required_fields(form_df)
    merged = merge_queue_context(form_df, queue_df)
    summary = compute_summary(merged, completeness)
    decision = pd.DataFrame([decision_recommendation(summary)])
    issues = completeness[completeness["Is Complete"] == False].copy()

    return {
        "Summary": summary,
        "Decision": decision,
        "Validation Rows": merged,
        "Completion Issues": issues,
        "Completeness": completeness,
    }


def export_analysis_outputs(workbook_path: str | Path, output_dir: str | Path) -> Dict[str, str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results = analyze_validation_workbook(workbook_path)

    paths = {}
    for name, df in results.items():
        filename = name.lower().replace(" ", "_") + ".csv"
        path = output_dir / filename
        df.to_csv(path, index=False)
        paths[name] = str(path)

    decision = results["Decision"].iloc[0].to_dict() if not results["Decision"].empty else {}
    md = [
        "# KURGIN Visual Validation Results",
        "",
        f"Workbook: `{workbook_path}`",
        "",
        "## Decision",
        "",
        f"- **Decision:** {decision.get('Decision', '')}",
        f"- **Recommendation:** {decision.get('Recommendation', '')}",
        f"- **Reason:** {decision.get('Reason', '')}",
        "",
        "## Summary",
        "",
        results["Summary"].to_markdown(index=False),
    ]
    md_path = output_dir / "visual_validation_results.md"
    md_path.write_text("\\n".join(md), encoding="utf-8")
    paths["Markdown"] = str(md_path)

    manifest_path = output_dir / "visual_validation_results_manifest.json"
    manifest_path.write_text(json.dumps(paths, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["Manifest"] = str(manifest_path)
    return paths


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze filled KURGIN visual/market validation workbook.")
    parser.add_argument("--input", required=True, help="Filled validation workbook .xlsx")
    parser.add_argument("--output-dir", required=True, help="Output directory for analysis files")
    args = parser.parse_args()

    outputs = export_analysis_outputs(args.input, args.output_dir)
    print(json.dumps(outputs, ensure_ascii=False, indent=2))
