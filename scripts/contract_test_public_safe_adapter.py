from __future__ import annotations

from platform_integration.public_safe_analyzer_adapter import (
    ALLOWED_PUBLIC_FIELDS,
    BLOCKED_INTERNAL_FIELDS,
    PUBLIC_LIMITATIONS,
    to_public_safe_analyzer_result,
)


BASE_RAW_RESULT = {
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
    "raw_engine_output": {"secret": "private engine payload"},
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
        "weights",
        "penalty_breakdown",
        "internal_diagnostics",
        "debug_trace",
        "raw_engine_output",
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


def test_ok_result_returns_public_fields_only():
    payload = to_public_safe_analyzer_result(BASE_RAW_RESULT)
    _assert_public_shape(payload)
    assert payload["status"] == "ok"
    assert payload["score_band"] == "Elite"
    assert payload["summary"]


def test_review_warning_is_public_safe():
    raw = dict(BASE_RAW_RESULT, final_score=88.0, visual_check=True, critical_risk=True)
    payload = to_public_safe_analyzer_result(raw)
    _assert_public_shape(payload)
    assert payload["status"] == "ok"
    assert payload["score_band"] == "High"
    assert payload["warnings"]


def test_unsupported_state_is_safe():
    payload = to_public_safe_analyzer_result({
        "status": "UNSUPPORTED_SHAPE",
        "reason": "Shape OVAL is not supported by current ROUND model",
        "diagnostics": {"secret": True},
        "raw_engine_output": {"secret": "private payload"},
    })
    _assert_public_shape(payload)
    assert payload["status"] == "unsupported"
    assert payload["score_band"] == "Unsupported"


def test_incomplete_state_is_safe():
    payload = to_public_safe_analyzer_result({
        "status": "MISSING_GEOMETRY",
        "message": "Missing required geometry fields: CrownAngle",
        "breakdown": "internal detail",
        "penalty_breakdown": {"secret": True},
    })
    _assert_public_shape(payload)
    assert payload["status"] == "incomplete"
    assert payload["score_band"] == "Review"


def test_error_state_does_not_leak_traceback_or_exception_text():
    payload = to_public_safe_analyzer_result({
        "status": "error",
        "exception": "ValueError: secret formula failed",
        "traceback": "Traceback secret internal stack",
        "raw_engine_output": {"secret": "private payload"},
    })
    _assert_public_shape(payload)
    assert payload["status"] == "error"
    assert payload["score_band"] == "Unavailable"


def test_empty_or_malformed_input_is_safe():
    for raw in ({}, None, "not-a-dict"):
        payload = to_public_safe_analyzer_result(raw)  # type: ignore[arg-type]
        _assert_public_shape(payload)
        assert payload["status"] == "error"
        assert payload["score_band"] == "Unavailable"


def main():
    tests = [
        test_ok_result_returns_public_fields_only,
        test_review_warning_is_public_safe,
        test_unsupported_state_is_safe,
        test_incomplete_state_is_safe,
        test_error_state_does_not_leak_traceback_or_exception_text,
        test_empty_or_malformed_input_is_safe,
    ]
    for test in tests:
        test()
    print("Public-safe analyzer adapter contract test OK")
    print({
        "allowed_public_fields": sorted(ALLOWED_PUBLIC_FIELDS),
        "blocked_internal_fields": sorted(BLOCKED_INTERNAL_FIELDS),
    })


if __name__ == "__main__":
    main()
