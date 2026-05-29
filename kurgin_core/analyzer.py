from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import pandas as pd

from config_settings.engine_config import ENGINE_VERSION
from excel_tools import (
    create_analysis_package,
    create_excel_output,
    make_analytics,
    process_dataframe,
    process_single_stone,
)
from formula_client.engine_client import get_formula_mode
from report_templates.pdf_single_stone_report import create_single_stone_pdf


CORE_SDK_VERSION = "KURGIN Core SDK v1.11.0"
DEFAULT_REPORT_LEVEL = "Professional Report"


@dataclass
class BatchAnalysis:
    """Container for batch analysis outputs.

    dataframe: full enriched dataframe with KURGIN result fields.
    analytics: summary objects used by Excel/export functions.
    mapping: column recognition dataframe.
    language: analysis language used for localization/interpreting.
    """

    dataframe: pd.DataFrame
    analytics: Dict[str, Any]
    mapping: pd.DataFrame
    language: str = "RU"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataframe": self.dataframe,
            "analytics": self.analytics,
            "mapping": self.mapping,
            "language": self.language,
        }


def analyze_stone(params: Dict[str, Any], language: str = "RU") -> Dict[str, Any]:
    """Analyze one stone and return a plain dict.

    This is the function KURGIN Platform should use for one-card analysis.
    It does not require Streamlit and does not expose internal formula coefficients.
    """
    payload = dict(params or {})
    payload["language"] = language
    result = process_single_stone(payload)
    if hasattr(result, "to_dict"):
        return result.to_dict()
    return dict(result)


def analyze_dataframe(df: pd.DataFrame, language: str = "RU") -> BatchAnalysis:
    """Analyze supplier/catalog dataframe.

    Bad rows do not break the whole file. They are marked with statuses and
    appear in Issues/System sheets during export.
    """
    processed, missing, mapping = process_dataframe(df, language=language)
    # process_dataframe in current architecture converts missing columns into Issues.
    # Keep `missing` compatibility but do not raise here.
    analytics = make_analytics(processed)
    return BatchAnalysis(
        dataframe=processed,
        analytics=analytics,
        mapping=mapping,
        language=language,
    )


def export_excel(batch: BatchAnalysis, report_level: str = DEFAULT_REPORT_LEVEL) -> bytes:
    """Export compact Excel with Results / Details / Issues / System sheets."""
    return create_excel_output(
        batch.dataframe,
        batch.analytics,
        mapping_df=batch.mapping,
        report_level=report_level,
    )


def export_analysis_package(
    batch: BatchAnalysis,
    report_level: str = DEFAULT_REPORT_LEVEL,
    pdf_mode: str = "all_ok",
) -> bytes:
    """Export ZIP package with compact Excel and optional PDF reports.

    pdf_mode:
    - "all_ok": PDF for every successfully calculated stone.
    - "top_only": PDF only for high-priority/top stones.
    - "none": Excel only inside package.
    """
    return create_analysis_package(
        batch.dataframe,
        batch.analytics,
        mapping_df=batch.mapping,
        report_level=report_level,
        pdf_mode=pdf_mode,
    )


def export_pdf(stone_result: Dict[str, Any], language: str = "BILINGUAL") -> bytes:
    """Export one-stone PDF report from an analyzed stone dict."""
    return create_single_stone_pdf(stone_result, language=language)


def get_version_info() -> Dict[str, Any]:
    """Return stable version metadata for UI/backend health checks."""
    return {
        "core_sdk_version": CORE_SDK_VERSION,
        "engine_version": ENGINE_VERSION,
        "formula_mode": get_formula_mode(),
        "default_report_level": DEFAULT_REPORT_LEVEL,
    }
