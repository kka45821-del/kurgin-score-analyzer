# ANALYZER_CLEANUP_PLAN.md

## 1. Current Mode

STABILIZATION ONLY

DOCS-ONLY CLEANUP PLAN

NO CODE CHANGES

NO REFACTOR

NO DELETION

This plan is allowed only because:

- `ANALYZER_REPO_STRUCTURE_MAP.md` exists;
- CI / smoke proof has been confirmed externally;
- this cleanup plan does not execute cleanup.

This document is a planning lock only. It does not authorize cleanup execution.

## 2. Cleanup Objective

The objective is to reduce `kurgin-score-analyzer` repository complexity without damaging:

- formula correctness;
- public-safe adapter boundary;
- Excel / Mass Analyzer behavior;
- API contracts;
- staging Formula Service boundary;
- regression and schema tests;
- future cleanup auditability.

Cleanup must be controlled, evidence-based, reversible, and separated from feature development.

## 3. Non-Goals

This plan does not authorize:

- deleting files now;
- moving files now;
- renaming files now;
- refactoring code now;
- changing formula behavior;
- changing scoring behavior;
- changing Excel output;
- changing API output;
- changing public-safe adapter fields;
- connecting live backend;
- creating payment / auth / profile / history / PDF / Verify / Admin / Data flows.

## 4. Cleanup Principles

Cleanup principles:

- tests before movement;
- schema lock before output changes;
- adapter contract before public integration;
- no deletion without usage audit;
- no formula change without separate formula task;
- no Excel refactor without regression proof;
- no legacy removal without import / search proof;
- no public UI import of analyzer internals;
- no hidden coupling between repos.

## 5. Cleanup Classification

### A. Safe docs cleanup candidates

Examples:

- docs;
- notes;
- release notes;
- duplicated planning documents;
- unclear old markdown files.

Classification: low-risk only after confirming the document is not a current contract.

### B. Requires usage audit

Examples:

- old scripts;
- old entrypoints;
- legacy UI files;
- duplicate OpenAPI / API docs;
- old staging scaffolds.

Classification: do not delete, move, or rename until imports/usages are checked and owner review is complete.

### C. Requires tests before change

Examples:

- API services;
- Excel paths;
- public-safe adapter paths;
- formula client paths;
- output schema files.

Classification: any change must be preceded by contract tests, schema locks, smoke tests, or regression tests.

### D. Protected / do not touch

Examples:

- formula core;
- formula candidates;
- formula versions;
- engine config;
- validation;
- data models;
- golden dataset;
- regression tests;
- public-safe adapter contracts;
- staging equivalence tests.

Classification: protected from casual cleanup, movement, deletion, or refactor.

## 6. Candidate Areas

| Area | Current classification | Risk level | Why it matters | Safe next step | Required proof before any future change |
|---|---|---:|---|---|---|
| `app.py` | Requires usage audit / legacy-candidate entrypoint | High | Streamlit analyzer entrypoint can be confused with public platform UI | Document current role and search imports/usages | Import/search proof, owner review, CI green |
| `ui_pages/` | Legacy / review candidate | Medium | Prototype UI paths can be mistaken for production UI | Mark as legacy/review in docs | Import/search proof, owner review |
| `api/` | Active API | High | API changes can break clients and service contracts | Keep stable; only change with API task | API contract tests, CI green, response schema review |
| `api/routes/` | Active API | High | Route behavior is external contract surface | Audit route ownership only | API contract tests and endpoint contract proof |
| `api/services/` | Active API/service layer | High | Bridges SDK, export, and API outputs | Keep changes minimal | API contract tests, output schema proof |
| `api_docs/` | Legacy / review candidate if present | Medium | Old OpenAPI files may be mistaken for current source of truth | Identify current vs historical docs | Owner review and current API comparison |
| `kurgin_core/` | Active engine / SDK | High | SDK entrypoint and batch/stone analysis layer | Do not cleanup casually | Core smoke, API tests, regression/equivalence if touched |
| `core_formula/` | Protected formula area if present | High | Formula correctness and scoring risk | No cleanup without formula task | Formula regression, equivalence, owner approval |
| `formula_modules/` | Protected active formula modules | High | Internal calculation behavior | No cleanup without formula task | Formula regression and scoring review |
| `formula_client/` | Active formula client | High | Local/cloud/staging boundary | Maintain contract | Formula client contract tests, local/cloud equivalence |
| `formula_versions/` | Research / protected if present | High | Formula versioning can affect scoring | Document, do not promote | Candidate review, regression proof |
| `formula_candidates/` | Research / protected if present | High | Candidate formulas must not become active by accident | Keep isolated | Owner review, regression proof, explicit promotion task |
| `formula_comparison/` | Active tests / research support | High | Regression comparison protects formula behavior | Keep stable | Regression runner success |
| `golden_dataset/` | Protected regression data | High | Baseline for regression proof | Do not edit casually | Regression justification and CI green |
| `excel_tools.py` | Active Excel / protected overloaded file | High | Batch and export behavior can break silently | Usage audit only | Excel schema/regression tests before refactor |
| `excel_processing/` | Active or review depending on usage | Medium | May hold batch logic | Search current imports | Import proof and Excel tests |
| `excel_output/` | Active export if present | High | Workbook output contract risk | No cleanup without export task | Excel output schema proof |
| `report_templates/` | Active PDF/report templates / protected | High | PDF/report output can break templates | Do not touch in cleanup | PDF/template tests and owner review |
| `deployment/selectel_staging/` | Staging | Medium | Staging can be confused with production | Mark as staging | No-secret review, staging owner review |
| `selectel_formula_service_scaffold/` | Staging scaffold | Medium | Scaffold must not be treated as production service | Keep separated | Staging contract confirmation |
| `platform_integration/` | Public-safe boundary | High | Protects public output from private internals | Keep tests strong | Public-safe adapter contract tests |
| `scripts/` | Active tests / staging / audit scripts | Medium | Scripts may include CI-critical and staging-only paths | Classify by prefix/function | CI references, owner review |
| old docs / release notes / sync manifests | Safe docs candidate or review | Low / Medium | May be outdated but historically useful | Mark status in docs | Owner review before deletion |

