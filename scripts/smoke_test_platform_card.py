from api.services.platform_card_service import analyze_platform_card

stone = {
    "Shape": "ROUND",
    "Report #": "PLATFORM-CARD",
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

payload = analyze_platform_card(stone, include_raw=True)
assert payload["status"] == "OK"
assert payload["card"]["kind"] == "kurgin_score_result_card"
assert payload["card"]["score"]["value"] is not None
print(payload["card"])
print("Platform card smoke OK")
