# ANALYZER_REPO_STRUCTURE_MAP.md

## 1. Current Mode

STABILIZATION ONLY

No new features.

No refactor.

No file deletion.

No formula movement.

No live backend connection.

No payment.

No auth / profile / history.

No PDF / report generation.

No Verify UI.

No Admin / Data publishing.

This file is a documentation-only structure lock for `kurgin-score-analyzer` before any cleanup, deletion, refactor, or ownership decision.

## 2. Repository Role

`kurgin-score-analyzer` is responsible for:

- Analyzer SDK / API;
- Excel / Mass Analyzer logic or contracts;
- public-safe adapter boundary;
- API / staging integration;
- contract and smoke tests;
- future PDF / report-related planning only, not production implementation.

`kurgin-score-analyzer` is not responsible for:

- public Streamlit UI;
- catalog publishing;
- payment;
- auth / profile / history;
- Admin UI;
- Data repo publishing;
- formula editing UI;
- direct public exposure of formula internals.

## 3. Active Execution Path

### Main active path

```text
input validation
→ formula / core engine
→ private engine result
→ sanitizer / public-safe adapter
→ API / service output
```

### Main entrypoints

- `kurgin_core/`
- `kurgin_core/analyzer.py`
- `app.py` — legacy / Streamlit-facing analyzer entrypoint; not the platform public UI path.

STATUS: NEEDS CONFIRMATION for which non-API entrypoint should remain canonical after Formula Service extraction.

### API entrypoints

- `api/`
- `api/main.py`
- `api/routes/`
- `api/services/`
- `api/services/core_service.py`

### Public-safe adapter entrypoints

- `platform_integration/public_safe_analyzer_adapter.py`
- `platform_integration/public_analyzer_preview_service.py`

### Service / client boundaries

- `formula_client/engine_client.py`
- `formula_client/cloud_client.py`
- `formula_client/local_client.py`

### Contract tests protecting the active path

- `.github/workflows/ci.yml`
- `scripts/contract_test_public_safe_adapter.py`
- `scripts/contract_test_public_preview_service.py`
- `scripts/contract_test_formula_client.py`
- `scripts/contract_test_output_schema.py`
- `scripts/contract_test_api.py`
- `scripts/smoke_test_core.py`
- `scripts/smoke_test_selectel_formula_staging.py`
- `scripts/compare_local_vs_cloud_formula.py`
- `formula_comparison/regression_runner.py`
- `golden_dataset/`

## 4. Public-Safe Adapter Boundary

Public-safe output is produced through:

- `platform_integration/public_safe_analyzer_adapter.py`
- `platform_integration/public_analyzer_preview_service.py`

The public output contract must stay limited to public-safe fields such as:

- `status`
- `score_band`
- `summary`
- `warnings`
- `limitations`
- `next_action`

Public output must not expose:

- `diagnostics`
- `breakdown`
- `triple_score`
- `structure_modifier`
- `raw_formula`
- `weights`
- `penalty_breakdown`
- `internal_diagnostics`
- `debug_trace`
- `traceback`
- `exception`
- `raw_engine_output`
- `formula_source`
- `coefficient_formula`
- `certificate_claim`
- `appraisal_claim`
- `price_effect`
- `payment_effect`
- `reserve_effect`
- `order_effect`

Public-safe adapter files must not become product UI files.

Public-safe adapter files must not create payment, profile, storage, Verify, or PDF behavior.

## 5. Formula Service Boundary

Formula Service remains a private / staging API boundary.

Known connection points:

- `formula_client/engine_client.py`
- `formula_client/cloud_client.py`
- `formula_client/local_client.py`
- `deployment/selectel_staging/`
- `selectel_formula_service_scaffold/`
- `scripts/smoke_test_selectel_formula_staging.py`
- `scripts/compare_local_vs_cloud_formula.py`

Rules:

- Do not move formula logic.
- Do not duplicate formula logic.
- Do not expose private formula internals.
- Do not let public UI import Formula Service internals.
- Keep cloud/local equivalence checks before promoting staging changes.

STATUS: BOUNDARY NEEDS CONTRACT CONFIRMATION for any future public-facing live integration.

## 6. Excel / Mass Analyzer Area

Files and folders related to Excel / Mass Analyzer:

- `excel_tools.py`
- `excel_processing/` if present
- `excel_output/` if present
- `report_templates/`
- `formula_comparison/`
- `golden_dataset/`
- batch-related SDK paths in `kurgin_core/`
- batch/export service paths in `api/services/`

Roles:

- Excel processing;
- batch analysis;
- validation;
- preview / issue classification;
- row-detail-ready outputs;
- workbook / package export;
- Mass Analyzer contracts.

Rules:

- Do not implement real Excel upload as part of stabilization.
- Do not refactor `excel_tools.py` without schema / regression tests.
- Do not expand Excel behavior without a separate task.
- Do not connect Mass Analyzer to catalog publishing.
- Do not create orders, reserves, payments, or public catalog writes from batch results.

## 7. API / Staging Area

API and staging-related files:

- `api/`
- `api/routes/`
- `api/services/`
- `api/config.py`
- `api/security.py`
- `deployment/selectel_staging/`
- `selectel_formula_service_scaffold/`
- `SELECTEL_PRIVATE_BOUNDARY.md` if present
- `SELECTEL_STAGING_PLAN.md` if present
- `scripts/smoke_test_selectel_formula_staging.py`
- `scripts/compare_local_vs_cloud_formula.py`
- `scripts/contract_test_formula_client.py`

Rules:

- API routes are not public Streamlit UI.
- Staging scaffolds are not production service by default.
- Selectel/cloud paths must not bypass contract tests.
- Staging scripts must not expose secrets.

## 8. Legacy / Unclear Area

