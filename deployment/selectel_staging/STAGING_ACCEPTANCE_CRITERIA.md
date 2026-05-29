# Staging Acceptance Criteria

Staging is accepted when all checks pass.

## API health

- `/v1/health` returns `status=ok`.
- `/v1/ready` returns `status=ready`.

## Auth

- Request without API key fails when secret is configured.
- Request with API key succeeds.

## Core functions

- `/v1/analyze/stone` returns `Calculation Status=OK`.
- `/v1/platform/stone-card` returns `kind=kurgin_score_result_card`.
- `/v1/export/stone/pdf` returns PDF bytes.
- `/v1/analyze/batch/json` returns `rows_ok >= 1`.

## Deployment

- Docker container restarts cleanly.
- Healthcheck passes.
- Logs are readable.
- No formula code is exposed to browser bundle.

## Production gate

Do not move to production until:

- API contract is stable.
- Platform backend integration is tested.
- Visual validation path remains separate from official formula.
- Secrets and deployment process are documented.
