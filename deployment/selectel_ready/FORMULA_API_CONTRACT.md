# KURGIN Formula API Contract

Purpose: move hidden formula execution to a closed backend, while KURGIN Platform calls a stable API.

## Principle

Frontend / KURGIN Platform should not contain final commercial formula logic.

Recommended boundary:

```text
KURGIN Platform
  ↓ HTTPS
Formula API on Selectel/private backend
  ↓
core_formula + formula_modules
```

## Endpoints

### POST /v1/analyze/stone

Input:

```json
{
  "language": "RU",
  "stone": {
    "Shape": "ROUND",
    "Report #": "LG123456789",
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
}
```

Output:

```json
{
  "status": "OK",
  "result": {
    "Kurgin Score": 98.7,
    "Verdict Local": "Элитный",
    "tags_all": "Perfect Build",
    "interpretation_short_ru": "...",
    "recommendation_ru": "...",
    "Calculation Status": "OK"
  },
  "version": {
    "engine_version": "...",
    "core_sdk_version": "KURGIN Core SDK v1.11.0"
  }
}
```

### POST /v1/analyze/batch

Input:
- multipart Excel file, or JSON rows.

Output:
- compact Excel bytes or JSON rows.

### GET /v1/health

Returns:
- engine version
- formula mode
- API version
- build time

## Security Notes

- Do not expose `core_formula/` to public frontend bundles.
- Do not put formula coefficients in browser code.
- Store Formula API credentials in backend/server environment only.
- Platform should receive only analysis result, tags, statuses and report data.
