#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/kurgin/kurgin-score-analyzer}"
ENV_FILE="$APP_DIR/.env.staging"

if [ ! -d "$APP_DIR" ]; then
  echo "APP_DIR does not exist: $APP_DIR"
  exit 1
fi

cd "$APP_DIR"

if [ -f "$ENV_FILE" ]; then
  echo "[KURGIN] $ENV_FILE already exists. Not overwriting."
  exit 0
fi

SECRET="$(python3 scripts/generate_api_secret.py)"

cat > "$ENV_FILE" <<EOF
KURGIN_API_ENV=staging
KURGIN_API_SECRET=$SECRET
KURGIN_ALLOWED_ORIGINS=https://staging.kurgin.example
KURGIN_DEFAULT_LANGUAGE=RU
KURGIN_PDF_LANGUAGE=BILINGUAL
KURGIN_MAX_BATCH_ROWS=2000
KURGIN_LOG_LEVEL=INFO
KURGIN_REQUIRE_SECRET_IN_PROD=true
EOF

chmod 600 "$ENV_FILE"

echo "[KURGIN] Created $ENV_FILE"
echo "[KURGIN] Save this secret securely:"
echo "$SECRET"
