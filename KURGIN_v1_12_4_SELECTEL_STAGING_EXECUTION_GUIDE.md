# KURGIN Formula API — Selectel Staging Execution Guide

Version: v1.12.4

## Purpose

This guide turns the staging plan into executable server steps.

## Server assumptions

- Ubuntu 22.04/24.04
- SSH access
- root or sudo access
- GitHub repo accessible
- Docker allowed

## Step 1 — Bootstrap server

Copy scripts to server or use repository after clone.

As root:

```bash
sudo bash deployment/selectel_staging/server_scripts/01_bootstrap_ubuntu_docker.sh
```

## Step 2 — Clone/update repository

```bash
sudo -u $USER bash deployment/selectel_staging/server_scripts/02_clone_or_update_repo.sh
```

If scripts are not on server yet:

```bash
mkdir -p /opt/kurgin
cd /opt/kurgin
git clone https://github.com/kka45821-del/kurgin-score-analyzer.git
cd kurgin-score-analyzer
```

Then continue from repo root.

## Step 3 — Create staging env

```bash
bash deployment/selectel_staging/server_scripts/03_create_env_staging.sh
```

Save the printed API secret.

Edit `.env.staging`:

```text
KURGIN_ALLOWED_ORIGINS=https://your-staging-platform-domain
```

## Step 4 — Start API

```bash
bash deployment/selectel_staging/server_scripts/04_start_staging_container.sh
```

## Step 5 — Run smoke test

```bash
bash deployment/selectel_staging/server_scripts/05_run_staging_smoke.sh
```

Expected result:

```json
{
  "status": "OK",
  "health": "ok",
  "ready": "ready",
  "score": 100,
  "class": "Элитный"
}
```

## Step 6 — Check external access

If reverse proxy is configured:

```bash
curl https://formula-staging.example/v1/health
```

Analyze with API key:

```bash
curl -X POST https://formula-staging.example/v1/analyze/stone \
  -H "Content-Type: application/json" \
  -H "X-KURGIN-API-Key: <secret>" \
  -d '{"language":"RU","stone":{"Shape":"ROUND","Report #":"STAGING","Lab":"IGI","Weight":1,"Measurements":"6.430x6.470x3.970","CrownAngle":34.5,"PavilionAngle":40.8,"TablePercent":56,"DepthPercent":61.5,"CrownPercent":15,"PavilionPercent":43,"GirdlePercent":3.5}}'
```

## Update staging later

```bash
bash deployment/selectel_staging/server_scripts/06_update_staging.sh
```

## Collect diagnostics

```bash
bash deployment/selectel_staging/server_scripts/07_collect_diagnostics.sh
```

Send the generated `.tar.gz` if debugging is needed.