Potential legacy / unclear zones:

- `ui_pages/` — LEGACY CANDIDATE
- old Streamlit / prototype files — NEEDS OWNER REVIEW
- older docs — UNCLEAR unless referenced by current contracts
- duplicate OpenAPI versions / `api_docs/` — NEEDS OWNER REVIEW
- release notes / sync manifests — UNCLEAR
- abandoned scaffold folders if present — DO NOT TOUCH UNTIL TEST COVERAGE EXISTS
- `app.py` as public platform path — LEGACY CANDIDATE / NEEDS OWNER REVIEW

Rules:

- Do not delete these files during stabilization.
- Do not rename them during stabilization.
- Do not move them during stabilization.
- Do not promote them to current production path without owner review.
- Do not connect public MVP UI to these files without a separate integration task.

## 9. Protected Area

Protected files / folders:

- `core_formula/`
- `config_settings/engine_config.py`
- `formula_modules/`
- `validation/`
- `data_models/`
- `kurgin_core/`
- `formula_client/`
- `golden_dataset/`
- `formula_comparison/`
- `formula_versions/` if present
- `formula_candidates/` if present
- `excel_tools.py`
- `report_templates/`
- API response contracts
- output schema locks
- public-safe adapter contracts
- regression tests
- staging equivalence tests

Protected means:

- do not casually refactor;
- do not move;
- do not delete;
- do not expose through public UI;
- do not change public output fields without schema lock update;
- do not change formula/scoring behavior without a separate formula task.

## 10. Cross-Repo Boundary Check

This task must not modify:

- `kurgin-formula-service`
- `kurgin-streamlit-mvp`
- `kurgin-data`
- `kurgin-admin-mvp`

Boundary confirmations:

- Analyzer must not write to `kurgin-data`.
- Analyzer must not create payment / order / reserve flows.
- Analyzer must not create Verify records.
- Analyzer must not create PDF / report production flow.
- Streamlit public UI must not import Analyzer internals directly.
- Any future connection must go through adapter / API / contract boundary.

## 11. Known Risks

| Risk | Location | Why it matters | Current status | Safe next step |
|---|---|---|---|---|
| Unclear active path | `app.py`, `kurgin_core/`, `api/` | Multiple entrypoints can confuse what is production path | STATUS: NEEDS CONFIRMATION | Confirm canonical SDK/API entrypoints before cleanup |
| Formula / API / Excel / PDF / public adapter mixed together | `kurgin_core/`, `excel_tools.py`, `api/services/`, `platform_integration/` | Mixed responsibilities increase regression risk | Active but sensitive | Keep contracts and avoid broad refactor |
| Legacy UI confused with production path | `ui_pages/`, old Streamlit/prototype files, `app.py` | Public platform UI should not depend on legacy analyzer UI | LEGACY CANDIDATE / NEEDS OWNER REVIEW | Mark in docs, audit imports before any move/delete |
| Selectel scaffold confused with production service | `deployment/selectel_staging/`, `selectel_formula_service_scaffold/` | Scaffold can be mistaken for live service | STAGING | Keep staging docs and no-secret review |
| Formula candidates promoted without review | `formula_versions/`, `formula_candidates/`, `formula_comparison/` | Candidate formulas can alter scoring | PROTECTED / RESEARCH | Require regression and equivalence tests |
| Excel tools growing without schema/regression tests | `excel_tools.py`, `excel_output/`, `report_templates/` | Excel/PDF outputs can break silently | High risk | Add/keep schema and regression tests before refactor |
| Public-safe boundary leakage | `platform_integration/public_safe_analyzer_adapter.py` | Raw internals must never reach public MVP | Hardened by contract tests | Maintain public-safe contract tests |
| Missing or unknown CI status | `.github/workflows/ci.yml` | Stabilization requires evidence | CI green not confirmed by this docs task | Check latest Actions run after commit |
| Local formula and cloud formula drift | `formula_client/`, `scripts/compare_local_vs_cloud_formula.py` | Cloud extraction can diverge from local results | Requires equivalence checks | Run local-vs-cloud comparison before promoting |

## 12. CI / Smoke / Contract Proof

Tests to check when validating this repository:

- `scripts/contract_test_public_safe_adapter.py`
- `scripts/contract_test_public_preview_service.py`
- `scripts/compare_local_vs_cloud_formula.py`
- `scripts/smoke_test_selectel_formula_staging.py`

Additional relevant checks:

- `scripts/smoke_test_core.py`
- `scripts/contract_test_api.py`
- `scripts/contract_test_formula_client.py`
- `scripts/contract_test_output_schema.py`
- `formula_comparison/regression_runner.py`

This document is docs-only and does not run CI by itself.

CI green not confirmed.

## 13. Files Changed

files added:

- `ANALYZER_REPO_STRUCTURE_MAP.md`

files modified:

- none

files deleted:

- none

## 14. Cleanup Strategy

No immediate deletion.

Future cleanup should be staged.

### Phase 1

- docs-only structure map;
- verify CI / smoke;
- identify active paths.

### Phase 2

- mark legacy / review folders in docs;
- add tests before moving code.

### Phase 3

- extract constants / schemas from overloaded files if safe;
- keep external function names stable.

### Phase 4

- remove deprecated files only after usage audit.

## 15. Acceptance Criteria

This document is valid when:

- `ANALYZER_REPO_STRUCTURE_MAP.md` exists;
- it is docs-only;
- no code changes are made;
- no formula changes are made;
- no scoring changes are made;
- no Excel / PDF / API behavior changes are made;
- no file deletion / move is made;
- active / staging / research / legacy / protected zones are clearly classified;
- protected files / folders are clearly named;
- future cleanup order is documented.

## 16. Status

Status: STABILIZATION ONLY structure lock.

Version: V0.1
