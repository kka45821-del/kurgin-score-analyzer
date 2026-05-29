# API Contract Validation Plan

## Goals

- Validate endpoint availability.
- Validate auth behavior.
- Validate response field stability.
- Validate PDF/Excel export paths.
- Validate error response standard.

## Endpoints

```text
GET  /v1/health
GET  /v1/ready
POST /v1/analyze/stone
POST /v1/analyze/batch/json
POST /v1/analyze/batch/excel
POST /v1/export/stone/pdf
POST /v1/export/batch/excel
POST /v1/export/batch/package
```

## Contract tests

Use:

```bash
python scripts/contract_test_api.py
```

## Pass conditions

- `/v1/health` returns status ok.
- `/v1/ready` returns status ready.
- one-stone analysis returns `Calculation Status = OK`.
- response contains stable fields.
- PDF endpoint returns `application/pdf`.
- unauthorized request fails when secret is configured.
