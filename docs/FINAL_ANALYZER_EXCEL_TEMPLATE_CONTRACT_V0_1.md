# FINAL ANALYZER EXCEL TEMPLATE CONTRACT v0.1

Repo: `kka45821-del/kurgin-score-analyzer`
Scope: docs-only Analyzer Excel template contract.
Status: canonical input-template contract / no implementation approval.

This document defines the canonical KURGIN Analyzer Excel template contract for future one-stone and batch Analyzer flows.

It does not change code, formula, scoring, Excel export, PDF generation, API behavior, public Streamlit behavior, Admin behavior, `kurgin-data`, Formula Service behavior, payment, auth, storage, history or deployment.

## 1. Purpose

The purpose of this document is to:

- define one canonical Analyzer Excel input template;
- reduce chaotic Excel-format handling;
- prevent arbitrary spreadsheet columns from silently becoming active Analyzer logic;
- separate input columns, public-safe output columns, internal/protected output columns, and admin/processing-only columns;
- prepare future validation and fixtures without changing current behavior;
- create a stable contract for future tests, batch/mass analysis, admin/manual upload alignment, data-structure checks and Formula Service integration planning.

This document is a contract layer only.

```text
contract ≠ parser implementation
contract ≠ public upload
contract ≠ production batch Analyzer
contract ≠ paid Analyzer
contract ≠ Streamlit integration
contract ≠ Excel export behavior change
```

## 2. Current status

Current status:

```text
template contract only
```

This document creates no new behavior.

Explicitly not approved here:

- no code changes;
- no formula/scoring changes;
- no new upload behavior;
- no arbitrary Excel parser;
- no public upload;
- no production batch Analyzer;
- no paid Analyzer;
- no PDF/report generation;
- no result-history storage;
- no Streamlit connection;
- no Admin/data publication behavior change;
- no Formula Service deployment.

## 3. Template rule

### 3.1. Canonical template rule

Only one approved Analyzer Excel template is valid by default.

```text
Analyzer input must use the canonical template.
Arbitrary Excel formats are not supported by default.
```

The canonical template must define expected columns, expected meaning, validation requirements and output handling.

### 3.2. Unknown-column rule

Unknown columns must not silently become active logic.

If a spreadsheet contains unknown columns, future parser behavior should classify them as one of:

- ignored / informational;
- warning-only;
- blocked until contract update;
- mapped only after explicit contract update and tests.

Unknown columns must not:

- change KURGIN Score;
- change formula inputs;
- change validation status;
- generate public output;
- generate PDF/report content;
- publish catalog data;
- affect payment, reserve, sale, price or availability states.

### 3.3. Column-change rule

Column additions, removals, renames or semantic changes require:

1. contract update;
2. fixture/template update;
3. parser/mapping test update;
4. smoke/regression tests;
5. public-safe boundary review if any output may reach a public surface.

No template change is active merely because a new column appears in an Excel file.

## 4. Column groups

## 4.1. A — INPUT REQUIRED

These columns are required for canonical Analyzer processing where the current supported analysis path is available.

| Column | Meaning | Required handling |
|---|---|---|
| `Shape` | Stone shape / cut shape | Required. Unsupported shapes must not call unsupported formula paths. |
| `Weight` / `Carat` | Stone weight in carats | Required as positive numeric value. Use one canonical column name in the final template; alias handling must be explicit if allowed. |
| `Color` | Color grade | Required as stone attribute. Must not dominate core KURGIN Score unless formula contract says so. |
| `Clarity` | Clarity grade | Required as stone attribute. Must not dominate core KURGIN Score unless formula contract says so. |
| `Report #` | Laboratory report / document number | Required for identification and duplicate detection. |
| `Lab` | Laboratory name / issuer | Required. Expected values should be validated by allowed lab policy where available. |
| `Measurements` | Full measurements string | Required if geometry fields are incomplete or if parser uses measurements for diameter/depth checks. |
| `CrownAngle` | Crown angle | Required for Round formula path. |
| `PavilionAngle` | Pavilion angle | Required for Round formula path. |
| `TablePercent` | Table percentage | Required for Round formula path. |
| `DepthPercent` | Depth percentage | Required for Round formula path. |
| `CrownPercent` | Crown height percentage | Required for structure checks. |
| `PavilionPercent` | Pavilion depth percentage | Required for structure checks. |
| `GirdlePercent` | Girdle percentage | Required for structure / spread / risk checks. |

Geometry rule:

```text
Measurements can support geometry parsing, but it must not replace required formula geometry unless the controlled parser explicitly allows that fallback and tests cover it.
```

Supported-shape rule:

```text
Round is the controlled first formula path unless another shape is separately approved, specified and tested.
```

## 4.2. B — INPUT OPTIONAL

