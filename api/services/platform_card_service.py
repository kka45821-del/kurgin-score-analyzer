from __future__ import annotations

from typing import Any, Dict

from kurgin_core import analyze_stone
from platform_integration.platform_adapter import build_platform_card_payload, filter_public_result


def analyze_platform_card(stone: Dict[str, Any], language: str = "RU", include_raw: bool = False, include_experimental: bool = True):
    result = analyze_stone(stone, language=language)
    card = build_platform_card_payload(result, include_experimental=include_experimental)
    response = {
        "status": result.get("Calculation Status", "OK"),
        "card": card,
    }
    if include_raw:
        response["result"] = filter_public_result(result, include_experimental=include_experimental)
    return response
