#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/kurgin/kurgin-score-analyzer}"
BRANCH="${BRANCH:-main}"

cd "$APP_DIR"

git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

docker compose -f docker-compose.staging.yml --env-file .env.staging build
docker compose -f docker-compose.staging.yml --env-file .env.staging up -d

sleep 10

set -a
. ./.env.staging
set +a

python3 scripts/staging_smoke_test.py --base-url http://127.0.0.1:8000 --api-key "$KURGIN_API_SECRET"

echo "[KURGIN] Update complete"
