from __future__ import annotations

import json
import os
from contextlib import contextmanager
from urllib.error import HTTPError

from formula_client import cloud_client, engine_client
from formula_client.cloud_client import CloudFormulaError


SAMPLE_ENGINE_KWARGS = {
    "crown_a": 34.5,
    "pav_a": 40.8,
    "table": 56,
    "depth": 61.5,
    "crown_p": 15,
    "pav_p": 43,
    "girdle_p": 3.5,
}

SAMPLE_CLOUD_RESPONSE = {
    "engine_version": "Kurgin Round Engine test-cloud",
    "final_score": 98.7,
    "final_verdict": "TOP: Excellent Selection",
    "triple_score": 98.0,
    "structure_modifier": 1.0071,
    "structure_tags": ["Perfect Build"],
    "visual_check": False,
    "critical_risk": False,
    "diagnostics": {
        "nailhead": 0.0,
        "fisheye": 0.0,
        "fire_loss": 0.0,
        "depth_dev": 0.0,
        "crown_dev": 0.0,
        "pavilion_dev": 0.0,
        "balance_err": 0.0,
        "girdle_penalty": 0.0,
        "ideal_depth": 61.5,
        "ideal_crown": 15.0,
        "ideal_pavilion": 43.0,
        "total_loss": 0.0,
    },
    "breakdown": "Cloud formula contract test response",
}

REQUIRED_CLOUD_RESPONSE_FIELDS = [
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


@contextmanager
def patched_env(**updates):
    old_values = {key: os.environ.get(key) for key in updates}
    try:
        for key, value in updates.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        yield
    finally:
        for key, old_value in old_values.items():
            if old_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old_value


@contextmanager
def patched_attr(obj, name, value):
    old_value = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old_value)


class FakeResponse:
    def __init__(self, body: bytes):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self.body


class FakeErrorBody:
    def read(self):
        return b'{"detail":"boom"}'


def assert_cloud_response_shape(response):
    missing = [field for field in REQUIRED_CLOUD_RESPONSE_FIELDS if field not in response]
    assert not missing, f"Missing cloud response fields: {missing}"
    assert isinstance(response["diagnostics"], dict), "diagnostics must be an object"
    assert isinstance(response["structure_tags"], list), "structure_tags must be a list"


def test_cloud_client_successful_response():
    def fake_urlopen(req, timeout):
        assert req.full_url == "https://formula.example.test/v1/analyze/stone"
        assert timeout == 20
        payload = json.loads(req.data.decode("utf-8"))
        assert payload == {"stone": SAMPLE_ENGINE_KWARGS}
        assert req.get_header("Authorization") == "Bearer test-key"
        return FakeResponse(json.dumps(SAMPLE_CLOUD_RESPONSE).encode("utf-8"))

    with patched_env(FORMULA_API_URL="https://formula.example.test/v1/analyze/stone", FORMULA_API_KEY="test-key"):
        with patched_attr(cloud_client.request, "urlopen", fake_urlopen):
            response = cloud_client.calculate_stone_cloud(SAMPLE_ENGINE_KWARGS)

    assert response == SAMPLE_CLOUD_RESPONSE
    assert_cloud_response_shape(response)


def test_cloud_client_missing_endpoint_fails():
    with patched_env(FORMULA_API_URL=None, FORMULA_API_KEY=None):
        try:
            cloud_client.calculate_stone_cloud(SAMPLE_ENGINE_KWARGS)
        except CloudFormulaError as exc:
            assert "FORMULA_API_URL is not configured" in str(exc)
        else:
            raise AssertionError("Expected CloudFormulaError for missing FORMULA_API_URL")


def test_cloud_client_http_error_fails():
    def fake_urlopen(req, timeout):
        raise HTTPError(req.full_url, 502, "Bad Gateway", hdrs=None, fp=FakeErrorBody())

    with patched_env(FORMULA_API_URL="https://formula.example.test/v1/analyze/stone"):
        with patched_attr(cloud_client.request, "urlopen", fake_urlopen):
            try:
                cloud_client.calculate_stone_cloud(SAMPLE_ENGINE_KWARGS)
            except CloudFormulaError as exc:
                assert "Cloud formula HTTP 502" in str(exc)
                assert "boom" in str(exc)
            else:
                raise AssertionError("Expected CloudFormulaError for HTTP error")


