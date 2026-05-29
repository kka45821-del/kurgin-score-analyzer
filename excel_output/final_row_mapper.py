from __future__ import annotations

from typing import Any

from excel_output.final_workbook_builder import ANALYZER_RESULTS_COLUMNS, VALIDATION_ERRORS_COLUMNS
from scripts.smoke_final_excel_contract import FORBIDDEN_PUBLIC_COLUMNS, PUBLIC_CATALOG_IMPORT_COLUMNS

READY_STATUSES = {"ready", "warning"}
IMPORTANT_PUBLIC_FIELDS = (
    "stone_id",
    "report_number",
    "shape",
    "carat",
    "color",
    "clarity",
    "table_pct",
    "depth_pct",
    "crown_angle",
    "pavilion_angle",
)

SOURCE_ALIASES = {
    "stone_id": ("stone_id", "StoneID", "id"),
    "report_number": ("report_number", "Report #", "ReportNumber", "certificate_number"),
    "laboratory": ("laboratory", "Lab", "lab"),
    "stock_number": ("stock_number", "Stock #", "StockNumber"),
    "shape": ("shape", "Shape"),
    "carat": ("carat", "Carat", "Weight", "weight"),
    "color": ("color", "Color"),
    "clarity": ("clarity", "Clarity"),
    "measurements": ("measurements", "Measurements", "dimensions"),
    "min_diameter": ("min_diameter", "MinDiameter"),
    "max_diameter": ("max_diameter", "MaxDiameter"),
    "avg_diameter": ("avg_diameter", "AvgDiameter"),
    "depth_mm": ("depth_mm", "DepthMM"),
    "table_pct": ("table_pct", "TablePercent", "Table %"),
    "depth_pct": ("depth_pct", "DepthPercent", "Depth %"),
    "crown_angle": ("crown_angle", "CrownAngle"),
    "crown_height_pct": ("crown_height_pct", "CrownPercent", "CrownHeightPercent"),
    "pavilion_angle": ("pavilion_angle", "PavilionAngle"),
    "pavilion_depth_pct": ("pavilion_depth_pct", "PavilionPercent", "PavilionDepthPercent"),
    "girdle_pct": ("girdle_pct", "GirdlePercent"),
    "fluorescence": ("fluorescence", "Fluorescence"),
    "cut": ("cut", "Cut"),
    "polish": ("polish", "Polish"),
    "symmetry": ("symmetry", "Symmetry"),
}

ANALYSIS_ALIASES = {
    "kurgin_score": ("kurgin_score", "final_score", "score"),
    "score_band": ("score_band", "band"),
    "public_score_label": ("public_score_label", "score_label"),
    "public_summary": ("public_summary", "summary", "short_conclusion"),
    "public_tags": ("public_tags", "tags"),
    "data_quality_status": ("data_quality_status", "data_completeness"),
    "validation_status": ("validation_status",),
    "admin_review_required": ("admin_review_required",),
}


def _first_present(source: dict[str, Any], aliases: tuple[str, ...], default: Any = "") -> Any:
    for alias in aliases:
        value = source.get(alias)
        if value is not None and value != "":
            return value
    return default


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    return False


def _has_insufficient_public_data(source: dict[str, Any], analysis: dict[str, Any]) -> bool:
    mapped_probe = {
        column: _first_present(source, SOURCE_ALIASES.get(column, (column,)))
        for column in IMPORTANT_PUBLIC_FIELDS
    }
    if not _is_missing(_first_present(analysis, ANALYSIS_ALIASES["validation_status"], "")):
        return False
    return any(_is_missing(mapped_probe[field]) for field in IMPORTANT_PUBLIC_FIELDS)


def _normalise_public_tags(value: Any) -> Any:
    if isinstance(value, list):
        return ",".join(str(item) for item in value)
    return value


