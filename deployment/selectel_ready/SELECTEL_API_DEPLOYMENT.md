# KURGIN Formula API — Selectel Deployment Draft

## Goal

Run KURGIN Formula API as a private backend service.  
KURGIN Platform calls it server-to-server. Formula code is not shipped to frontend.

## Minimal deploy

```bash
docker build -t kurgin-formula-api .
docker run -d \
  --name kurgin-formula-api \
  -p 8000:8000 \
  -e KURGIN_API_ENV=production \
  -e KURGIN_API_SECRET=replace_with_secret \
  -e KURGIN_ALLOWED_ORIGINS=https://kurgin.example \
  kurgin-formula-api
```

## Health check

```bash
curl https://formula-api.example/v1/health
```

## Auth

Pass:

```text
X-KURGIN-API-Key: <secret>
```

Production must set `KURGIN_API_SECRET`.

## API boundary

Frontend must not call Formula API directly unless behind a trusted server proxy.

Recommended:

```text
KURGIN Platform backend
  → Formula API on Selectel/private network
    → kurgin_core / core_formula
```

## Do not expose

- `core_formula/`
- formula coefficients
- private supplier files
- raw internal diagnostics unless endpoint is protected
