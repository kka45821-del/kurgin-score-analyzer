from __future__ import annotations

from datetime import datetime, timezone

from openpyxl import Workbook

from scripts.smoke_final_excel_contract import (
    FORBIDDEN_PUBLIC_COLUMNS,
    PUBLIC_CATALOG_IMPORT_COLUMNS,
    REQUIRED_SHEETS,
)

CONTRACT_NAME = "FINAL_ANALYZER_EXCEL_OUTPUT_CONTRACT"
CONTRACT_VERSION = "0.1"
ADMIN_IMPORT_SHEET = "PUBLIC_CATALOG_IMPORT"

ANALYZER_RESULTS_COLUMNS = [
    "row_id",
    "stone_id",
    "report_number",
    "kurgin_score",
    "score_band",
    "class",
    "tags",
    "short_conclusion",
    "recommendation",
    "warnings",
    "limitations",
    "data_completeness",
    "report_quality",
    "visual_check",
    "critical_risk",
]

VALIDATION_ERRORS_COLUMNS = [
    "row_id",
    "stone_id",
    "report_number",
    "field",
    "error_code",
    "severity",
    "message",
    "recommended_action",
    "blocks_catalog_import",
]

INTERNAL_DIAGNOSTICS_COLUMNS = [
    "row_id",
    "stone_id",
    "report_number",
    "triple_score",
    "structure_modifier",
    "diagnostics",
    "breakdown",
    "engine_version",
    "calculation_status",
    "internal_warnings",
]

README_SCHEMA_COLUMNS = [
    "contract_name",
    "contract_version",
    "generated_at",
    "analyzer_version",
    "engine_version",
    "admin_import_sheet",
    "required_sheets",
]


def _reset_workbook_to_required_sheets(workbook: Workbook) -> None:
    active_sheet = workbook.active
    active_sheet.title = ADMIN_IMPORT_SHEET
    for sheet_name in REQUIRED_SHEETS:
        if sheet_name == ADMIN_IMPORT_SHEET:
            continue
        workbook.create_sheet(sheet_name)


def _append_header(workbook: Workbook, sheet_name: str, columns: list[str]) -> None:
    workbook[sheet_name].append(columns)


def _append_dict_rows(workbook: Workbook, sheet_name: str, columns: list[str], rows: list[dict] | None) -> None:
    if not rows:
        return
    sheet = workbook[sheet_name]
    for row in rows:
        sheet.append([row.get(column, "") for column in columns])


def _validate_public_rows(public_rows: list[dict]) -> None:
    forbidden = set(FORBIDDEN_PUBLIC_COLUMNS)
    for index, row in enumerate(public_rows, start=1):
        forbidden_keys = sorted(forbidden.intersection(row.keys()))
        if forbidden_keys:
            raise ValueError(
                "PUBLIC_CATALOG_IMPORT row "
                f"{index} contains forbidden public columns: {', '.join(forbidden_keys)}"
            )


def _populate_readme_schema(workbook: Workbook) -> None:
    sheet = workbook["README_SCHEMA"]
    sheet.append(README_SCHEMA_COLUMNS)
    sheet.append([
        CONTRACT_NAME,
        CONTRACT_VERSION,
        datetime.now(timezone.utc).isoformat(),
        "pending",
        "pending",
        ADMIN_IMPORT_SHEET,
        ",".join(REQUIRED_SHEETS),
    ])


def build_empty_final_workbook() -> Workbook:
    """Build an empty final Analyzer workbook matching contract v0.1.

    This skeleton does not run the formula, change Analyzer scoring, or alter the
    existing Excel/PDF report generators. It only creates the required workbook
    structure and headers for future Admin/Catalog import work.
    """
    workbook = Workbook()
    _reset_workbook_to_required_sheets(workbook)

    _append_header(workbook, ADMIN_IMPORT_SHEET, PUBLIC_CATALOG_IMPORT_COLUMNS)
    _append_header(workbook, "ANALYZER_RESULTS", ANALYZER_RESULTS_COLUMNS)
    _append_header(workbook, "VALIDATION_ERRORS", VALIDATION_ERRORS_COLUMNS)
    _append_header(workbook, "INTERNAL_DIAGNOSTICS", INTERNAL_DIAGNOSTICS_COLUMNS)
    _populate_readme_schema(workbook)

    return workbook


def build_final_workbook(
    public_rows: list[dict],
    analyzer_rows: list[dict] | None = None,
    validation_rows: list[dict] | None = None,
    diagnostics_rows: list[dict] | None = None,
) -> Workbook:
    """Build a final Analyzer workbook from already prepared safe rows.

    This function only writes rows into the final contract workbook. It does not
    calculate the formula, mutate the existing Excel generator, or touch PDF/report
    generation.
    """
    _validate_public_rows(public_rows)

    workbook = build_empty_final_workbook()
    _append_dict_rows(workbook, ADMIN_IMPORT_SHEET, PUBLIC_CATALOG_IMPORT_COLUMNS, public_rows)
    _append_dict_rows(workbook, "ANALYZER_RESULTS", ANALYZER_RESULTS_COLUMNS, analyzer_rows)
    _append_dict_rows(workbook, "VALIDATION_ERRORS", VALIDATION_ERRORS_COLUMNS, validation_rows)
    _append_dict_rows(workbook, "INTERNAL_DIAGNOSTICS", INTERNAL_DIAGNOSTICS_COLUMNS, diagnostics_rows)
    return workbook
