"""Minimal KURGIN Platform backend client example."""

from __future__ import annotations

import requests


def analyze_stone(api_url: str, api_key: str, stone: dict, language: str = "RU", timeout: int = 30):
    response = requests.post(
        f"{api_url.rstrip('/')}/v1/analyze/stone",
        json={"language": language, "stone": stone},
        headers={"X-KURGIN-API-Key": api_key} if api_key else {},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    demo = {
        "Shape": "ROUND",
        "Report #": "PLATFORM-DEMO",
        "Lab": "IGI",
        "Weight": 1.0,
        "Measurements": "6.430x6.470x3.970",
        "CrownAngle": 34.5,
        "PavilionAngle": 40.8,
        "TablePercent": 56,
        "DepthPercent": 61.5,
        "CrownPercent": 15,
        "PavilionPercent": 43,
        "GirdlePercent": 3.5,
    }
    print(analyze_stone("http://localhost:8000", "", demo))
