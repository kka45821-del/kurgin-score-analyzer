from __future__ import annotations

from typing import Any

from excel_output.final_row_mapper import (
    build_analyzer_result_row,
    build_public_catalog_row,
    build_validation_error_row,
)
from excel_output.final_workbook_builder import build_final_workbook

IDENTITY_FIELDS = ("stone_id", "report_number")
SCORE_FIELDS = ("kurgin_score", "final_score", "score")
DIAGNOSTICS_FIELDS = (
    "triple_score",
    "structure_modifier",
    "diagnostics",
    "breakdown",
    "engine_version",
    "calculation_status",
    "internal_warnings",
)

SOURCE_ID_ALIASES = {
    "stone_id": ("stone_id", "StoneID", "id"),
    "report_number": ("report_number", "Report #", "ReportNumber", "certificate_number"),
    "row_id": ("row_id", "RowID"),
}


def _first_present(data: dict[str, Any], aliases: tuple[str, ...], default: Any = "") -> Any:
    for alias in aliases:
        value = data.get(alias)
        if value is not None and value != "":
            return value
    return default


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    return False


def _source_identity(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "row_id": _first_present(source, SOURCE_ID_ALIASES["row_id"], ""),
        "stone_id": _first_present(source, SOURCE_ID_ALIASES["stone_id"], ""),
        "report_number": _first_present(source, SOURCE_ID_ALIASES["report_number"], ""),
    }


def _has_score(analysis: dict[str, Any]) -> bool:
    return any(not _is_missing(analysis.get(field)) for field in SCORE_FIELDS)


def _validation_rows_for(source: dict[str, Any], analysis: dict[str, Any], public_row: dict[str, Any]) -> list[dict[str, Any]]:
    identity = _source_identity(source)
    validation_rows: list[dict[str, Any]] = []

    if _is_missing(identity["stone_id"]) and _is_missing(identity["report_number"]):
        validation_rows.append(
            build_validation_error_row(
                row_id=identity["row_id"],
                stone_id=identity["stone_id"],
                report_number=identity["report_number"],
                field="stone_id/report_number",
                error_code="missing_required_identity",
                severity="blocker",
                message="Missing both stone_id and report_number.",
                recommended_action="Add stable stone_id or report_number before Admin import.",
                blocks_catalog_import="yes",
            )
        )

    validation_status = public_row.get("validation_status", "")
    if validation_status != "ready":
        validation_rows.append(
            build_validation_error_row(
                row_id=identity["row_id"],
                stone_id=identity["stone_id"],
                report_number=identity["report_number"],
                field="validation_status",
                error_code="validation_status_not_ready",
                severity="review",
                message=f"validation_status is {validation_status or 'empty'}, not ready.",
                recommended_action="Review source and Analyzer output before publication.",
                blocks_catalog_import="no",
            )
        )

    if not _has_score(analysis):
        validation_rows.append(
            build_validation_error_row(
                row_id=identity["row_id"],
                stone_id=identity["stone_id"],
                report_number=identity["report_number"],
                field="kurgin_score",
                error_code="score_missing",
                severity="review",
                message="Analyzer score is missing.",
                recommended_action="Run or review Analyzer result before scored publication.",
                blocks_catalog_import="no",
            )
        )

    return validation_rows


def _diagnostics_row_for(source: dict[str, Any], analysis: dict[str, Any]) -> dict[str, Any]:
    identity = _source_identity(source)
    row = {
        "row_id": identity["row_id"],
        "stone_id": identity["stone_id"],
        "report_number": identity["report_number"],
    }
    for field in DIAGNOSTICS_FIELDS:
        row[field] = analysis.get(field, "")
    return row


def build_final_rows_from_analysis(source: dict, analysis: dict) -> dict:
    """Bridge one source/analyzer pair into final Excel contract rows.

    Internal diagnostics remain only in diagnostics_row. Public row is built through
    the public contract mapper and therefore stays restricted to public catalog
    columns.
    """
    analysis = analysis or {}
    public_row = build_public_catalog_row(source, analysis)
    analyzer_row = build_analyzer_result_row(source, analysis)
    validation_rows = _validation_rows_for(source, analysis, public_row)
    diagnostics_row = _diagnostics_row_for(source, analysis)

    return {
        "public_row": public_row,
        "analyzer_row": analyzer_row,
        "validation_rows": validation_rows,
        "diagnostics_row": diagnostics_row,
    }


def build_final_workbook_from_analysis_rows(rows: list[tuple[dict, dict]]):
    public_rows: list[dict] = []
    analyzer_rows: list[dict] = []
    validation_rows: list[dict] = []
    diagnostics_rows: list[dict] = []

    for source, analysis in rows:
        final_rows = build_final_rows_from_analysis(source, analysis)
        public_rows.append(final_rows["public_row"])
        analyzer_rows.append(final_rows["analyzer_row"])
        validation_rows.extend(final_rows["validation_rows"])
        diagnostics_rows.append(final_rows["diagnostics_row"])

    return build_final_workbook(
        public_rows=public_rows,
        analyzer_rows=analyzer_rows,
        validation_rows=validation_rows,
        diagnostics_rows=diagnostics_rows,
    )
