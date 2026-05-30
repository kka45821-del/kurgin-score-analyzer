# SELECTEL_STAGING_PLAN.md

## Purpose

This document defines the controlled Selectel staging extraction plan for the KURGIN formula service.

This is a planning and staging-preparation document only. It does not deploy Selectel, remove local formula code, move production traffic, change scoring behavior, change Excel/PDF/API outputs, or change Admin/Public/PWA integration.

## Baseline references

This plan depends on two prior locks:

- `SELECTEL_PRIVATE_BOUNDARY.md` — defines what must become private and what may remain public/client-side.
- `ANALYZER_OUTPUT_SCHEMA_LOCK.md` — defines stable Analyzer Excel/API/PDF output surfaces.

Current baseline:

- CI green baseline is required before any staging extraction.
- Dependencies are pinned.
- Cloud formula client contract tests exist.
- Analyzer output schema lock exists.
- Current local formula remains in this repository during staging preparation.

## Non-goals

This task does not:

- deploy Selectel;
- remove `core_formula/` from this repository;
- delete `formula_client/local_client.py`;
- change formula weights;
- change scoring behavior;
- change Excel/PDF/API output schemas;
- change Admin integration;
- change Public/PWA integration;
- move production traffic;
- require a live Selectel endpoint in normal CI.

## 1. Private Selectel service package

The staging service should be a private repository or private deployment package. It should contain only what is needed to execute formula calculations and expose a minimal authenticated API.

### Required private formula files

Copy into the private Selectel service package:

```text
core_formula/
config_settings/engine_config.py
```

These files contain the official local formula implementation and configuration. They must remain private before production extraction.

### Required formula support modules

Copy only required support modules needed for formula execution and response compatibility.

Minimum likely set:

```text
formula_modules/interpretation/
formula_modules/measurement_spread/
validation/input_validator.py
data_models/stone.py
platform_config/app_config.py
translations_lang/
```

Decision rule:

- If the staging endpoint accepts already-normalized engine kwargs only, it may not need all upload/Excel modules.
- If the staging endpoint accepts certificate-style rows later, it will need `data_models/stone.py`, validation, enrichment, and possibly translation/interpretation modules.
- For the first staging API contract below, the endpoint accepts engine kwargs, so the private service can be minimal.

### Required version metadata

The private service must return version metadata from the same source used by formula execution.

Minimum metadata:

```text
engine_version
formula_service_version
build_id or git_sha
formula_contract_version
runtime_environment
```

The current `engine_version` must be returned in the formula response.

### Minimal private API wrapper

The private service should expose a minimal FastAPI or equivalent HTTP wrapper.

Required staging endpoint:

```text
POST /v1/formula/stone
```

Optional health endpoints:

```text
GET /health
GET /v1/health
GET /v1/ready
```

The private wrapper should not include Streamlit UI, Excel export, PDF generation, Admin UI, Public/PWA code, or unrelated Analyzer surfaces.

### Files not required in the first private formula package

For first staging extraction, do not copy unless explicitly needed:

```text
app.py
ui_pages/
report_templates/
excel_tools.py
excel_processing/
api/routes/platform.py
platform_integration/
visual_market_validation/
baseline_reports/
```

These may remain in the Analyzer repo while the formula service is tested as a calculation boundary.

## 2. Staging API contract

### Endpoint

```text
POST /v1/formula/stone
```

### Request headers

```text
Content-Type: application/json
Authorization: Bearer <FORMULA_API_KEY>
```

During staging, requests without a valid key should return `401` or `403`.

### Input shape

The initial staging endpoint should accept normalized engine kwargs. This avoids mixing upload parsing, Excel processing, PDF/report generation, and formula execution in the first private service.

```json
{
  "stone": {
    "crown_a": 34.5,
    "pav_a": 40.8,
    "table": 56,
    "depth": 61.5,
    "crown_p": 15,
    "pav_p": 43,
    "girdle_p": 3.5
  }
}
```

### Input validation

Required keys:

```text
crown_a
pav_a
table
depth
crown_p
pav_p
girdle_p
```

Validation rules:

- all required keys must be present;
- all values must be numeric;
- malformed input should return a structured 400 response;
- validation error responses must not expose stack traces or formula internals.

### Output shape

The staging output must match the current shape expected by `formula_client/cloud_client.py` and the mocked cloud formula contract tests.

Required fields:

```text
engine_version
final_score
final_verdict
triple_score
structure_modifier
structure_tags
visual_check
critical_risk
diagnostics
breakdown
```

Example:

```json
{
  "engine_version": "Kurgin Round Engine v1.2-dev",
  "final_score": 98.7,
  "final_verdict": "TOP: Excellent Selection",
  "triple_score": 98.0,
  "structure_modifier": 1.0071,
  "structure_tags": ["Perfect Build"],
  "visual_check": false,
  "critical_risk": false,
  "diagnostics": {
    "nailhead": 0.0,
    "fisheye": 0.0,
    "fire_loss": 0.0,
    "depth_dev": 0.0,
    "crown_dev": 0.0,
    "pavilion_dev": 0.0,
    "balance_err": 0.0,
    "girdle_penalty": 0.0,
    "ideal_depth": 61.5,
    "ideal_crown": 15.0,
    "ideal_pavilion": 43.0,
    "total_loss": 0.0
  },
  "breakdown": "..."
}
```

### Staging/internal-only fields

`breakdown` and raw `diagnostics` are allowed in staging/internal formula responses for equivalence checks.

They must not be returned to public/client outputs by default. This follows `SELECTEL_PRIVATE_BOUNDARY.md` and `ANALYZER_OUTPUT_SCHEMA_LOCK.md`.

### Public-safe equivalent later

Before production, public-facing adapters should return public-safe fields only, such as:

```text
score
class/verdict
public-safe tags
warning/recommendation
calculation_status
engine/output version
```

Raw formula internals should remain private/internal unless explicitly approved for authenticated professional/Admin surfaces.

## 3. Environment and secrets

### Analyzer staging environment

Analyzer staging should use:

```text
FORMULA_MODE=cloud_fallback
FORMULA_API_URL=<staging endpoint>/v1/formula/stone
FORMULA_API_KEY=<staging key>
```

### Private Formula Service staging environment

The private service should use its own service-side variables, for example:

```text
KURGIN_FORMULA_ENV=staging
KURGIN_FORMULA_API_KEY=<staging key>
KURGIN_FORMULA_SERVICE_VERSION=<version>
KURGIN_FORMULA_BUILD_ID=<git sha or build id>
```

The exact variable names can be adjusted by the deployment implementation, but secrets must remain server-side.

### Secret handling rules

Required rules:

- no committed `.env` files;
- no API keys in source code;
- no keys in logs;
- no keys in issue comments;
- no keys in Excel/PDF/System sheets;
- no keys in API responses;
- staging key must be separate from future production key;
- key rotation must be possible without code changes.

### Logging rules

Allowed in logs:

```text
request_id
status_code
latency_ms
failure_category
formula_service_version
engine_version
sanitized report/correlation id
```

Not allowed in logs:

```text
FORMULA_API_KEY
full request body if it contains sensitive supplier data
formula coefficients
stack traces returned to public clients
private endpoint credentials
```

## 4. Staging behavior

### Default staging mode

Staging should use:

```text
FORMULA_MODE=cloud_fallback
```

Reason:

- validates the Selectel cloud path;
- preserves local fallback if staging endpoint is temporarily unavailable;
- reduces risk while equivalence checks are being built.

### Fallback requirements

Fallback in staging is acceptable only if:

- fallback reason is logged;
- fallback count is visible in staging logs or monitoring;
- frequent fallback blocks promotion to production;
- equivalence checks still run separately against cloud.

### Production mode later

Production cloud-only behavior is out of scope for this issue.

Future production should use:

```text
FORMULA_MODE=cloud
```

Production should fail closed if the private Formula API is unavailable, unless a separate explicit security/business decision allows fallback.

## 5. Equivalence checks

Before production extraction, local and cloud formula results must be compared.

### Dataset

Use the existing golden dataset as the first equivalence source:

```text
golden_dataset/golden_dataset_template.csv
```

Later, add real supplier/baseline datasets if approved.

### Comparison procedure

For each row that is valid for current ROUND formula:

1. Convert row to engine kwargs.
2. Run local formula via current local implementation.
3. Run cloud formula through Selectel staging endpoint.
4. Compare numeric score.
5. Compare verdict/class.
6. Compare flags.
7. Compare tags.
8. Compare diagnostics if staging/internal mode allows it.
9. Produce a CSV summary.

### Tolerance

Initial numeric tolerance:

```text
absolute final_score delta <= 0.01
absolute triple_score delta <= 0.01
absolute structure_modifier delta <= 0.0001
```

Strict equality expected for:

```text
final_verdict
structure_tags
visual_check
critical_risk
input status for supported/unsupported rows
```

Any verdict/class change must be treated as a blocking discrepancy unless explicitly approved.

### Discrepancy classes

Use these discrepancy classes:

```text
OK
SCORE_DELTA
VERDICT_CHANGED
TAG_CHANGED
FLAG_CHANGED
DIAGNOSTIC_DELTA
CLOUD_ERROR
LOCAL_ERROR
INPUT_STATUS_MISMATCH
```

### Promotion gate

Staging is not eligible for production extraction if:

- cloud endpoint is unstable;
- fallback occurs frequently;
- any score delta exceeds tolerance;
- any verdict/class change occurs;
- tags or critical flags differ;
- output shape differs from `ANALYZER_OUTPUT_SCHEMA_LOCK.md`;
- public/client filtering violates `SELECTEL_PRIVATE_BOUNDARY.md`.

## 6. Tests

### Existing tests that stay

Existing mocked cloud tests remain normal CI tests:

```text
scripts/contract_test_formula_client.py
```

Existing output schema lock test remains normal CI test:

```text
scripts/contract_test_output_schema.py
```

These tests do not require live Selectel secrets.

### Tests to add later

Add later, after a staging endpoint exists:

```text
scripts/smoke_test_selectel_formula_staging.py
scripts/compare_local_vs_cloud_formula.py
```

The live staging smoke script should:

- run only when `FORMULA_API_URL` and `FORMULA_API_KEY` are configured;
- skip safely if secrets are absent;
- never print keys;
- verify `/v1/formula/stone` returns required fields;
- verify one known stone response shape;
- optionally compare score against local output.

The local-vs-cloud equivalence script should:

- load golden dataset;
- run local and cloud formula paths;
- write an internal comparison report;
- fail if deltas exceed tolerance;
- fail if verdict/classes/flags/tags differ.

### CI policy for live Selectel endpoint

Normal CI should not require a live Selectel endpoint.

Allowed CI behavior:

- mocked cloud tests always run;
- output schema lock tests always run;
- live Selectel staging smoke test only runs if secrets exist;
- if secrets are absent, live staging test prints a safe skip message and exits successfully.

## 7. Rollback plan

### Development rollback

For development:

```text
FORMULA_MODE=local
```

This uses the current local formula path.

### Staging rollback

For staging:

```text
FORMULA_MODE=cloud_fallback
```

This allows cloud validation while preserving local fallback.

If staging endpoint is unstable:

1. Keep Analyzer staging in `cloud_fallback`.
2. Review cloud failure logs.
3. Do not promote to production.
4. Fix private service in a separate task.
5. Re-run equivalence checks.

### Production rollback later

Production cloud-only is out of scope for this issue.

Future production rollback policy must be approved separately. Production fallback to local must not be enabled unless the public/client repo still has formula code and the security/business risk is accepted.

## 8. Implementation checklist for future Selectel staging task

### Preparation

- Confirm CI green on current public repo.
- Confirm `SELECTEL_PRIVATE_BOUNDARY.md` is accepted.
- Confirm `ANALYZER_OUTPUT_SCHEMA_LOCK.md` is accepted.
- Confirm dependency pinning remains valid.
- Confirm cloud contract tests pass.

### Private service package

- Create private Selectel service repository/package.
- Copy minimal private formula files.
- Add minimal API wrapper.
- Add auth check.
- Add health/ready endpoints.
- Add version metadata.
- Add staging deployment config.

### Analyzer staging config

- Set `FORMULA_MODE=cloud_fallback`.
- Set `FORMULA_API_URL` to staging endpoint.
- Set `FORMULA_API_KEY` as deployment secret.
- Confirm no secrets are committed.

### Validation

- Run mocked cloud tests.
- Run live staging smoke test if secrets exist.
- Run local-vs-cloud equivalence check.
- Review score deltas, verdicts, tags, flags.
- Review fallback logs.
- Review public response filtering.

### Promotion decision

Do not move to production extraction until:

- staging endpoint is stable;
- equivalence checks pass;
- fallback count is zero or understood;
- output schema lock remains valid;
- private/public boundary remains valid;
- no formula internals are exposed in public/client outputs.

## 9. Required future issues

Recommended follow-up issues:

1. Add live Selectel staging smoke script with safe secret-gated skip.
2. Add local-vs-cloud equivalence script using golden dataset.
3. Add cloud response schema validation in `formula_client/cloud_client.py`.
4. Add fallback reason logging for staging.
5. Create private Selectel formula service package.
6. Deploy Selectel staging service.
7. Run staging equivalence report.
8. Decide production cloud-only/fail-closed policy.
9. Remove private formula code from public/client repo in a separate approved task.

## 10. Acceptance criteria for this plan

This plan is complete when:

- `SELECTEL_STAGING_PLAN.md` exists;
- it references `SELECTEL_PRIVATE_BOUNDARY.md`;
- it references `ANALYZER_OUTPUT_SCHEMA_LOCK.md`;
- it defines private service contents;
- it defines endpoint contract;
- it defines environment variables and secrets policy;
- it defines staging mode;
- it defines equivalence checks and tolerance;
- it defines tests and CI policy;
- it defines rollback policy;
- no formula behavior is changed;
- no Selectel deployment is performed.