def test_cloud_client_malformed_json_fails():
    def fake_urlopen(req, timeout):
        return FakeResponse(b"{not-json")

    with patched_env(FORMULA_API_URL="https://formula.example.test/v1/analyze/stone"):
        with patched_attr(cloud_client.request, "urlopen", fake_urlopen):
            try:
                cloud_client.calculate_stone_cloud(SAMPLE_ENGINE_KWARGS)
            except CloudFormulaError as exc:
                assert "Cloud formula request failed" in str(exc)
            else:
                raise AssertionError("Expected CloudFormulaError for malformed JSON")


def test_engine_client_formula_mode_cloud_calls_cloud():
    calls = {"cloud": 0, "local": 0}

    def fake_cloud(engine_kwargs):
        calls["cloud"] += 1
        assert engine_kwargs == SAMPLE_ENGINE_KWARGS
        return SAMPLE_CLOUD_RESPONSE

    def fake_local(engine_kwargs):
        calls["local"] += 1
        raise AssertionError("local formula should not be called in cloud mode")

    with patched_env(FORMULA_MODE="cloud"):
        with patched_attr(engine_client, "calculate_stone_cloud", fake_cloud):
            with patched_attr(engine_client, "calculate_stone_local", fake_local):
                response = engine_client.calculate_stone(SAMPLE_ENGINE_KWARGS)

    assert response == SAMPLE_CLOUD_RESPONSE
    assert calls == {"cloud": 1, "local": 0}
    assert_cloud_response_shape(response)


def test_engine_client_cloud_fallback_uses_local_after_cloud_failure():
    calls = {"cloud": 0, "local": 0}
    local_response = dict(SAMPLE_CLOUD_RESPONSE, engine_version="local-fallback-test")

    def fake_cloud(engine_kwargs):
        calls["cloud"] += 1
        raise CloudFormulaError("cloud unavailable")

    def fake_local(engine_kwargs):
        calls["local"] += 1
        assert engine_kwargs == SAMPLE_ENGINE_KWARGS
        return local_response

    with patched_env(FORMULA_MODE="cloud_fallback"):
        with patched_attr(engine_client, "calculate_stone_cloud", fake_cloud):
            with patched_attr(engine_client, "calculate_stone_local", fake_local):
                response = engine_client.calculate_stone(SAMPLE_ENGINE_KWARGS)

    assert response == local_response
    assert calls == {"cloud": 1, "local": 1}
    assert_cloud_response_shape(response)


def test_engine_client_formula_mode_local_calls_local():
    calls = {"cloud": 0, "local": 0}
    local_response = dict(SAMPLE_CLOUD_RESPONSE, engine_version="local-test")

    def fake_cloud(engine_kwargs):
        calls["cloud"] += 1
        raise AssertionError("cloud formula should not be called in local mode")

    def fake_local(engine_kwargs):
        calls["local"] += 1
        assert engine_kwargs == SAMPLE_ENGINE_KWARGS
        return local_response

    with patched_env(FORMULA_MODE="local"):
        with patched_attr(engine_client, "calculate_stone_cloud", fake_cloud):
            with patched_attr(engine_client, "calculate_stone_local", fake_local):
                response = engine_client.calculate_stone(SAMPLE_ENGINE_KWARGS)

    assert response == local_response
    assert calls == {"cloud": 0, "local": 1}
    assert_cloud_response_shape(response)


def main():
    tests = [
        test_cloud_client_successful_response,
        test_cloud_client_missing_endpoint_fails,
        test_cloud_client_http_error_fails,
        test_cloud_client_malformed_json_fails,
        test_engine_client_formula_mode_cloud_calls_cloud,
        test_engine_client_cloud_fallback_uses_local_after_cloud_failure,
        test_engine_client_formula_mode_local_calls_local,
    ]
    for test in tests:
        test()
    print("Cloud formula client contract tests OK")
    print({
        "tested_modes": ["cloud", "cloud_fallback", "local"],
        "required_response_fields": REQUIRED_CLOUD_RESPONSE_FIELDS,
        "production_notes": {
            "cloud_mode": "production should prefer fail-closed cloud mode unless fallback is explicitly allowed",
            "fallback_logging": "fallback reason should be logged before production use",
            "schema_validation": "cloud responses should be schema-validated before public exposure",
            "public_fields": "public clients should receive filtered result/card payloads, not raw formula internals",
        },
    })


if __name__ == "__main__":
    main()
