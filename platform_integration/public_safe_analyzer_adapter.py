from __future__ import annotations

from typing import Any, Mapping


PUBLIC_LIMITATIONS = [
    "Не является сертификатом.",
    "Не является оценкой стоимости.",
    "Не является геммологическим заключением.",
]

NEXT_ACTION = "request_professional_review"

ALLOWED_PUBLIC_FIELDS = {
    "status",
    "score_band",
    "summary",
    "warnings",
    "limitations",
    "next_action",
}

BLOCKED_INTERNAL_FIELDS = {
    "diagnostics",
    "breakdown",
    "triple_score",
    "structure_modifier",
    "raw_formula",
    "weights",
    "penalty_breakdown",
    "internal_diagnostics",
    "debug_trace",
    "traceback",
    "exception",
    "raw_engine_output",
    "formula_source",
    "coefficient_formula",
    "certificate_claim",
    "appraisal_claim",
    "price_effect",
    "order_effect",
    "reserve_effect",
    "payment_effect",
}

_UNSUPPORTED_MARKERS = (
    "unsupported",
    "unsupported_shape",
    "not supported",
    "shape is not supported",
    "version is in development",
    "версия находится в разработке",
)

_INCOMPLETE_MARKERS = (
    "incomplete",
    "missing",
    "missing_geometry",
    "catalog_data_only",
    "validation_error",
    "possible_scale_issue",
    "no geometry",
    "required geometry",
    "недостаточно",
)

_ERROR_MARKERS = (
    "error",
    "failed",
    "unavailable",
    "timeout",
    "exception",
    "traceback",
)


def to_public_safe_analyzer_result(result: Mapping[str, Any] | None) -> dict[str, Any]:
    """Convert raw Analyzer/formula output into a public-safe preview payload.

    This adapter intentionally does not expose raw formula internals, diagnostics,
    coefficient math, pricing effects, order effects, reserve effects, payment
    effects, certificate claims, or appraisal claims.
    """
    if not isinstance(result, Mapping) or not result:
        return _payload(
            status="error",
            score_band="Unavailable",
            summary="Analysis result is unavailable. Please request a professional review.",
            warnings=["Analysis could not be prepared for public preview."],
        )

    status = _detect_status(result)
    if status == "unsupported":
        return _payload(
            status="unsupported",
            score_band="Unsupported",
            summary="This stone is not supported by the current public preview model.",
            warnings=["Use professional review for this shape or data set."],
        )

    if status == "incomplete":
        return _payload(
            status="incomplete",
            score_band="Review",
            summary="The available data is incomplete for a reliable public preview.",
            warnings=["Additional geometry or validation data is required."],
        )

    if status == "error":
        return _payload(
            status="error",
            score_band="Unavailable",
            summary="Analysis is temporarily unavailable. Please request a professional review.",
            warnings=["Public preview cannot show a result for this item."],
        )

    score = _safe_float(result.get("final_score"))
    if score is None:
        return _payload(
            status="incomplete",
            score_band="Review",
            summary="The score is not available for public preview.",
            warnings=["Additional review is required before showing a public result."],
        )

    band = _score_band(score)
    warnings = _public_warnings(result)
    summary = _summary_for_band(band, warnings)
    return _payload(
        status="ok",
        score_band=band,
        summary=summary,
        warnings=warnings,
    )


def _payload(status: str, score_band: str, summary: str, warnings: list[str]) -> dict[str, Any]:
    return {
        "status": status,
        "score_band": score_band,
        "summary": summary,
        "warnings": list(warnings),
        "limitations": list(PUBLIC_LIMITATIONS),
        "next_action": NEXT_ACTION,
    }


def _detect_status(result: Mapping[str, Any]) -> str:
    status_text = _joined_text(
        result.get("status"),
        result.get("input_status"),
        result.get("final_verdict"),
        result.get("error"),
        result.get("reason"),
        result.get("message"),
    )

    if _contains_any(status_text, _UNSUPPORTED_MARKERS):
        return "unsupported"
    if _contains_any(status_text, _INCOMPLETE_MARKERS):
        return "incomplete"
    if _contains_any(status_text, _ERROR_MARKERS):
        return "error"
    if result.get("final_score") is None and any(field in result for field in ("traceback", "exception", "debug_trace")):
        return "error"
    return "ok"


def _public_warnings(result: Mapping[str, Any]) -> list[str]:
    warnings: list[str] = []
    if result.get("critical_risk") is True:
        warnings.append("Professional review is recommended before purchase decisions.")
    if result.get("visual_check") is True:
        warnings.append("Visual review is recommended before public presentation.")
    return warnings


def _score_band(score: float) -> str:
    if score >= 95:
        return "Elite"
    if score >= 90:
        return "Premium"
    if score >= 80:
        return "High"
    if score >= 70:
        return "Standard"
    return "Review"


def _summary_for_band(score_band: str, warnings: list[str]) -> str:
    if warnings:
        return f"{score_band} public preview with review warnings."
    if score_band == "Elite":
        return "Elite public preview based on available analyzer data."
    if score_band == "Premium":
        return "Premium public preview based on available analyzer data."
    if score_band == "High":
        return "High public preview based on available analyzer data."
    if score_band == "Standard":
        return "Standard public preview based on available analyzer data."
    return "Public preview requires additional professional review."


def _safe_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _joined_text(*values: Any) -> str:
    return " ".join(str(value).lower() for value in values if value is not None)


def _contains_any(text: str, markers: tuple[str, ...]) -> bool:
    return any(marker in text for marker in markers)
