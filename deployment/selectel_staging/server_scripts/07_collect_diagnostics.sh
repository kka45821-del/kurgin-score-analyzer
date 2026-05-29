#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/kurgin/kurgin-score-analyzer}"
OUT_DIR="${OUT_DIR:-/tmp/kurgin_formula_api_diagnostics_$(date +%Y%m%d_%H%M%S)}"

mkdir -p "$OUT_DIR"

{
  echo "== date =="
  date -u
  echo
  echo "== uname =="
  uname -a
  echo
  echo "== docker =="
  docker --version || true
  docker compose version || true
  echo
  echo "== containers =="
  docker ps -a || true
  echo
  echo "== app git =="
  if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR"
    git status --short
    git log -1 --oneline
  fi
} > "$OUT_DIR/system.txt" 2>&1

if docker ps --format '{{.Names}}' | grep -q '^kurgin-formula-api-staging$'; then
  docker logs --tail=300 kurgin-formula-api-staging > "$OUT_DIR/container_logs.txt" 2>&1 || true
fi

curl -sS http://127.0.0.1:8000/v1/health > "$OUT_DIR/health.json" 2>&1 || true
curl -sS http://127.0.0.1:8000/v1/ready > "$OUT_DIR/ready.json" 2>&1 || true

tar -czf "$OUT_DIR.tar.gz" -C "$(dirname "$OUT_DIR")" "$(basename "$OUT_DIR")"

echo "$OUT_DIR.tar.gz"
