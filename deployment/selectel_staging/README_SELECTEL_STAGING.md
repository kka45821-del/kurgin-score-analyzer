# KURGIN Formula API — Selectel Staging Deployment

Version: v1.12.3  
Status: staging plan / deployment-ready scaffold  
Official KURGIN Score changed: No

## Goal

Run KURGIN Formula API in a private staging environment before production.

Recommended architecture:

```text
KURGIN Platform backend
  → HTTPS
Selectel staging server
  → Docker container: kurgin-formula-api
  → KURGIN Core SDK / current formula
```

## What this staging should prove

- Docker image builds.
- API starts and survives restart.
- `/v1/health` returns `ok`.
- `/v1/ready` returns `ready`.
- API key protection works.
- `/v1/analyze/stone` works.
- `/v1/platform/stone-card` works.
- `/v1/export/stone/pdf` works.
- batch JSON works.
- logs are readable.
- formula code remains backend-only.

## Do not use staging as production

Staging is for testing API, deployment, security boundary and platform integration.  
Do not expose staging endpoint to public frontend without backend proxy.
