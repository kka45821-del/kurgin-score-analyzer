from __future__ import annotations

from typing import Any, Mapping

from kurgin_core import analyze_stone

from platform_integration.public_safe_analyzer_adapter import to_public_safe_analyzer_result


PUBLIC_INPUT_FIELD_MAP = {
    "shape": "Shape",
    "carat": "Weight",
    "color": "Color",
    "clarity": "Clarity",
    "table_pct": "TablePercent",
    "depth_pct": "DepthPercent",
    "crown_angle": "CrownAngle",
    "pavilion_angle": "PavilionAngle",
    "crown_height": "CrownPercent",
    "pavilion_depth": "PavilionPercent",
    "girdle": "GirdlePercent",
    "fluorescence": "Fluorescence Intensity",
    "report_number": "Report #",
}

_REQUIRED_GEOMETRY_FIELDS = (
    "table_pct",
    "depth_pct",
    "crown_angle",
    "pavilion_angle",
    "crown_height",
    "pavilion_depth",
    "girdle",
)

_SUPPORTED_SHAPE = "ROUND"


def analyze_public_preview(public_input: dict, language: str = "RU") -> dict:
    """Return a public-safe Analyzer preview payload for future Tools integration.

    The function accepts public-facing field names, maps them to the Analyzer SDK
    input shape, calls the existing Analyzer SDK, and sanitizes the raw result
    through the public-safe adapter before returning anything to callers.
    """
    if not isinstance(public_input, Mapping):
        return to_public_safe_analyzer_result({
            "status": "error",
            "message": "Public preview input is malformed.",
        })

    normalized = _normalize_public_input(public_input)
    shape = str(normalized.get("shape") or "").strip().upper()
    if shape and shape != _SUPPORTED_SHAPE:
        return to_public_safe_analyzer_result({
            "status": "UNSUPPORTED_SHAPE",
            "reason": f"Shape {shape} is not supported by current public preview model",
        })

    missing = _missing_geometry(normalized)
    if missing:
        return to_public_safe_analyzer_result({
            "status": "MISSING_GEOMETRY",
            "message": "Missing required geometry fields: " + ", ".join(missing),
        })

    analyzer_input = _to_analyzer_input(normalized)
    try:
        raw_result = analyze_stone(analyzer_input, language=_normalize_language(language))
    except Exception:
        return to_public_safe_analyzer_result({
            "status": "error",
            "message": "Analyzer public preview is unavailable.",
        })

    return to_public_safe_analyzer_result(raw_result)


def _normalize_public_input(public_input: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key).strip().lower(): _normalize_value(value) for key, value in public_input.items()}


def _normalize_value(value: Any) -> Any:
    if isinstance(value, str):
        text = value.strip()
        return text if text else None
    return value


def _missing_geometry(normalized: Mapping[str, Any]) -> list[str]:
    return [field for field in _REQUIRED_GEOMETRY_FIELDS if _is_empty(normalized.get(field))]


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    return text == "" or text.lower() in {"nan", "none", "—", "-"}


def _to_analyzer_input(normalized: Mapping[str, Any]) -> dict[str, Any]:
    analyzer_input: dict[str, Any] = {}
    for public_field, analyzer_field in PUBLIC_INPUT_FIELD_MAP.items():
        value = normalized.get(public_field)
        if not _is_empty(value):
            analyzer_input[analyzer_field] = value
    if "Shape" not in analyzer_input:
        analyzer_input["Shape"] = _SUPPORTED_SHAPE
    return analyzer_input


def _normalize_language(language: str) -> str:
    normalized = str(language or "RU").strip().upper()
    return normalized if normalized in {"RU", "EN", "BILINGUAL"} else "RU"
