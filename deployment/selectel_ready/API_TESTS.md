# KURGIN Formula API Tests

## Local run

```bash
pip install -r requirements-api.txt
uvicorn api.main:app --reload
```

## Health

```bash
curl http://localhost:8000/v1/health
```

## Analyze one stone

```bash
curl -X POST http://localhost:8000/v1/analyze/stone \
  -H "Content-Type: application/json" \
  -d '{
    "language": "RU",
    "stone": {
      "Shape": "ROUND",
      "Report #": "API-DEMO",
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
      "GirdlePercent": 3.5
    }
  }'
```

## Export PDF

First analyze stone, then send result to `/v1/export/stone/pdf`.