## 7. Proposed Cleanup Phases

### Phase 0 — Baseline

Already done:

- structure map exists;
- CI green confirmed externally;
- no repository drift.

### Phase 1 — Documentation alignment

Allowed:

- add docs;
- mark files as active / staging / research / legacy / protected in docs;
- document ownership and risk.

Not allowed:

- moving code;
- deleting code;
- changing behavior.

### Phase 2 — Usage audit

Allowed:

- search imports / usages;
- identify entrypoints;
- identify unused candidates;
- document findings.

Not allowed:

- deleting files;
- moving files;
- refactoring code.

### Phase 3 — Test coverage before cleanup

Allowed:

- propose tests;
- propose contract checks;
- identify missing schema locks.

Not allowed:

- changing behavior unless separately approved.

### Phase 4 — Low-risk cleanup proposal

Allowed:

- propose future PRs;
- list exact files;
- define rollback plan;
- define CI proof required.

Not allowed in this task:

- executing cleanup.

### Phase 5 — Controlled cleanup execution

Future only.

Requires:

- separate approval;
- separate task;
- CI proof;
- rollback plan;
- exact file list;
- owner review.

## 8. Required Proof Before Future Cleanup

Before any future cleanup PR, require:

- CI green before change;
- usage audit result;
- import / search proof;
- contract test coverage;
- schema lock if output changes;
- regression test if Excel / formula-related;
- rollback plan;
- files changed list;
- post-change CI green.

No cleanup should proceed without this proof.

## 9. Risk Register

| Area | Risk | Risk level | Why it matters | Required proof | Safe next step |
|---|---|---:|---|---|---|
| `app.py` | Canonical ambiguity | High | May be mistaken for public platform path | Import/search proof, owner review | Document role before any change |
| `ui_pages/` | Legacy confusion | Medium | Prototype UI can be treated as production | Usage audit | Mark as legacy/review |
| `excel_tools.py` | Overgrowth | High | Central Excel/batch behavior can break | Excel schema/regression tests | Do not refactor yet |
| Formula candidates | Candidate promotion risk | High | Candidate formula can change scoring | Regression and explicit promotion approval | Keep isolated |
| Public-safe boundary | Leakage of private fields | High | Formula internals must not reach public MVP | Public-safe contract tests | Keep adapter tests strict |
| Local/cloud formula paths | Drift | High | Formula Service extraction can diverge | Local-vs-cloud equivalence | Run comparison before promotion |
| API contracts | Contract drift | High | Downstream clients can break | API contract tests | Avoid route/output changes |
| Output schema | Schema drift | High | Excel/API/public output can silently change | Output schema lock | Update schema only with approval |
| Selectel scaffold | Mistaken for production | Medium | Scaffold can be deployed incorrectly | Staging review, no-secret check | Keep clearly labeled staging |
| Docs vs code | Divergence | Medium | Planning docs can imply behavior not implemented | Cross-check with code and CI | Mark planning vs implemented status |

## 10. Explicitly Blocked Actions

Blocked in this task:

- code cleanup;
- file deletion;
- file movement;
- formula refactor;
- Excel refactor;
- API refactor;
- public adapter refactor;
- legacy removal;
- productionization;
- payment / auth / PDF / Verify / Admin / Data work.

This task produces documentation only.

## 11. Acceptance Criteria

The task is accepted only if:

- `ANALYZER_CLEANUP_PLAN.md` is added;
- no code files are modified;
- no files are deleted;
- no files are moved;
- no behavior changes are made;
- no other repos are touched;
- cleanup candidates are classified;
- cleanup phases are documented;
- future proof requirements are documented;
- CI status is reported.

## 12. Final Report Required

After completion, report:

1. Summary
2. Files added
3. Files modified
4. Files deleted
5. Cleanup candidate classifications
6. High-risk areas
7. Whether CI was changed
8. Whether CI was run
9. CI green confirmed / CI green not confirmed
10. Confirmation that no other repos were modified

Expected files changed:

files added:

- `ANALYZER_CLEANUP_PLAN.md`

files modified:

- none

files deleted:

- none
