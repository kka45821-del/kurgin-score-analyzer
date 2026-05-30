# KURGIN Score Analyzer Repository Structure Map V0.1

## 1. Purpose

This document maps the current `kurgin-score-analyzer` repository structure to reduce spaghetti-code risk.

It is a docs-only structure map.

It does not delete, move, rename, refactor, or reclassify files at runtime.

It does not change formula behavior, scoring behavior, API behavior, Excel export, PDF templates, or public output.

## 2. Main Analyzer Production Path

The main working path for Analyzer must remain explicit:

```text
input validation
→ formula / core engine
→ private engine result
→ sanitizer / public-safe adapter
→ API / service output
```

Interpretation:

1. Input is received and validated by API, SDK, Streamlit app, or service boundary.
2. Core SDK / engine path calls the formula engine.
3. Formula engine produces private/raw result objects or dictionaries.
4. Public surfaces must pass through sanitizer / public-safe adapter before external display.
5. API/service output must preserve the relevant contract and must not leak private formula internals.

## 3. Repository Categories

The repository should be read through these categories:

- `ACTIVE_ENGINE`
- `ACTIVE_API`
- `PUBLIC_SAFE_BOUNDARY`
- `ACTIVE_EXCEL_EXPORT`
- `ACTIVE_TESTS`
- `STAGING_DEPLOYMENT`
- `DOCS_CONTRACTS`
- `LEGACY_OR_REVIEW`
- `DO_NOT_TOUCH`

A file may be used by more than one runtime surface, but each file should still have one primary responsibility.

## 4. ACTIVE_ENGINE

### Files / folders

- `kurgin_core/`
- `kurgin_core/analyzer.py`
- `formula_client/`
- `formula_client/engine_client.py`
- `formula_client/local_client.py`
- `formula_client/cloud_client.py`
- `formula_modules/`
- `config_settings/`
- `excel_tools.py`
- engine-related constants and config used by the core SDK

### Role

This category is the active calculation and SDK layer.

`kurgin_core/analyzer.py` is the SDK-style entry point. It calls `process_single_stone`, `process_dataframe`, export helpers, and formula-client mode selection.

`formula_client/engine_client.py` controls local / cloud / cloud_fallback formula execution modes.

`formula_modules/` and formula-related config are internal calculation modules.

### Can this be changed now?

Only with explicit formula / scoring task scope.

Not during docs, public UI, public-safe adapter, or Streamlit MVP stabilization tasks.

### Risk

High.

Changes may alter scoring behavior, formula results, local-vs-cloud equivalence, Excel outputs, API payloads, or regression results.

### Do not

- Do not change formula/scoring without a dedicated formula task.
- Do not change cloud/local mode behavior casually.
- Do not expose formula internals to public adapters.
- Do not mix commercial access, payment, profile, or UI logic here.
- Do not use this layer directly from public Streamlit MVP UI.

## 5. ACTIVE_API

### Files / folders

- `api/`
- `api/main.py`
- `api/routes/`
- `api/services/`
- `api/services/core_service.py`
- `api/config.py`
- `api/security.py`
- `api/errors.py`
- `api/middleware.py`

### Role

This category is the FastAPI / service wrapper around the Analyzer SDK.

`api/main.py` creates the API app and includes routers.

`api/services/core_service.py` calls `kurgin_core` functions, sanitizes basic JSON values, and exposes service operations for analysis and export.

### Can this be changed now?

Only for explicit API contract tasks.

Not during formula, Streamlit MVP public UI, docs-only, or adapter-only tasks.

### Risk

High.

Changes may alter existing API behavior, response format, CORS/security behavior, API stability, and downstream clients.

### Do not

- Do not change endpoint paths without explicit API migration task.
- Do not bypass existing sanitization.
- Do not add payment/auth/profile/report features here without approved architecture.
- Do not expose private formula internals through API responses.
- Do not modify `app.py` or public UI as part of API hardening unless explicitly required.

## 6. PUBLIC_SAFE_BOUNDARY

### Files / folders

- `platform_integration/public_safe_analyzer_adapter.py`
- `platform_integration/public_analyzer_preview_service.py`
- `scripts/contract_test_public_safe_adapter.py`
- `scripts/contract_test_public_preview_service.py`

### Role

This category is the public-safe transformation boundary.

