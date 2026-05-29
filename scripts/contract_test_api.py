from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app


REQUIRED_RESULT_FIELDS = [
    "Calculation Status",
    "Kurgin Score",
    "Verdict",
    "Verdict Local",
    "score_band_label_ru",
    "tags_all",
    "tag1",
    "tag2",
    "tag3",
    "tag4",
    "tag5",
    "tag6",
    "interpretation_short_ru",
    "recommendation_ru",
    "warning_ru",
]


def sample_payload():
    return {
        "language": "RU",
        "stone": {
            "Shape": "ROUND",
            "Report #": "CONTRACT-TEST",
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
        },
    }


def main():
    client = TestClient(app)

    health = client.get("/v1/health")
    assert health.status_code == 200, health.text
    assert health.json()["status"] == "ok"

    ready = client.get("/v1/ready")
    assert ready.status_code == 200, ready.text
    assert ready.json()["status"] == "ready"

    response = client.post("/v1/analyze/stone", json=sample_payload())
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "OK"
    result = data["result"]

    missing = [field for field in REQUIRED_RESULT_FIELDS if field not in result]
    assert not missing, f"Missing fields: {missing}"

    batch = client.post("/v1/analyze/batch/json", json={
        "language": "RU",
        "rows": [sample_payload()["stone"]],
        "include_records": True,
    })
    assert batch.status_code == 200, batch.text
    assert batch.json()["rows_ok"] == 1


    card = client.post("/v1/platform/stone-card?include_raw=true", json=sample_payload())
    assert card.status_code == 200, card.text
    card_data = card.json()
    assert card_data["status"] == "OK"
    assert card_data["card"]["kind"] == "kurgin_score_result_card"
    assert card_data["card"]["score"]["value"] is not None

    pdf = client.post("/v1/export/stone/pdf", json={
        "language": "BILINGUAL",
        "stone_result": result,
    })
    assert pdf.status_code == 200, pdf.text
    assert pdf.headers["content-type"].startswith("application/pdf")
    assert len(pdf.content) > 1000

    print("API contract test OK")
    print({
        "health": health.json()["status"],
        "ready": ready.json()["status"],
        "score": result.get("Kurgin Score"),
        "class": result.get("score_band_label_ru"),
        "pdf_bytes": len(pdf.content),
        "platform_card_kind": card_data["card"]["kind"],
    })


if __name__ == "__main__":
    main()
