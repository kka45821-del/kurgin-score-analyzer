# KURGIN Formula API Contract v1.11.9

## Health

```text
GET /v1/health
```

## Analyze stone

```text
POST /v1/analyze/stone
```

Body:

```json
{
  "language": "RU",
  "stone": {
    "Shape": "ROUND",
    "Report #": "LG...",
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

## Analyze batch JSON

```text
POST /v1/analyze/batch/json
```

## Analyze batch Excel

```text
POST /v1/analyze/batch/excel
```

Multipart:
- file: `.xlsx`
- language: `RU`

## Export PDF

```text
POST /v1/export/stone/pdf
```

## Export Excel

```text
POST /v1/export/batch/excel
```

## Export ZIP package

```text
POST /v1/export/batch/package
```

Query:
- `pdf_mode=all_ok|top_only|none`

## Security

If `KURGIN_API_SECRET` is set, pass:

```text
X-KURGIN-API-Key: <secret>
```


## Platform stone card

```text
POST /v1/platform/stone-card
```

Purpose: compact payload for KURGIN Platform Tools card rendering.

Query:
- `include_raw=true|false`
- `include_experimental=true|false`

Response contains:
- `status`
- `card`
- optional `result`
- `version`