`public_safe_analyzer_adapter.py` converts raw/private Analyzer output into a limited public-safe payload.

Allowed public-safe output fields:

- `status`
- `score_band`
- `summary`
- `warnings`
- `limitations`
- `next_action`

Blocked internal fields include formula diagnostics, raw formula data, private engine output, pricing/payment/order effects, certificate/appraisal claims, traceback, and exception data.

`public_analyzer_preview_service.py` is the safe future integration layer for public preview use cases. It maps public input into Analyzer input and sanitizes output through the public-safe adapter.

### Can this be changed now?

Yes, but only for public-boundary hardening, contract tests, or safe adapter tasks.

### Risk

Medium to high.

This layer protects public products from private formula leakage.

### Do not

- Do not add extra public fields without public-output contract review.
- Do not expose `diagnostics`, `breakdown`, `triple_score`, `structure_modifier`, `raw_formula`, `weights`, `raw_engine_output`, `debug_trace`, or formula source.
- Do not add commercial, payment, PDF, Verify, or profile behavior here.
- Do not call Streamlit UI from this layer.
- Do not bypass this layer for public MVP integration.

## 7. ACTIVE_EXCEL_EXPORT

### Files / folders

- `excel_output/`
- `excel_output/final_export.py`
- Excel workbook/export helpers used by the Analyzer
- `report_templates/`
- `formula_comparison/`
- `golden_dataset/`

### Role

This category supports Analyzer Excel output, workbook generation, regression comparison, and golden-dataset checks.

`golden_dataset/` and `formula_comparison/` are used to preserve regression expectations and compare formula versions.

### Can this be changed now?

Only for explicit Excel/export/regression tasks.

### Risk

High.

Changes may break client-facing Excel output, reporting consistency, or CI regression checks.

### Do not

- Do not refactor `excel_tools.py` casually.
- Do not change Excel output fields without a schema/contract task.
- Do not change regression dataset paths without CI validation.
- Do not mix public-safe preview behavior into Excel export internals.
- Do not change PDF templates as part of Excel skeleton work.

## 8. ACTIVE_TESTS

### Files / folders

- `.github/workflows/ci.yml`
- `scripts/ci_compile.py`
- `scripts/ci_repo_hygiene.py`
- `scripts/smoke_test_core.py`
- `scripts/contract_test_api.py`
- `scripts/smoke_test_platform_card.py`
- `scripts/contract_test_formula_client.py`
- `scripts/contract_test_public_safe_adapter.py`
- `scripts/contract_test_public_preview_service.py`
- `scripts/contract_test_output_schema.py`
- `scripts/smoke_test_selectel_formula_staging.py`
- `scripts/compare_local_vs_cloud_formula.py`
- regression runner checks under `formula_comparison/`

### Role

This category protects compile safety, core SDK behavior, API contracts, formula client contracts, public-safe adapter behavior, output schema, live staging smoke, local-vs-cloud equivalence, and formula regression.

### Can this be changed now?

Yes, for test hardening or contract corrections.

### Risk

Medium.

Bad test changes can hide real regressions or produce false failures.

### Do not

- Do not weaken tests to make CI pass.
- Do not remove contract checks without replacement.
- Do not print secrets or live API keys.
- Do not make live smoke mandatory when environment variables are absent.
- Do not mix test fixes with formula/scoring changes.

## 9. STAGING_DEPLOYMENT

### Files / folders

- `deployment/`
- `deployment/selectel_staging/`
- `selectel_formula_service_scaffold/`
- staging scripts / deployment notes / scaffold files

### Role

This category supports staging, deployment experiments, and Formula Service scaffolding.

It is not the production source of truth for the formula itself.

### Can this be changed now?

Only for explicit staging/deployment tasks.

### Risk

Medium to high.

Deployment scaffolds can be confused with production service code.

### Do not

- Do not treat `deployment/selectel_staging/` as production-ready by default.
- Do not copy secrets into repo.
- Do not deploy production from scaffold files without review.
- Do not change formula behavior from deployment scaffolds.
- Do not assume scaffold placeholders are live service implementation.

## 10. DOCS_CONTRACTS

### Files / folders

- `docs/`
- contract docs
- planning docs
- structure maps
- public-output locks
- architecture notes

### Role

This category records decisions, contracts, boundaries, and future planning.

Docs can describe future states but must not imply implementation in the current MVP unless code and CI also prove it.

