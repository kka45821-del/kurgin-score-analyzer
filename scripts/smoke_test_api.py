from api.main import app
from api.services.core_service import analyze_one, version_payload

stone = {
    "Shape": "ROUND",
    "Report #": "API-SMOKE",
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

result = analyze_one(stone)
assert result["Calculation Status"] == "OK"
assert result["Kurgin Score"] is not None
print(version_payload())
print("API smoke OK")