Optional input columns may support interpretation, display or validation, but they must not silently alter the formula path unless explicitly specified and tested.

| Column | Meaning | Handling |
|---|---|---|
| `Fluorescence` | Fluorescence intensity | Optional characteristic / warning context. |
| `Cut` | Cut grade | Optional display / validation context. |
| `Polish` | Polish grade | Optional display / validation context. |
| `Symmetry` | Symmetry grade | Optional display / validation context. |
| `Stock #` | Supplier/internal stock identifier | Optional identification field. Must not replace `Report #` as primary lab-document reference. |
| `Notes` | Notes | Optional only if public-safe. Internal notes must not enter public-safe output. |
| `Certificate URL` | Link to document if used internally | Optional and must be validated before public use. |
| `Source` | Source file/source system | Optional processing context. |

Optional-column rule:

```text
Optional input may be stored or reported only within its approved scope.
Optional input must not create public claims, pricing claims, certificate claims or payment/reserve/sold states.
```

## 4.3. C — OUTPUT PUBLIC-SAFE

These are sanitized output columns that may be candidates for public-safe surfaces after adapter review.

| Column | Meaning | Public-safe condition |
|---|---|---|
| `KURGIN Score` | Sanitized score value | Allowed only as quality-analysis support, not financial rating. |
| `score_band` | Score band/class | Must be controlled language. |
| `public_summary` | Short public-safe result summary | Must avoid certificate, appraisal, price and guarantee claims. |
| `warnings` | Public-safe warnings | Must not expose formula internals. |
| `limitations` | Public-safe limitations | Required where data is missing, incomplete or user-provided. |
| `next_action` | Safe next action | Must not create checkout, payment, reserve or order. |
| `validation_status` | Row-level validation status | Must reflect row state and must not silently convert incomplete rows to ok. |
| `shape_supported` | Whether the shape is supported by current public-safe path | Optional public-safe technical status if wording is controlled. |
| `data_completeness` | Public-safe completeness indicator | Must not expose internal scoring internals. |

Public-safe output rule:

```text
Public-safe output is not equal to raw Analyzer output.
Public-safe output must pass through a sanitizer / public-safe adapter before public UI use.
```

## 4.4. D — OUTPUT INTERNAL / PROTECTED

These fields may exist in private Analyzer internals, private Excel exports, staging reports, regression outputs or developer diagnostics.

They must not be exposed in public Streamlit UI, public adapter responses, public catalog cards, public Index, public Verify, or public report previews unless separately sanitized and approved.

Protected/internal examples:

- `formula_internals`;
- `diagnostics`;
- `breakdown`;
- `triple_score`;
- `structure_modifier`;
- `weights`;
- `penalty_details`;
- `penalty_breakdown`;
- `raw_engine_output`;
- `debug_trace`;
- `formula_source`;
- `coefficient_formula`;
- `internal_thresholds`;
- `internal_tags`;
- `engine_trace`;
- `stack_trace`;
- `exception_detail`;
- `raw_formula_result`;
- `commercial_internal_notes`.

Protected-output rule:

```text
Internal/protected output must never be treated as public UI output by default.
```

## 4.5. E — ADMIN / PROCESSING ONLY

These fields support processing, audits, validation, batch control and future operational workflows.

They are not formula inputs unless explicitly mapped.
They are not public claims.
They are not public UI output by default.

| Column | Meaning | Handling |
|---|---|---|
| `row_id` | Row identifier inside a batch | Processing only. |
| `batch_id` | Batch upload/processing identifier | Processing only. |
| `upload_status` | Upload/import status | Processing only. |
| `validation_errors` | Row validation errors | Processing/admin only unless sanitized summary is needed. |
| `processing_status` | Row processing status | Processing/admin only. |
| `mapping_status` | Column mapping status | Processing/admin only. |
| `source_file` | Source file name or reference | Processing/admin only. |
| `processed_at` | Processing timestamp | Processing/admin only. |
| `template_version` | Template version used | Processing/admin only, useful for audit. |
| `contract_version` | Contract version used | Processing/admin only, useful for audit. |

Processing-only rule:

```text
Admin/process columns must not become public labels, badges, CTA, checkout state, reserve state or catalog status without a separate approved contract.
```

## 5. Validation statuses

The canonical template contract allows the following validation statuses.

| Status | Meaning | Allowed behavior |
|---|---|---|
| `ready` | Required inputs valid and supported for the current path | Row may be processed by approved Analyzer path. |
| `incomplete` | Required data missing or insufficient | Row must not silently become ok. Output must include limitations. |
| `invalid_input` | Values are malformed, nonnumeric where numeric is required, impossible or invalid | Row must not be processed as valid. |
| `unsupported_shape` | Shape is outside supported formula path | Must not call unsupported formula path. |
| `duplicate_report` | Duplicate `Report #` in the batch or context | Must be flagged; handling must be explicit. |
| `engine_unavailable` | Engine/service unavailable | Must not fabricate Analyzer result. |
| `processing_error` | Unexpected processing failure | Must be visible in controlled processing output; must not become ok. |

