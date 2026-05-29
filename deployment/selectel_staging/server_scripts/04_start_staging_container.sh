#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/kurgin/kurgin-score-analyzer}"

cd "$APP_DIR"

if [ ! -f ".env.staging" ]; then
  echo "Missing .env.staging. Run 03_create_env_staging.sh first."
  exit 1
fi

python3 scripts/validate_staging_env.py

docker compose -f docker-compose.staging.yml --env-file .env.staging build
docker compose -f docker-compose.staging.yml --env-file .env.staging up -d

echo "[KURGIN] Waiting for container readiness..."
sleep 10

curl -fsS http://127.0.0.1:8000/v1/health
echo
curl -fsS http://127.0.0.1:8000/v1/ready
echo

echo "[KURGIN] Container status:"
docker compose -f docker-compose.staging.yml --env-file .env.staging ps
