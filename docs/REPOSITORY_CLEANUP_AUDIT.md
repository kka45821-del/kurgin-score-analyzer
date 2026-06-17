# Repository cleanup audit

This document records the repository cleanup audit before any destructive cleanup.

## Current conclusion

- The repository is not large by file size.
- The main issue is structural clarity: production code, Streamlit UI, historical experiments, contracts, docs, and validation assets are mixed at the top level.
- The first cleanup step should be documentation-only. Do not delete code or folders in the first cleanup PR.
- Deletions should be done later in separate, small PRs with tests.

## Production / active core

These paths are treated as active and should not be removed during cleanup without a dedicated replacement plan.

| Path | Tracked files | Notes |
|---|---:|---|
| `app.py` | 1 | Main Streamlit entrypoint. |
| `excel_tools.py` | 1 | Single-stone and Excel export processing. |
| `excel_output` | 5 | Active Excel export/output module area. Do not treat as generated local output. |
| `core_formula` | 4 | Core scoring engine. |
| `formula_modules` | 23 | Formula modules, interpretation, tags, measurement spread logic. |
| `kurgin_core` | 3 | KURGIN core package/module area. |
| `config_settings` | 2 | Runtime thresholds and engine settings. |
| `translations_lang` | 4 | Public labels and tag translations. |
| `report_templates` | 4 | PDF and report schema templates. |
| `validation` | 2 | Input and processing validation. |
| `tests` | 2 | Automated and regression tests. |
| `requirements.txt` | 1 | Application dependencies. |
| `requirements-core.txt` | 1 | Core dependencies. |
| `packages.txt` | 1 | System packages for Streamlit/PDF font support. |

## UI / Streamlit layer

These paths are part of the user-facing Streamlit layer.

| Path | Tracked files | Notes |
|---|---:|---|
| `ui_pages` | 61 | Streamlit page/module mirror layer. Sync-sensitive. |
| `.streamlit` | 1 | Streamlit configuration. |
| `assets` | 1 | Branding and static assets. |

## Integration / deployment layer

These paths may be active for staging, API contracts, platform integration, or deployment. Do not delete without checking the current deployment path.

| Path | Tracked files |
|---|---:|
| `api` | 15 |
| `deployment` | 22 |
| `platform_config` | 2 |
| `platform_integration` | 9 |
| `formula_client` | 5 |
| `access_control` | 2 |

## Historical / review candidates

These paths are candidates for later cleanup, archiving, or consolidation. They are not automatically safe to delete.

| Path | Tracked files | Initial action |
|---|---:|---|
| `baseline_reports` | 1 | Check whether these are generated outputs or required fixtures. |
| `candidate_reports` | 1 | Check whether these are generated outputs or required fixtures. |
| `candidate_review_v1_11_6` | 1 | Review usage before deletion or archiving. |
| `formula_candidates` | 7 | Likely historical formula work; preserve until formula lineage is documented. |
| `formula_comparison` | 4 | Likely historical formula work; preserve until formula lineage is documented. |
| `formula_versions` | 11 | Likely historical formula work; preserve until formula lineage is documented. |
| `golden_dataset` | 1 | Keep unless replaced by a formal regression fixture location. |
| `selectel_formula_service_scaffold` | 7 | Check whether external service extraction still needs this scaffold. |
| `visual_market_validation` | 5 | Review usage before deletion or archiving. |
| `visual_validation_results_readiness` | 1 | Review usage before deletion or archiving. |
| `api_docs` | 5 | Review usage before deletion or archiving. |
| `api_contract` | 3 | Review usage before deletion or archiving. |

## Documentation / planning files

These should be consolidated later, not deleted blindly.

| Path | Tracked files |
|---|---:|
| `docs` | 3 |
| `README.txt` | 1 |
| `README_INTEGRATION.md` | 1 |
| `RELEASE_NOTES_v1_12_2.md` | 1 |
| `REGRESSION_WORKFLOW.md` | 1 |
| `ANALYZER_CLEANUP_PLAN.md` | 1 |
| `ANALYZER_OUTPUT_SCHEMA_LOCK.md` | 1 |
| `ANALYZER_REPO_STRUCTURE_MAP.md` | 1 |
| `REPOSITORY_CLEANUP_NOTES.md` | 1 |
| `FORMULA_CANDIDATE_PLAN_v1_11_4.md` | 1 |
| `GITHUB_SYNC_INSTRUCTIONS.md` | 1 |
| `SELECTEL_PRIVATE_BOUNDARY.md` | 1 |
| `SELECTEL_STAGING_PLAN.md` | 1 |

## ui_pages mirror risk

Files below exist in both root modules and `ui_pages`. They are sync-sensitive. Recent PR #25 fixed one such mirror for score-band text templates.