Status integrity rule:

```text
A non-ready row must not silently pass as ready.
```

## 6. Public / private boundary

### 6.1. Excel output is not public UI output

```text
Excel output ≠ public UI output
```

Private Analyzer Excel may contain operational, diagnostic, internal or processing fields.
Public Streamlit must receive only sanitized public-safe output.

### 6.2. Internal diagnostics must not become public UI

Internal Excel diagnostics must not be displayed in:

- public Streamlit MVP;
- public catalog cards;
- public Analyzer preview;
- public Index;
- public Verify skeleton;
- public report previews;
- public API adapter responses.

### 6.3. Analyzer claim boundaries

The following boundaries are locked:

```text
Analyzer ≠ certificate
Analyzer ≠ price valuation
Analyzer ≠ appraisal
Analyzer ≠ investment advice
KURGIN Score ≠ financial rating
KURGIN Score ≠ resale score
KURGIN Score ≠ liquidity score
```

KURGIN Score may be used only as controlled quality-analysis support inside the approved Analyzer context.

## 7. Batch behavior

Batch analysis must follow row-level processing rules.

Required rules:

- batch analysis processes rows independently;
- invalid rows do not silently pass;
- incomplete rows do not become ok;
- unsupported shapes do not call unsupported formula paths;
- duplicate `Report #` rows are flagged;
- engine-unavailable rows do not fabricate results;
- processing errors remain visible in controlled output;
- batch result does not automatically create PDF for every row;
- batch result does not publish catalog data;
- batch result does not create payment, reserve, order, sold, auth/pro role, storage/history or public upload behavior.

Batch-output rule:

```text
Batch output is an Analyzer result artifact, not a catalog publication artifact.
```

## 8. Relationship to existing repository paths

This document relates to the following repository areas:

- `excel_tools.py`;
- `excel_output/`;
- `report_templates/`;
- `formula_comparison/`;
- `golden_dataset/`;
- `platform_integration/public_safe_analyzer_adapter.py`;
- API service contracts;
- Excel export and package-export paths;
- smoke and regression test fixtures.

This document does not change any of those areas.

Interpretation:

```text
existing files remain unchanged;
existing behavior remains unchanged;
future implementation must align to this contract only after a separate approved task.
```

## 9. Blocked actions

The following are blocked by this contract task:

- code changes;
- formula/scoring changes;
- Excel export behavior changes;
- PDF/report generation changes;
- API behavior changes;
- public upload;
- arbitrary Excel acceptance;
- payment;
- auth/pro roles;
- storage/history;
- Streamlit connection;
- Admin behavior changes;
- `kurgin-data` publish;
- production batch Analyzer;
- paid Analyzer;
- Formula Service integration;
- cleanup deletion/move;
- deployment changes.

## 10. Future implementation order

Future implementation must be staged.

Recommended order:

1. Contract — this document.
2. Fixture/template validation.
3. Smoke tests for template headers and required fields.
4. Controlled parser / mapper.
5. Batch validation with row-level statuses.
6. Public-safe export adapter.
7. Regression checks against golden dataset.
8. API contract alignment if needed.
9. Only later UI/integration if separately approved.

Future implementation must not skip directly from contract to public upload, paid Analyzer, PDF generation, Streamlit connection or Formula Service production integration.

## 11. Minimum future template fixture requirements

A future canonical fixture should include:

- one valid Round ready row;
- one incomplete geometry row;
- one invalid numeric row;
- one unsupported shape row;
- one duplicate `Report #` case;
- one no-fluorescence optional-field case;
- one row with unknown columns that must remain inactive.

Fixture requirements are not implemented by this task.

## 12. Acceptance checklist

This document satisfies the template-contract task if:

- only `docs/FINAL_ANALYZER_EXCEL_TEMPLATE_CONTRACT_V0_1.md` is created;
- no code changes are made;
- no formula/scoring changes are made;
- no Excel export changes are made;
- no PDF behavior changes are made;
- no API behavior changes are made;
- no Streamlit/Admin/data changes are made;
- input, optional input, public-safe output, internal/protected output and admin/processing-only columns are separated;
- arbitrary Excel files are explicitly not supported by default;
- public upload, payment, PDF/report generation, storage/history and real integration are blocked.

## 13. Closure

Final status:

```text
CONTRACT DOCUMENTED
NO BEHAVIOR CHANGE
```

The canonical Analyzer Excel template is now defined at the documentation-contract level.

No implementation is approved by this document.
