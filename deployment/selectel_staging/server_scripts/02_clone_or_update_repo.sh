#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/kka45821-del/kurgin-score-analyzer.git}"
APP_DIR="${APP_DIR:-/opt/kurgin/kurgin-score-analyzer}"
BRANCH="${BRANCH:-main}"

echo "[KURGIN] Sync repo: $REPO_URL -> $APP_DIR"

mkdir -p "$(dirname "$APP_DIR")"

if [ -d "$APP_DIR/.git" ]; then
  cd "$APP_DIR"
  git fetch origin
  git checkout "$BRANCH"
  git pull origin "$BRANCH"
else
  git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
  cd "$APP_DIR"
fi

echo "[KURGIN] Current commit:"
git rev-parse HEAD
git log -1 --oneline
