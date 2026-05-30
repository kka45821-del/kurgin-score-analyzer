# KURGIN Formula Service Scaffold

Private Selectel staging service scaffold for KURGIN formula execution.

This folder is a template for the future private repository/service package:

```text
kka45821-del/kurgin-formula-service
```

No production deployment is performed by this scaffold.

## Purpose

The service exposes a minimal private formula API:

```text
GET  /v1/health
GET  /v1/ready
POST /v1/formula/stone
```

`POST /v1/formula/stone` accepts normalized engine kwargs and returns the formula result shape expected by the Analyzer cloud client.

## Expected private repository structure

```text
app/
  main.py
core_formula/
config_settings/
  engine_config.py
requirements.txt
README.md
.env.example
```

In this public Analyzer repo, `core_formula/` and `engine_config.py` are not duplicated inside this scaffold folder. In the future private repo, copy the private formula files there.

## Endpoint contract

### GET /v1/health

Returns service status and version metadata.

### GET /v1/ready

Runs a minimal internal formula readiness check and returns `ready` or `not_ready`.

### POST /v1/formula/stone

Requires:

```text
Authorization: Bearer <KURGIN_FORMULA_API_KEY>
```

Input:

```json
{
  "stone": {
    "crown_a": 34.5,
    "pav_a": 40.8,
    "table": 56,
    "depth": 61.5,
    "crown_p": 15,
    "pav_p": 43,
    "girdle_p": 3.5
  }
}
```

Output:

```text
engine_version
final_score
final_verdict
triple_score
structure_modifier
structure_tags
visual_check
critical_risk
diagnostics
breakdown
```

`breakdown` and raw `diagnostics` are staging/internal only by default.

## Environment variables

```text
KURGIN_FORMULA_ENV=staging
KURGIN_FORMULA_API_KEY=<staging key>
KURGIN_FORMULA_SERVICE_VERSION=0.1.0-staging
KURGIN_FORMULA_BUILD_ID=<git sha or build id>
```

Analyzer staging later uses:

```text
FORMULA_MODE=cloud_fallback
FORMULA_API_URL=<staging endpoint>/v1/formula/stone
FORMULA_API_KEY=<same staging key>
```

## Local run after private formula files are copied

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Health:

```bash
curl http://localhost:8000/v1/health
```

Formula call:

```bash
curl -X POST http://localhost:8000/v1/formula/stone \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $KURGIN_FORMULA_API_KEY" \
  -d '{
    "stone": {
      "crown_a": 34.5,
      "pav_a": 40.8,
      "table": 56,
      "depth": 61.5,
      "crown_p": 15,
      "pav_p": 43,
      "girdle_p": 3.5
    }
  }'
```

## Safety rules

- Do not commit real `.env` files.
- Do not commit real API keys.
- Do not print API keys in logs.
- Do not return stack traces to public clients.
- Do not expose formula source code in public/client bundles.
- Keep this service private before production extraction.

## Current limitation

This is a scaffold. It requires private formula files to be copied into the private service repo before `/v1/ready` and `/v1/formula/stone` can return real formula results.

The current public Analyzer repo remains stable and unchanged in behavior.
