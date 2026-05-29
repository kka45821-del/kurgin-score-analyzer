from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests


def sample_stone():
    return {
        "Shape": "ROUND",
        "Report #": "STAGING-SMOKE",
        "Lab": "IGI",
        "Weight": 1.0,
        "Color": "F",
        "Clarity": "VS1",
        "Measurements": "6.430x6.470x3.970",
        "CrownAngle": 34.5,
        "PavilionAngle": 40.8,
        "TablePercent": 56,
        "DepthPercent": 61.5,
        "CrownPercent": 15,
        "PavilionPercent": 43,
        "GirdlePercent": 3.5,
    }


def headers(api_key: str):
    return {"X-KURGIN-API-Key": api_key} if api_key else {}


def assert_ok(response, label):
    if response.status_code >= 400:
        raise AssertionError(f"{label} failed: {response.status_code} {response.text[:500]}")


def main():
    parser = argparse.ArgumentParser(description="Run KURGIN Formula API staging smoke test.")
    parser.add_argument("--base-url", required=True, help="Example: http://127.0.0.1:8000")
    parser.add_argument("--api-key", default="", help="X-KURGIN-API-Key value")
    parser.add_argument("--output-dir", default="", help="Optional output folder for sample response/PDF")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    h = headers(args.api_key)

    health = requests.get(f"{base}/v1/health", timeout=20)
    assert_ok(health, "health")
    assert health.json()["status"] == "ok"

    ready = requests.get(f"{base}/v1/ready", timeout=30)
    assert_ok(ready, "ready")
    assert ready.json()["status"] == "ready"

    analyze = requests.post(
        f"{base}/v1/analyze/stone",
        json={"language": "RU", "stone": sample_stone()},
        headers=h,
        timeout=60,
    )
    assert_ok(analyze, "analyze stone")
    analyze_json = analyze.json()
    assert analyze_json["status"] == "OK"
    result = analyze_json["result"]

    card = requests.post(
        f"{base}/v1/platform/stone-card",
        json={"language": "RU", "stone": sample_stone()},
        headers=h,
        timeout=60,
    )
    assert_ok(card, "platform card")
    assert card.json()["card"]["kind"] == "kurgin_score_result_card"

    batch = requests.post(
        f"{base}/v1/analyze/batch/json",
        json={"language": "RU", "rows": [sample_stone()], "include_records": True},
        headers=h,
        timeout=60,
    )
    assert_ok(batch, "batch json")
    assert batch.json()["rows_ok"] == 1

    pdf = requests.post(
        f"{base}/v1/export/stone/pdf",
        json={"language": "BILINGUAL", "stone_result": result},
        headers=h,
        timeout=90,
    )
    assert_ok(pdf, "pdf export")
    assert pdf.headers.get("content-type", "").startswith("application/pdf")
    assert len(pdf.content) > 1000

    if args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "staging_analyze_response.json").write_text(json.dumps(analyze_json, ensure_ascii=False, indent=2), encoding="utf-8")
        (out / "staging_platform_card.json").write_text(json.dumps(card.json(), ensure_ascii=False, indent=2), encoding="utf-8")
        (out / "staging_sample_report.pdf").write_bytes(pdf.content)

    print(json.dumps({
        "status": "OK",
        "health": health.json()["status"],
        "ready": ready.json()["status"],
        "score": result.get("Kurgin Score"),
        "class": result.get("score_band_label_ru"),
        "pdf_bytes": len(pdf.content),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
