from __future__ import annotations

from io import BytesIO
from typing import Any, Dict, List

import pandas as pd

from api.config import get_settings
from kurgin_core import (
    analyze_dataframe,
    analyze_stone,
    export_analysis_package,
    export_excel,
    export_pdf,
    get_version_info,
)


def sanitize_json_value(value):
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    return value


def sanitize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    return {str(k): sanitize_json_value(v) for k, v in record.items()}


def summarize_dataframe(df: pd.DataFrame) -> Dict[str, int]:
    total = len(df)
    ok = int((df.get("Calculation Status", pd.Series(dtype=str)) == "OK").sum()) if "Calculation Status" in df.columns else 0
    return {
        "rows_total": total,
        "rows_ok": ok,
        "rows_issues": total - ok,
    }


def analyze_one(stone: Dict[str, Any], language: str = "RU") -> Dict[str, Any]:
    result = analyze_stone(stone, language=language)
    return sanitize_record(result)


def analyze_rows(rows: List[Dict[str, Any]], language: str = "RU"):
    settings = get_settings()
    if len(rows) > settings.max_batch_rows:
        raise ValueError(f"Batch too large: {len(rows)} > {settings.max_batch_rows}")

    df = pd.DataFrame(rows)
    batch = analyze_dataframe(df, language=language)
    summary = summarize_dataframe(batch.dataframe)
    records = [sanitize_record(row) for row in batch.dataframe.to_dict(orient="records")]
    return batch, summary, records


def analyze_excel_bytes(data: bytes, language: str = "RU"):
    df = pd.read_excel(BytesIO(data))
    if len(df) > get_settings().max_batch_rows:
        raise ValueError(f"Batch too large: {len(df)} > {get_settings().max_batch_rows}")
    return analyze_dataframe(df, language=language)


def export_batch_excel(data: bytes, language: str = "RU") -> bytes:
    batch = analyze_excel_bytes(data, language=language)
    return export_excel(batch)


def export_batch_package(data: bytes, language: str = "RU", pdf_mode: str = "all_ok") -> bytes:
    batch = analyze_excel_bytes(data, language=language)
    return export_analysis_package(batch, pdf_mode=pdf_mode)


def export_stone_pdf(stone_result: Dict[str, Any], language: str = "BILINGUAL") -> bytes:
    return export_pdf(stone_result, language=language)


def version_payload() -> Dict[str, Any]:
    payload = get_version_info()
    payload.update({
        "api_version": get_settings().api_version,
        "service_name": get_settings().service_name,
        "environment": get_settings().environment,
    })
    return payload