| ui_pages file | Root counterpart |
|---|---|
| `ui_pages/.gitignore` | `.gitignore` |
| `ui_pages/.streamlit/config.toml` | `.streamlit/config.toml` |
| `ui_pages/README.txt` | `README.txt` |
| `ui_pages/access_control/__init__.py` | `access_control/__init__.py` |
| `ui_pages/access_control/access_manager.py` | `access_control/access_manager.py` |
| `ui_pages/app.py` | `app.py` |
| `ui_pages/config_settings/__init__.py` | `config_settings/__init__.py` |
| `ui_pages/config_settings/engine_config.py` | `config_settings/engine_config.py` |
| `ui_pages/core_formula/__init__.py` | `core_formula/__init__.py` |
| `ui_pages/core_formula/main_engine.py` | `core_formula/main_engine.py` |
| `ui_pages/core_formula/structure_engine.py` | `core_formula/structure_engine.py` |
| `ui_pages/core_formula/triple_engine.py` | `core_formula/triple_engine.py` |
| `ui_pages/data_models/__init__.py` | `data_models/__init__.py` |
| `ui_pages/data_models/stone.py` | `data_models/stone.py` |
| `ui_pages/excel_processing/__init__.py` | `excel_processing/__init__.py` |
| `ui_pages/excel_processing/column_mapping.py` | `excel_processing/column_mapping.py` |
| `ui_pages/excel_tools.py` | `excel_tools.py` |
| `ui_pages/formula_client/README.md` | `formula_client/README.md` |
| `ui_pages/formula_client/__init__.py` | `formula_client/__init__.py` |
| `ui_pages/formula_client/cloud_client.py` | `formula_client/cloud_client.py` |
| `ui_pages/formula_client/engine_client.py` | `formula_client/engine_client.py` |
| `ui_pages/formula_client/local_client.py` | `formula_client/local_client.py` |
| `ui_pages/formula_modules/README.md` | `formula_modules/README.md` |
| `ui_pages/formula_modules/__init__.py` | `formula_modules/__init__.py` |
| `ui_pages/formula_modules/interpretation/__init__.py` | `formula_modules/interpretation/__init__.py` |
| `ui_pages/formula_modules/interpretation/disclaimer_templates.py` | `formula_modules/interpretation/disclaimer_templates.py` |
| `ui_pages/formula_modules/interpretation/interpretation_engine.py` | `formula_modules/interpretation/interpretation_engine.py` |
| `ui_pages/formula_modules/interpretation/recommendation_templates.py` | `formula_modules/interpretation/recommendation_templates.py` |
| `ui_pages/formula_modules/interpretation/report_text_builder.py` | `formula_modules/interpretation/report_text_builder.py` |
| `ui_pages/formula_modules/interpretation/risk_templates.py` | `formula_modules/interpretation/risk_templates.py` |
| `ui_pages/formula_modules/interpretation/score_band_interpreter.py` | `formula_modules/interpretation/score_band_interpreter.py` |
| `ui_pages/formula_modules/interpretation/score_text_templates.py` | `formula_modules/interpretation/score_text_templates.py` |
| `ui_pages/formula_modules/interpretation/tag_templates.py` | `formula_modules/interpretation/tag_templates.py` |
| `ui_pages/formula_modules/interpretation/text_style.py` | `formula_modules/interpretation/text_style.py` |
| `ui_pages/formula_modules/interpretation/verdict_templates.py` | `formula_modules/interpretation/verdict_templates.py` |
| `ui_pages/formula_modules/light_transport/__init__.py` | `formula_modules/light_transport/__init__.py` |
| `ui_pages/formula_modules/spread/__init__.py` | `formula_modules/spread/__init__.py` |
| `ui_pages/formula_modules/structure/__init__.py` | `formula_modules/structure/__init__.py` |
| `ui_pages/formula_modules/tags/__init__.py` | `formula_modules/tags/__init__.py` |
| `ui_pages/formula_modules/tags/tag_registry.py` | `formula_modules/tags/tag_registry.py` |
| `ui_pages/formula_modules/triple/__init__.py` | `formula_modules/triple/__init__.py` |
| `ui_pages/platform_config/__init__.py` | `platform_config/__init__.py` |
| `ui_pages/platform_config/app_config.py` | `platform_config/app_config.py` |
| `ui_pages/report_templates/__init__.py` | `report_templates/__init__.py` |
| `ui_pages/report_templates/pdf_single_stone_report.py` | `report_templates/pdf_single_stone_report.py` |
| `ui_pages/report_templates/report_columns.py` | `report_templates/report_columns.py` |
| `ui_pages/requirements.txt` | `requirements.txt` |
| `ui_pages/translations_lang/__init__.py` | `translations_lang/__init__.py` |
| `ui_pages/translations_lang/en.py` | `translations_lang/en.py` |
| `ui_pages/translations_lang/label_translator.py` | `translations_lang/label_translator.py` |
| `ui_pages/translations_lang/ru.py` | `translations_lang/ru.py` |
| `ui_pages/ui_pages/__init__.py` | `ui_pages/__init__.py` |
| `ui_pages/ui_pages/analytics_page.py` | `ui_pages/analytics_page.py` |
| `ui_pages/ui_pages/debug_page.py` | `ui_pages/debug_page.py` |
| `ui_pages/ui_pages/download_page.py` | `ui_pages/download_page.py` |
| `ui_pages/validation/__init__.py` | `validation/__init__.py` |
| `ui_pages/validation/input_validator.py` | `validation/input_validator.py` |

## Recommended cleanup order

1. Commit this audit document only.
2. Add or update README with the current production path and module responsibilities.
3. Add a `.gitignore` rule only for clearly generated local audit/output files if they keep reappearing.
4. Review generated/output folders separately.
5. Review historical formula folders separately.
6. Review documentation consolidation separately.
7. Do not remove `ui_pages` mirrors until Streamlit routing and imports are explicitly refactored.

## Current no-delete rule

No folder should be deleted in the first cleanup PR. The first PR is documentation-only to reduce risk.
