# Selectel Staging Runbook

## 1. Prepare server

Install Docker and Docker Compose plugin.

Recommended server baseline:

```text
Ubuntu 22.04/24.04
2 CPU
4 GB RAM minimum
20+ GB disk
private firewall
```

## 2. Copy repository to server

Example:

```bash
git clone https://github.com/kka45821-del/kurgin-score-analyzer.git
cd kurgin-score-analyzer
```

Or upload release package.

## 3. Create `.env.staging`

```bash
cp .env.staging.example .env.staging
```

Edit:

```text
KURGIN_API_ENV=staging
KURGIN_API_SECRET=<strong secret>
KURGIN_ALLOWED_ORIGINS=https://staging.kurgin.example
KURGIN_MAX_BATCH_ROWS=2000
```

Generate secret:

```bash
python scripts/generate_api_secret.py
```

## 4. Build and start

```bash
docker compose -f docker-compose.staging.yml --env-file .env.staging build
docker compose -f docker-compose.staging.yml --env-file .env.staging up -d
```

## 5. Check health

```bash
curl http://127.0.0.1:8000/v1/health
curl http://127.0.0.1:8000/v1/ready
```

## 6. Run smoke test

```bash
python scripts/staging_smoke_test.py \
  --base-url http://127.0.0.1:8000 \
  --api-key <secret>
```

## 7. Test from platform backend

Platform backend should call:

```text
POST /v1/platform/stone-card
```

with header:

```text
X-KURGIN-API-Key: <secret>
```

## 8. Logs

```bash
docker logs -f kurgin-formula-api-staging
```

## 9. Restart

```bash
docker compose -f docker-compose.staging.yml --env-file .env.staging restart
```

## 10. Stop

```bash
docker compose -f docker-compose.staging.yml --env-file .env.staging down
```
