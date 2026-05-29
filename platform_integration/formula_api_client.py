"""Python client for KURGIN Formula API.

This is intended for KURGIN Platform backend usage.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests


class KurginFormulaApiClient:
    def __init__(self, base_url: str, api_key: str = "", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-KURGIN-API-Key"] = self.api_key
        return headers

    def health(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/v1/health", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def ready(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/v1/ready", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def analyze_stone(self, stone: Dict[str, Any], language: str = "RU") -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/v1/analyze/stone",
            json={"language": language, "stone": stone},
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def analyze_batch_json(self, rows: list[Dict[str, Any]], language: str = "RU", include_records: bool = True):
        response = requests.post(
            f"{self.base_url}/v1/analyze/batch/json",
            json={"language": language, "rows": rows, "include_records": include_records},
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def export_stone_pdf(self, stone_result: Dict[str, Any], language: str = "BILINGUAL") -> bytes:
        response = requests.post(
            f"{self.base_url}/v1/export/stone/pdf",
            json={"language": language, "stone_result": stone_result},
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.content
