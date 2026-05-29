#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/kurgin/kurgin-score-analyzer}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"

cd "$APP_DIR"

if [ ! -f ".env.staging" ]; then
  echo "Missing .env.staging"
  exit 1
fi

set -a
. ./.env.staging
set +a

mkdir -p output/staging_smoke

python3 scripts/staging_smoke_test.py   --base-url "$BASE_URL"   --api-key "$KURGIN_API_SECRET"   --output-dir output/staging_smoke

echo "[KURGIN] Smoke outputs:"
ls -la output/staging_smoke