### Can this be changed now?

Yes, for docs-only tasks.

### Risk

Low to medium.

Docs may create confusion if they sound like implemented behavior.

### Do not

- Do not describe planning as already implemented.
- Do not change code during docs-only tasks.
- Do not introduce new claims, pricing, certification, or production launch promises.
- Do not use docs to bypass existing code contracts.

## 11. LEGACY_OR_REVIEW

### Files / folders

- `ui_pages/`
- older Streamlit/page prototypes
- old UI helpers not in the active API/SDK path
- older integration experiments
- `api_docs/` old OpenAPI or historical API descriptions
- other folders not referenced by current CI or active SDK/API path

### Role

This category may contain legacy UI, review-only material, historical API references, or experimental surfaces.

It may be useful for reference, but it is not the main production path.

### Can this be changed now?

Only after confirming current usage.

### Risk

Medium.

Legacy files are easy to mistake for active production code.

### Do not

- Do not assume `ui_pages/` is the main production path.
- Do not treat old `api_docs/openapi` versions as source of truth.
- Do not refactor legacy files into active code without a migration task.
- Do not delete legacy/review files in stabilization tasks.
- Do not connect public MVP to legacy UI files without review.

## 12. DO_NOT_TOUCH

### Files / folders / areas

- private formula internals unless explicit formula task is active;
- scoring formulas and thresholds;
- `excel_tools.py` during public UI / docs / adapter tasks;
- PDF templates during Analyzer skeleton tasks;
- existing API behavior during docs and public adapter tasks;
- secrets, keys, `.env` values, deployment credentials;
- golden dataset expectations unless regression task requires it;
- Formula Service repo and live service code from this repo task.

### Role

This category contains sensitive or high-blast-radius areas.

### Can this be changed now?

No, unless the current task explicitly names that file or behavior.

### Risk

Very high.

### Do not

- Do not change formula/scoring behavior.
- Do not change API output contracts.
- Do not change Excel/PDF/report output fields.
- Do not alter secrets or env names.
- Do not add payment/auth/profile/storage/PDF/Verify UI.
- Do not change public output shape without contract review.

## 13. Explicit Notes

### `ui_pages/`

`ui_pages/` is not the main production path for Analyzer calculation or API output.

Treat it as legacy/review unless a specific active task proves otherwise.

### `deployment/selectel_staging/`

`deployment/selectel_staging/` is staging-oriented.

It is not production-ready by default.

### `api_docs/openapi` old versions

Old OpenAPI files and historical API docs are not source of truth unless explicitly regenerated and approved.

The active API source of truth is the current API code and current contract tests.

### `public_safe_analyzer_adapter.py`

`platform_integration/public_safe_analyzer_adapter.py` is the sanitizer layer for public-safe output.

Public MVP surfaces must not receive raw Analyzer or formula output directly.

### Formula internals

Formula internals must not reach public output.

Raw/private fields such as diagnostics, breakdown, triple_score, structure_modifier, raw_formula, weights, raw_engine_output, debug_trace, formula_source, coefficient_formula, certificate_claim, appraisal_claim, price_effect, order_effect, reserve_effect, and payment_effect must stay blocked from public-safe output.

## 14. Change Policy

Before changing a file, identify its category.

If the file belongs to `ACTIVE_ENGINE`, `ACTIVE_API`, `ACTIVE_EXCEL_EXPORT`, or `DO_NOT_TOUCH`, require a precise task and test plan.

If the file belongs to `PUBLIC_SAFE_BOUNDARY`, require a public-output contract test.

If the file belongs to `STAGING_DEPLOYMENT`, require staging scope and no-secret review.

If the file belongs to `LEGACY_OR_REVIEW`, confirm whether it is active before changing it.

No files should be deleted or moved as part of stabilization unless a separate repository cleanup task explicitly authorizes it.

## 15. Acceptance Criteria

This document is valid when:

- it exists at `docs/ANALYZER_REPO_STRUCTURE_MAP_V0_1.md`;
- it identifies the active production path;
- it categorizes key folders and files;
- it makes clear that legacy, staging, and docs are not the main production path;
- it does not change code;
- it does not change CI;
- it does not change formula/scoring/API/Excel/PDF behavior.

## 16. Status

Status: structure map lock for stabilization.

Version: V0.1
