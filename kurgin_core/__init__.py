"""KURGIN Score Analyzer Core SDK.

This package is the stable integration layer for KURGIN Platform.
It is intentionally independent from Streamlit UI.
"""

from .analyzer import (
    analyze_stone,
    analyze_dataframe,
    export_excel,
    export_pdf,
    export_analysis_package,
    get_version_info,
)

__all__ = [
    "analyze_stone",
    "analyze_dataframe",
    "export_excel",
    "export_pdf",
    "export_analysis_package",
    "get_version_info",
]
