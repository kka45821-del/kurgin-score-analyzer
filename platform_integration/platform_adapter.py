from __future__ import annotations

from typing import Any, Dict, List


PUBLIC_STABLE_FIELDS = [
    "Calculation Status",
    "Kurgin Score",
    "Verdict Local",
    "score_band_label_ru",
    "tags_all",
    "tag1",
    "tag2",
    "tag3",
    "tag4",
    "tag5",
    "tag6",
    "interpretation_short_ru",
    "recommendation_ru",
    "warning_ru",
    "Report #",
    "Lab",
    "Shape",
    "Weight",
    "Color",
    "Clarity",
    "Measurements",
    "AvgDiameter",
    "VisualSpreadStatus",
    "DiameterSymmetryStatus",
    "Upload Quality Status",
    "Geometry Status",
    "PDF Report Status",
    "Engine Version",
    "Formula Output Version",
]

EXPERIMENTAL_FIELDS = [
    "AdjustedKURGINScorePreview",
    "AdjustedScoreBandPreview",
    "DiameterSpreadModifierPreview",
    "ScoreClassCapPreview",
    "Diameter Policy Status",
    "Diameter Policy Action",
    "Diameter Policy Reason",
    "High Score Diameter Flag",
]


def _safe(value: Any, default: str = ""):
    if value is None:
        return default
    text = str(value).strip()
    if text.lower() in {"nan", "none", "—", "-"}:
        return default
    return value


def _score(value):
    try:
        return round(float(value), 2)
    except Exception:
        return None


def _tags(result: Dict[str, Any]) -> List[str]:
    tags = []
    for col in ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]:
        val = _safe(result.get(col), "")
        if val:
            tags.append(str(val))
    if not tags:
        raw = _safe(result.get("tags_all") or result.get("Tags Local") or result.get("Tags"), "")
        if raw:
            tags = [item.strip() for item in str(raw).replace(";", ",").split(",") if item.strip()]
    return tags


def build_platform_card_payload(result: Dict[str, Any], include_experimental: bool = True) -> Dict[str, Any]:
    """Convert one analyzed stone result into a stable Platform Tools card payload."""
    status = str(result.get("Calculation Status", ""))
    report_number = _safe(result.get("Report #"), "")
    lab = _safe(result.get("Lab"), "")
    shape = _safe(result.get("Shape"), "")
    score = _score(result.get("Kurgin Score"))

    card = {
        "kind": "kurgin_score_result_card",
        "schema_version": "KURGIN Platform Card v1.12.1",
        "status": status,
        "identity": {
            "report_number": report_number,
            "lab": lab,
            "stock_number": _safe(result.get("Stock #"), ""),
            "stone_title": _safe(result.get("Stone Title"), ""),
        },
        "stone": {
            "shape": shape,
            "weight": _safe(result.get("Weight"), ""),
            "color": _safe(result.get("Color"), ""),
            "clarity": _safe(result.get("Clarity"), ""),
            "measurements": _safe(result.get("Measurements"), ""),
        },
        "score": {
            "value": score,
            "scale": 100,
            "class_ru": _safe(result.get("score_band_label_ru") or result.get("Verdict Local"), ""),
            "verdict": _safe(result.get("Verdict Local") or result.get("Verdict"), ""),
        },
        "tags": _tags(result),
        "summary": {
            "short_ru": _safe(result.get("interpretation_short_ru"), ""),
            "recommendation_ru": _safe(result.get("recommendation_ru"), ""),
            "warning_ru": _safe(result.get("warning_ru"), ""),
        },
        "measurements": {
            "avg_diameter": _safe(result.get("AvgDiameter"), ""),
            "visual_spread_status": _safe(result.get("VisualSpreadStatus"), ""),
            "diameter_symmetry_status": _safe(result.get("DiameterSymmetryStatus"), ""),
        },
        "quality": {
            "upload_quality_status": _safe(result.get("Upload Quality Status"), ""),
            "geometry_status": _safe(result.get("Geometry Status"), ""),
            "report_quality_status": _safe(result.get("Report Quality Status"), ""),
        },
        "report": {
            "pdf_status": _safe(result.get("PDF Report Status"), ""),
            "pdf_file": _safe(result.get("PDF Report File"), ""),
        },
        "version": {
            "engine_version": _safe(result.get("Engine Version"), ""),
            "formula_output_version": _safe(result.get("Formula Output Version"), ""),
        },
        "actions": {
            "can_show_score": status == "OK",
            "can_generate_pdf": str(result.get("PDF Report Status", "")) == "ready_to_generate",
            "needs_review": status != "OK" or bool(result.get("High Score Diameter Flag") is True),
        },
    }

    if include_experimental:
        card["experimental"] = {
            "adjusted_score_preview": _score(result.get("AdjustedKURGINScorePreview")),
            "adjusted_class_preview": _safe(result.get("AdjustedScoreBandPreview"), ""),
            "score_class_cap_preview": _safe(result.get("ScoreClassCapPreview"), ""),
            "diameter_policy_status": _safe(result.get("Diameter Policy Status"), ""),
            "diameter_policy_action": _safe(result.get("Diameter Policy Action"), ""),
            "diameter_policy_reason": _safe(result.get("Diameter Policy Reason"), ""),
            "high_score_diameter_flag": bool(result.get("High Score Diameter Flag") is True),
        }

    return card


def filter_public_result(result: Dict[str, Any], include_experimental: bool = False) -> Dict[str, Any]:
    """Return only stable public fields, optionally with experimental preview fields."""
    fields = PUBLIC_STABLE_FIELDS + (EXPERIMENTAL_FIELDS if include_experimental else [])
    return {field: result.get(field) for field in fields if field in result}
