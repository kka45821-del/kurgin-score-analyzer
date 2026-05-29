# KURGIN Platform Integration Example

## Backend-to-backend call

KURGIN Platform should call Formula API from backend, not directly from browser.

Example flow:

```text
User opens Tools / KURGIN Score Analyzer
  ↓
KURGIN Platform backend receives stone parameters
  ↓
Backend calls Formula API with X-KURGIN-API-Key
  ↓
Formula API returns score/tags/report fields
  ↓
Platform renders card and optional PDF button
```

## Python example

```python
import requests

payload = {
    "language": "RU",
    "stone": {
        "Shape": "ROUND",
        "Report #": "LG123",
        "Lab": "IGI",
        "Weight": 1.0,
        "Measurements": "6.430x6.470x3.970",
        "CrownAngle": 34.5,
        "PavilionAngle": 40.8,
        "TablePercent": 56,
        "DepthPercent": 61.5,
        "CrownPercent": 15,
        "PavilionPercent": 43,
        "GirdlePercent": 3.5
    }
}

response = requests.post(
    "https://formula-api.example/v1/analyze/stone",
    json=payload,
    headers={"X-KURGIN-API-Key": "<secret>"},
    timeout=30,
)
data = response.json()
```

## Store in platform

Recommended platform fields:

```text
stone_id
report_number
kurgin_score
kurgin_class
tags_all
interpretation_short_ru
recommendation_ru
calculation_status
engine_version
formula_output_version
pdf_status
```
