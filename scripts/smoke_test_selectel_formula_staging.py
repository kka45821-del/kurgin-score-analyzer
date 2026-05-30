from __future__ import annotations

import json
import os
import sys
from urllib import error, request


SKIP_MESSAGE = "Selectel staging smoke skipped: FORMULA_API_URL or FORMULA_API_KEY not configured"
TIMEOUT_SECONDS = 20

SAMPLE_PAYLOAD = {
    "stone": {
        "crown_a": 34.5,
        "pav_a": 40.8,
        "table": 56,
        "depth": 61.5,
        "crown_p": 15,
        "pav_p": 43,
        "girdle_p": 3.5,
    }
}

REQUIRED_RESPONSE_FIELDS = [
    "engine_version",
    "final_score",
    "final_verdict",
    "triple_score",
    "structure_modifier",
    "structure_tags",
    "visual_check",
    "critical_risk",
    "diagnostics",
    "breakdown",
]


def _safe_summary(response: dict) -> dict:
    """Return only non-secret, non-full-response smoke summary."""
    return {
        "status": "ok",
        "engine_version": response.get("engine_version"),
        "final_score": response.get("final_score"),
        "final_verdict": response.get("final_verdict"),
        "structure_tags_count": len(response.get("structure_tags") or []),
        "visual_check": response.get("visual_check"),
        "critical_risk": response.get("critical_risk"),
        "diagnostics_keys": sorted(list((response.get("diagnostics") or {}).keys())),
    }


def _validate_response_shape(response: dict) -> None:
    missing = [field for field in REQUIRED_RESPONSE_FIELDS if field not in response]
    if missing:
        raise AssertionError(f"Selectel staging response missing required fields: {missing}")

    if not isinstance(response["diagnostics"], dict):
        raise AssertionError("Selectel staging response field diagnostics must be an object")
    if not isinstance(response["structure_tags"], list):
        raise AssertionError("Selectel staging response field structure_tags must be a list")

    numeric_fields = ["final_score", "triple_score", "structure_modifier"]
    for field in numeric_fields:
        if not isinstance(response[field], (int, float)):
            raise AssertionError(f"Selectel staging response field {field} must be numeric")

    bool_fields = ["visual_check", "critical_risk"]
    for field in bool_fields:
        if not isinstance(response[field], bool):
            raise AssertionError(f"Selectel staging response field {field} must be boolean")


def _post_formula(endpoint: str, api_key: str) -> dict:
    data = json.dumps(SAMPLE_PAYLOAD, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        endpoint,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            status_code = getattr(resp, "status", None) or resp.getcode()
            body = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")[:500]
        raise RuntimeError(f"Selectel staging smoke failed: HTTP {exc.code}: {detail}") from exc
    except Exception as exc:
        raise RuntimeError(f"Selectel staging smoke failed: request error: {exc}") from exc

    if status_code != 200:
        raise RuntimeError(f"Selectel staging smoke failed: expected HTTP 200, got {status_code}")

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Selectel staging smoke failed: response is not valid JSON") from exc

    if not isinstance(parsed, dict):
        raise RuntimeError("Selectel staging smoke failed: response JSON must be an object")

    return parsed


def main() -> int:
    endpoint = os.getenv("FORMULA_API_URL", "").strip()
    api_key = os.getenv("FORMULA_API_KEY", "").strip()

    if not endpoint or not api_key:
        print(SKIP_MESSAGE)
        return 0

    response = _post_formula(endpoint, api_key)
    _validate_response_shape(response)
    print("Selectel staging smoke OK")
    print(json.dumps(_safe_summary(response), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
