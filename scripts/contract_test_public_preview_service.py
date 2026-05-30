from __future__ import annotations

import platform_integration.public_analyzer_preview_service as preview_service
from platform_integration.public_safe_analyzer_adapter import (
    ALLOWED_PUBLIC_FIELDS,
    BLOCKED_INTERNAL_FIELDS,
    PUBLIC_LIMITATIONS,
)


OK_PUBLIC_INPUT = {
    "shape": "Round",
    "carat": 1.0,
    "color": "F",
    "clarity": "VS1",
    "table_pct": 56,
    "depth_pct": 61.5,
    "crown_angle": 34.5,
    "pavilion_angle": 40.8,
    "crown_height": 15,
    "pavilion_depth": 43,
    "girdle": 3.5,
    "fluorescence": "None",
    "report_number": "PUBLIC001",
}

RAW_ANALYZER_RESULT = {
    "engine_version": "Kurgin Round Engine contract-test",
    "final_score": 96.4,
    "final_verdict": "TOP: Excellent Selection",
    "triple_score": 98.0,
    "structure_modifier": 1.0071,
    "structure_tags": ["Perfect Build"],
    "visual_check": False,
    "critical_risk": False,
    "diagnostics": {"nailhead": 0.0, "fisheye": 0.0},
    "breakdown": "internal formula explanation",
    "raw_formula": "secret coefficient expression",
    "weights": {"secret": 1.0},
    "penalty_breakdown": {"secret": 0.0},
    "internal_diagnostics": {"secret": True},
    "debug_trace": ["secret trace"],
    "formula_source": "private formula source",
    "coefficient_formula": "secret formula",
    "certificate_claim": "not allowed",
    "appraisal_claim": "not allowed",
    "price_effect": "not allowed",
    "order_effect": "not allowed",
    "reserve_effect": "not allowed",
    "payment_effect": "not allowed",
}


def _assert_public_shape(payload):
    assert set(payload.keys()) == ALLOWED_PUBLIC_FIELDS, payload
    assert payload["limitations"] == PUBLIC_LIMITATIONS
    assert payload["next_action"] == "request_professional_review"
    assert isinstance(payload["warnings"], list)
    for blocked in BLOCKED_INTERNAL_FIELDS:
        assert blocked not in payload, blocked
    rendered = repr(payload).lower()
    blocked_text = [
        "traceback",
        "exception",
        "secret",
        "diagnostics",
        "breakdown",
        "triple_score",
        "structure_modifier",
        "raw_formula",
        "coefficient_formula",
        "formula_source",
        "certificate_claim",
        "appraisal_claim",
        "price_effect",
        "order_effect",
        "reserve_effect",
        "payment_effect",
    ]
    for text in blocked_text:
        assert text not in rendered, text


def test_ok_public_input_returns_public_safe_output():
    calls = []

    def fake_analyze_stone(params, language="RU"):
        calls.append((params, language))
        assert params["Shape"] == "Round"
        assert params["Weight"] == 1.0
        assert params["TablePercent"] == 56
        assert params["DepthPercent"] == 61.5
        assert params["CrownAngle"] == 34.5
        assert params["PavilionAngle"] == 40.8
        assert params["CrownPercent"] == 15
        assert params["PavilionPercent"] == 43
        assert params["GirdlePercent"] == 3.5
        assert params["Fluorescence Intensity"] == "None"
        assert params["Report #"] == "PUBLIC001"
        assert language == "RU"
        return RAW_ANALYZER_RESULT

    original = preview_service.analyze_stone
    preview_service.analyze_stone = fake_analyze_stone
    try:
        payload = preview_service.analyze_public_preview(OK_PUBLIC_INPUT, language="RU")
    finally:
        preview_service.analyze_stone = original

    assert len(calls) == 1
    _assert_public_shape(payload)
    assert payload["status"] == "ok"
    assert payload["score_band"] == "Elite"


def test_unsupported_shape_returns_safe_output_without_sdk_call():
    def fail_analyze_stone(params, language="RU"):
        raise AssertionError("SDK must not be called for unsupported shapes")

    original = preview_service.analyze_stone
    preview_service.analyze_stone = fail_analyze_stone
    try:
        payload = preview_service.analyze_public_preview(dict(OK_PUBLIC_INPUT, shape="OVAL"))
    finally:
        preview_service.analyze_stone = original

    _assert_public_shape(payload)
    assert payload["status"] == "unsupported"
    assert payload["score_band"] == "Unsupported"


def test_missing_geometry_returns_incomplete_without_sdk_call():
    def fail_analyze_stone(params, language="RU"):
        raise AssertionError("SDK must not be called for incomplete geometry")

    incomplete = dict(OK_PUBLIC_INPUT)
    incomplete.pop("crown_angle")

    original = preview_service.analyze_stone
    preview_service.analyze_stone = fail_analyze_stone
    try:
        payload = preview_service.analyze_public_preview(incomplete)
    finally:
        preview_service.analyze_stone = original

    _assert_public_shape(payload)
    assert payload["status"] == "incomplete"
    assert payload["score_band"] == "Review"


def test_malformed_input_returns_safe_error():
    payload = preview_service.analyze_public_preview("not-a-dict")  # type: ignore[arg-type]
    _assert_public_shape(payload)
    assert payload["status"] == "error"
    assert payload["score_band"] == "Unavailable"


def test_sdk_error_does_not_leak_traceback_or_exception_text():
    def failing_analyze_stone(params, language="RU"):
        raise RuntimeError("secret formula source traceback should not leak")

    original = preview_service.analyze_stone
    preview_service.analyze_stone = failing_analyze_stone
    try:
        payload = preview_service.analyze_public_preview(OK_PUBLIC_INPUT)
    finally:
        preview_service.analyze_stone = original

    _assert_public_shape(payload)
    assert payload["status"] == "error"
    assert payload["score_band"] == "Unavailable"


def main():
    tests = [
        test_ok_public_input_returns_public_safe_output,
        test_unsupported_shape_returns_safe_output_without_sdk_call,
        test_missing_geometry_returns_incomplete_without_sdk_call,
        test_malformed_input_returns_safe_error,
        test_sdk_error_does_not_leak_traceback_or_exception_text,
    ]
    for test in tests:
        test()
    print("Public analyzer preview service contract test OK")
    print({
        "public_input_fields": sorted(preview_service.PUBLIC_INPUT_FIELD_MAP.keys()),
        "public_output_fields": sorted(ALLOWED_PUBLIC_FIELDS),
    })


if __name__ == "__main__":
    main()
