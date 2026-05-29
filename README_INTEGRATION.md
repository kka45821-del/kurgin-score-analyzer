# KURGIN Score Analyzer Integration Notes

Current route chosen: prepare the analyzer as a reusable core for future KURGIN Platform integration.

## What to use in KURGIN Platform

Prefer importing from:

```python
from kurgin_core import analyze_stone, analyze_dataframe, export_pdf, export_excel
```

Do not couple KURGIN Platform to Streamlit UI.

## Stable integration functions

- `analyze_stone(params, language="RU")`
- `analyze_dataframe(df, language="RU")`
- `export_pdf(stone_result, language="BILINGUAL")`
- `export_excel(batch)`
- `export_analysis_package(batch, pdf_mode="all_ok" | "top_only" | "none")`

## Current architecture

```text
kurgin_core/            integration SDK
core_formula/           current local formula engine
formula_modules/        interpretation, measurement/spread, policy modules
excel_processing/       upload recognition and data quality
report_templates/       Excel/PDF report generation
app.py                  temporary/dev Streamlit interface
```

## Future Selectel hidden formula deployment

The hidden backend should keep:

```text
core_formula/
config_settings/
formula_modules/
formula_client/local_client.py
```

KURGIN Platform should call Formula API, not copy formula coefficients to frontend.


## v1.11.2 Formula Versioning

New folders:

```text
formula_versions/
formula_comparison/
golden_dataset/
```

Use them before changing official formula logic.


## v1.11.3 Real Baseline

Added `baseline_reports/` with:
- real golden dataset
- baseline current formula report
- supplier file summary
- diameter review cases
- high score diameter review cases
- issues export
- regression report on real cases

This stage does not change official KURGIN Score.


## v1.11.4 Candidate Formula Design Brief

Added:
- `formula_candidates/v2_candidate/FORMULA_CANDIDATE_V2_BRIEF.md`
- `formula_candidates/v2_candidate/v2_candidate_rules.json`
- `formula_candidates/v2_candidate/ACCEPTANCE_CRITERIA.md`
- `formula_candidates/v2_candidate/IMPLEMENTATION_TASKS.md`
- `formula_candidates/v2_candidate/DECISION_LOG_TEMPLATE.md`

Official formula is not changed. Next stage should implement experimental class-cap-only candidate under `formula_versions/experimental/v2_candidate`.


## v1.11.5 Experimental Candidate v2

Implemented class-cap-only candidate under:

```text
formula_versions/experimental/v2_candidate/
```

Regression runner now supports `calculate_with_row(row, engine_kwargs)`.

Official `current` formula remains unchanged.


## v1.11.6 Candidate Review

Added candidate review artifacts:

```text
candidate_review_v1_11_6/
formula_candidates/v2_candidate/DECISION_LOG_v1_11_6.json
```

Conclusion: candidate is conservative and passes initial checks, but should not be promoted without visual/market validation.


## v1.11.7 Visual / Market Validation

Added:

```text
visual_market_validation/
```

This folder contains:
- validation workbook template;
- review queue seed;
- visual/market rubric;
- media manifest template;
- validation schema.

Official formula remains unchanged.


## v1.11.8 Visual Validation Results Analyzer

Added:

```text
visual_market_validation/analyze_validation_results.py
visual_market_validation/promotion_gate_rules.json
scripts/analyze_visual_validation.py
```

This stage analyzes a filled visual/market validation workbook and recommends whether candidate logic can move forward.

Official formula remains unchanged.


## v1.11.9 Core API Skeleton + Selectel Backend

Added:

```text
api/
api/routes/
api/services/
Dockerfile
docker-compose.yml
requirements-api.txt
deployment/selectel_ready/SELECTEL_API_DEPLOYMENT.md
```

This prepares the analyzer for private backend deployment.
Official KURGIN Score remains unchanged.


## v1.12.0 Selectel Staging Deployment Readiness

Added:
- request id middleware
- standardized error payload
- `/v1/ready`
- contract test script
- output contract draft
- platform client example
- staging/production env templates
- Docker healthcheck
- Selectel staging checklist

Official KURGIN Score remains unchanged.


## v1.12.1 Platform Integration Adapter

Added:

```text
platform_integration/
api/routes/platform.py
api/services/platform_card_service.py
```

New endpoint:

```text
POST /v1/platform/stone-card
```

This gives KURGIN Platform Tools page a compact card payload without exposing formula internals.


## v1.12.2 Repository Sync + CI Gate

Added:

```text
.github/workflows/ci.yml
scripts/ci_compile.py
scripts/ci_repo_hygiene.py
GITHUB_SYNC_INSTRUCTIONS.md
REPO_SYNC_MANIFEST.json
```

This package is ready to sync into `kka45821-del/kurgin-score-analyzer`.

Official KURGIN Score remains unchanged.


## v1.12.3 Selectel Staging Deployment Plan

Added:

```text
docker-compose.staging.yml
deployment/selectel_staging/
scripts/staging_smoke_test.py
scripts/validate_staging_env.py
scripts/generate_api_secret.py
```

This prepares the actual Selectel staging run. Official KURGIN Score remains unchanged.


## v1.12.4 Selectel Staging Execution Kit

Added executable server scripts under:

```text
deployment/selectel_staging/server_scripts/
```

This stage is ready for actual Selectel server execution.
Official KURGIN Score remains unchanged.