def _clean_public_row(row: dict[str, Any]) -> dict[str, Any]:
    allowed = set(PUBLIC_CATALOG_IMPORT_COLUMNS)
    forbidden = set(FORBIDDEN_PUBLIC_COLUMNS)
    cleaned = {column: row.get(column, "") for column in PUBLIC_CATALOG_IMPORT_COLUMNS}
    unexpected_forbidden = sorted(forbidden.intersection(row.keys()))
    if unexpected_forbidden:
        raise ValueError(f"Forbidden public columns were mapped: {', '.join(unexpected_forbidden)}")
    return {key: value for key, value in cleaned.items() if key in allowed}


def build_public_catalog_row(source: dict, analysis: dict | None = None) -> dict:
    analysis = analysis or {}
    row: dict[str, Any] = {column: "" for column in PUBLIC_CATALOG_IMPORT_COLUMNS}

    for column, aliases in SOURCE_ALIASES.items():
        row[column] = _first_present(source, aliases, "")

    for column, aliases in ANALYSIS_ALIASES.items():
        row[column] = _first_present(analysis, aliases, row.get(column, ""))

    row["public_tags"] = _normalise_public_tags(row.get("public_tags", ""))
    row["data_quality_status"] = row.get("data_quality_status") or "incomplete"
    row["validation_status"] = row.get("validation_status") or "review_required"

    insufficient_data = _has_insufficient_public_data(source, analysis)
    row["admin_review_required"] = bool(row.get("admin_review_required") or insufficient_data)
    row["show_in_catalog"] = bool(row["validation_status"] in READY_STATUSES and not row["admin_review_required"])
    row["price_status"] = row.get("price_status") or "request_price"
    row["public_action"] = row.get("public_action") or "request_price"
    row["availability_status"] = row.get("availability_status") or "available_to_request"

    return _clean_public_row(row)


def build_analyzer_result_row(source: dict, analysis: dict | None = None) -> dict:
    analysis = analysis or {}
    row = {column: "" for column in ANALYZER_RESULTS_COLUMNS}
    row["row_id"] = _first_present(source, ("row_id", "RowID"), "")
    row["stone_id"] = _first_present(source, SOURCE_ALIASES["stone_id"], "")
    row["report_number"] = _first_present(source, SOURCE_ALIASES["report_number"], "")
    row["kurgin_score"] = _first_present(analysis, ANALYSIS_ALIASES["kurgin_score"], "")
    row["score_band"] = _first_present(analysis, ANALYSIS_ALIASES["score_band"], "")
    row["class"] = _first_present(analysis, ("class", "result_class"), "")
    row["tags"] = _normalise_public_tags(_first_present(analysis, ("tags", "public_tags"), ""))
    row["short_conclusion"] = _first_present(analysis, ("short_conclusion", "summary", "public_summary"), "")
    row["recommendation"] = _first_present(analysis, ("recommendation",), "")
    row["warnings"] = _normalise_public_tags(_first_present(analysis, ("warnings",), ""))
    row["limitations"] = _normalise_public_tags(_first_present(analysis, ("limitations",), ""))
    row["data_completeness"] = _first_present(analysis, ("data_completeness", "data_quality_status"), "")
    row["report_quality"] = _first_present(analysis, ("report_quality",), "")
    row["visual_check"] = _first_present(analysis, ("visual_check",), "")
    row["critical_risk"] = _first_present(analysis, ("critical_risk",), "")
    return row


def build_validation_error_row(
    *,
    row_id: Any = "",
    stone_id: Any = "",
    report_number: Any = "",
    field: str,
    error_code: str,
    severity: str,
    message: str,
    recommended_action: str = "",
    blocks_catalog_import: str | bool = "no",
) -> dict:
    return {
        "row_id": row_id,
        "stone_id": stone_id,
        "report_number": report_number,
        "field": field,
        "error_code": error_code,
        "severity": severity,
        "message": message,
        "recommended_action": recommended_action,
        "blocks_catalog_import": blocks_catalog_import,
    }
