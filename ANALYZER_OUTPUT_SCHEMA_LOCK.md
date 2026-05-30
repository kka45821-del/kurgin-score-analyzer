# ANALYZER_OUTPUT_SCHEMA_LOCK.md

## Purpose

This document locks the current public/stable Analyzer output shapes before Admin/Public integration and before Selectel production extraction.

This is a schema and planning lock. It does not change formula logic, scoring behavior, Excel output, PDF templates, API behavior, Admin/Public/PWA integration, or Selectel deployment.

## Scope

Locked surfaces:

1. Excel workbook output.
2. API response shapes.
3. Platform card response shape.
4. PDF and batch ZIP package behavior.
5. Stable vs experimental/internal fields.
6. Future Admin import decision boundary.

Non-goals:

- Do not add `KURGIN_Catalog_Import` sheet yet.
- Do not refactor `excel_tools.py`.
- Do not change PDF design.
- Do not move formula to Selectel in this task.
- Do not change formula weights or scoring behavior.

## Excel workbook schema lock

### Sheet names and order

The Analyzer Excel workbook must keep this sheet order:

```text
Results
Details
Issues
System
```

These names are part of the stable Analyzer output contract. New sheets require a separate schema decision.

### Results sheet

Purpose: compact operational output for calculated rows. This sheet may become the future Admin import source, but only after a separate Admin adapter task.

Required stable columns in `Results`:

```text
Stock #
Availability
Report #
Lab
Shape
Weight
Color
Clarity
Cut
Polish
Symmetry
Fluorescence Intensity
Measurements
MinDiameter
MaxDiameter
AvgDiameter
DepthMM
DiameterDiff
RoundnessDeviation
ExpectedDiameter
SpreadDelta %
VisualSpreadStatus
DiameterSymmetryStatus
MeasurementConsistencyStatus
DiameterSpreadModifierPreview
ScoreClassCapPreview
AdjustedKURGINScorePreview
AdjustedScoreBandPreview
Diameter Policy Status
Diameter Policy Action
Diameter Policy Reason
High Score Diameter Flag
TablePercent
DepthPercent
CrownAngle
PavilionAngle
CrownPercent
PavilionPercent
GirdlePercent
Kurgin Score
Verdict Local
score_band_label_ru
tags_all
tag1
tag2
tag3
tag4
tag5
tag6
interpretation_short_ru
recommendation_ru
warning_ru
Data Completeness %
Report Quality Status
platform_import_status
recommended_pdf_priority
PDF Report Status
PDF Report File
PDF Generation Mode
Upload Quality Status
Geometry Status
Missing Geometry Fields
Possible Scale Issues
Column Recognition Status
Calculation Status
```

Stable for future Admin import reference:

```text
KURGIN Import ID
Stock #
Availability
Report #
Lab
Shape
Weight
Color
Clarity
Measurements
Kurgin Score
Verdict Local
score_band_label_ru
tags_all
tag1-tag6
interpretation_short_ru
recommendation_ru
warning_ru
Data Completeness %
Report Quality Status
platform_import_status
recommended_pdf_priority
PDF Report Status
PDF Report File
PDF Generation Mode
Calculation Status
Validation Errors
Formula Output Version
Engine Version
```

Important note: some Admin import reference fields currently live in `Details`/`System`, not always in `Results`. A future Admin adapter may compose its import payload from `Results`, `Details`, and `System`, but must not add a new workbook sheet without a separate task.

### Experimental / research / preview columns

The following fields are not final public/Admin business contracts yet:

```text
DiameterSpreadModifierPreview
ScoreClassCapPreview
AdjustedKURGINScorePreview
AdjustedScoreBandPreview
Diameter Policy Status
Diameter Policy Action
Diameter Policy Reason
High Score Diameter Flag
spread_score
spread_status
diameter_symmetry_score
diameter_symmetry_status
roundness_status
commercial_view
value_score
```

They may be useful for research, visual review, future policy modules, or Admin QA, but they should not be treated as final public scoring behavior.

### Details sheet

Purpose: expanded calculated-row details, report metadata, certificate fields, geometry, formula output, public text, and technical support fields.

Important columns in `Details`:

```text
KURGIN Import ID
Stone Title
Identification Line
Stock #
Availability
Location
Country
State
City
Report #
Lab
Shape
Weight
Color
Clarity
Cut
Polish
Symmetry
Hearts & Arrows
Fluorescence
Fluorescence Intensity
Fluorescence Color
Measurements
Length
Width
Height
Ratio
Treatment
Growth Method
Diamond Type
Origin Type
Luster
Category
Inscription
Cert comment
Member Comment
CertFile
Report Issue Date
Report Type
Is Matched Pair Separable
Country of Polishing
Shade
Milky
Eye Clean
BGM
KeyToSymbols
White Inclusion
Black Inclusion
Open Inclusion
DepthPercent
TablePercent
CrownPercent
CrownAngle
PavilionPercent
PavilionAngle
GirdlePercent
GirdleThin
GirdleThick
GirdleCondition
CuletSize
CuletCondition
MinDiameter
MaxDiameter
AvgDiameter
DepthMM
DiameterDiff
RoundnessDeviation
ExpectedDiameter
SpreadDelta %
VisualSpreadStatus
DiameterSymmetryStatus
MeasurementConsistencyStatus
Kurgin Score
Verdict
Verdict Local
score_band
score_band_label_ru
Triple Score
Structure Modifier
Visual Check
Critical Risk
Nailhead
Fisheye
Fire Loss
Depth Dev
Crown Dev
Pavilion Dev
Balance Err
Girdle Penalty
Tags
Tags Local
tags_all
tag1-tag6
tag_light
tag_structure
tag_spread
tag_risk
tag_certificate
tag_commercial
certificate_flags
interpretation_short_ru
interpretation_detail_ru
recommendation_ru
warning_ru
disclaimer_ru
KURGIN Report ID
PDF Report Status
PDF Report File
PDF Report URL
PDF Generation Mode
platform_import_status
recommended_pdf_priority
Report Template Version
Formula Output Version
Engine Version
Upload Quality Status
Geometry Status
Missing Geometry Fields
Possible Scale Issues
Column Recognition Status
Calculation Status
Validation Errors
Breakdown
```

`Details` may include internal or semi-internal fields. It is not automatically public-safe.

### Issues sheet

Purpose: all unsupported, validation, missing-geometry, measurement, scale and review issues separated from `Results`.

Required columns in `Issues`:

```text
Issue Type
Stock #
Report #
Lab
Shape
Weight
Color
Clarity
Calculation Status
Problem
Validation Errors
Missing Fields
Measurement Parse Status
Measurement Source
Measurement Warning
Measurement Conflict
Chosen Measurement Source
Upload Quality Status
Geometry Status
Missing Geometry Fields
Possible Scale Issues
Data Completeness %
Report Quality Status
platform_import_status
Diameter Policy Status
Diameter Policy Action
Diameter Policy Reason
High Score Diameter Flag
recommendation_ru
PDF Report Status
```

Rows expected in `Issues`:

- unsupported shape rows;
- catalog-only rows;
- missing geometry rows;
- possible scale issue rows;
- validation error rows;
- measurement parsing issue rows;
- high-score diameter review rows.

### System sheet

Purpose: compact audit/version/support sheet.

Required columns:

```text
Section
Field
Value
Detail
```

Required System/version/audit fields:

```text
Engine Version
Report Template Version
Formula Output Version
Formula Mode
Supported Shapes
```

Expected System sections include:

```text
Summary
Versions
Issues
Upload Recognition
Column Mapping
Data Dictionary
```

`System` must not expose secrets such as `FORMULA_API_KEY`, production private endpoints, stack traces, or private deployment metadata.

## API output schema lock

### GET /v1/health

Required shape:

```json
{
  "status": "ok",
  "version": {
    "core_sdk_version": "...",
    "engine_version": "...",
    "formula_mode": "local|cloud|cloud_fallback",
    "default_report_level": "...",
    "api_version": "...",
    "service_name": "...",
    "environment": "..."
  }
}
```

### GET /v1/ready

Required shape:

```json
{
  "status": "ready|not_ready",
  "calculation_status": "OK|...",
  "version": { }
}
```

`/v1/ready` must run a minimal one-stone analysis and should be used for deployment readiness checks.

### POST /v1/analyze/stone

Current shape:

```json
{
  "status": "OK|...",
  "result": { },
  "version": { }
}
```

This endpoint currently returns a rich Analyzer result. Treat it as service/internal or authenticated API output, not necessarily as public-safe browser output.

Required stable result fields:

```text
Calculation Status
Kurgin Score
Verdict
Verdict Local
score_band_label_ru
tags_all
tag1
tag2
tag3
tag4
tag5
tag6
interpretation_short_ru
recommendation_ru
warning_ru
```

### POST /v1/analyze/batch/json

Current shape:

```json
{
  "status": "OK",
  "rows_total": 1,
  "rows_ok": 1,
  "rows_issues": 0,
  "records": [ ],
  "version": { }
}
```

If `include_records=false`, `records` may be `null`.

### POST /v1/platform/stone-card

This is the preferred public-safe shape for Platform/Public card integration.

Required shape:

```json
{
  "status": "OK|...",
  "card": {
    "kind": "kurgin_score_result_card",
    "schema_version": "...",
    "status": "OK|...",
    "identity": { },
    "stone": { },
    "score": { },
    "tags": [ ],
    "summary": { },
    "measurements": { },
    "quality": { },
    "report": { },
    "version": { },
    "actions": { }
  },
  "version": { }
}
```

Public platform cards must not expose raw formula internals by default.

### POST /v1/export/stone/pdf

Required behavior:

- returns `application/pdf`;
- response body must be non-empty PDF bytes;
- default filename header is currently `kurgin_stone_report.pdf`;
- PDF content is based on already analyzed stone result.

## PDF and package schema lock

### One-stone PDF

Current generator:

```text
create_single_stone_pdf(row, language="MULTI")
```

PDF report should contain:

- KURGIN report title/branding;
- identity fields;
- KURGIN Score;
- verdict/class;
- public interpretation;
- recommendation;
- certificate and geometry table;
- risk/public warning information;
- disclaimer.

PDF design must not be changed in this task.

### PDF filename convention

For batch package rows:

```text
reports/{report_id}_KURGIN_Report.pdf
```

`report_id` priority:

1. `Report #`
2. `Stock #`
3. `row_{index+1}`
4. `manual`

For API one-stone PDF endpoint:

```text
kurgin_stone_report.pdf
```

### Batch ZIP package

Current ZIP structure:

```text
kurgin_score_result.xlsx
reports/{report_id}_KURGIN_Report.pdf
```

PDF generation modes:

```text
all_ok   -> PDF for all rows with Calculation Status == OK
top_only -> PDF for high-score rows, excluding critical-risk rows
none     -> Excel only inside package
```

Unsupported, catalog-only, missing-geometry, scale issue and validation-warning rows should not receive generated PDFs by default.

### Version fields

Version fields must remain available for audit/reproducibility:

```text
Engine Version
Report Template Version
Formula Output Version
Formula Mode
```

## Stable vs internal/public-safe decision lock

### Public-safe fields

Public-safe fields may include:

```text
Kurgin Score
Verdict Local
score_band_label_ru
tags_all
tag1-tag6
interpretation_short_ru
recommendation_ru
warning_ru
Calculation Status
PDF Report Status
PDF Report File
Report Quality Status
Data Completeness %
Engine Version
Formula Output Version
Report #
Lab
Stock #
Shape
Weight
Color
Clarity
Measurements
AvgDiameter
VisualSpreadStatus
DiameterSymmetryStatus
```

### Internal-only by default

The following are internal-only by default and should not be returned by public responses unless a separate authenticated internal/Admin/professional mode is approved:

```text
Breakdown
raw diagnostics
Triple Score
Structure Modifier
Nailhead
Fisheye
Fire Loss
Depth Dev
Crown Dev
Pavilion Dev
Balance Err
Girdle Penalty
formula weights
thresholds
penalties
cap logic
candidate formula internals
regression comparison output
```

### Candidate / preview fields

Candidate and preview fields are not final public contracts:

```text
AdjustedKURGINScorePreview
AdjustedScoreBandPreview
DiameterSpreadModifierPreview
ScoreClassCapPreview
Diameter Policy Status
Diameter Policy Action
Diameter Policy Reason
High Score Diameter Flag
candidate_* fields
```

They may be shown in controlled review or internal Admin QA, but should not be treated as public score behavior.

## Admin import decision

`Results` can become the future Admin import source, but not automatically.

Decision:

- `Results` is the preferred base for future Admin import.
- A separate Admin adapter task must decide the final Admin import payload.
- Do not add `KURGIN_Catalog_Import` sheet yet.
- Do not change current workbook sheets yet.
- Future Admin import may combine fields from `Results`, `Details`, and `System` if needed, but should output a stable Admin-specific adapter contract separately.

## Snapshot test policy

The schema snapshot test should verify the current output contract without changing output.

It should check:

- Excel sheet names and order;
- key columns in `Results`;
- key columns in `Details`;
- key columns in `Issues`;
- key fields in `System`;
- key API response shapes;
- platform card public-safe shape;
- PDF response content type and non-empty body.

The test should not assert exact numeric formula values beyond minimal sanity checks unless a separate golden-score test is intended.

## Change policy

Any future change to these outputs must be classified as one of:

1. Non-breaking additive field.
2. Non-breaking documentation clarification.
3. Breaking schema change.
4. Internal-only change.
5. Experimental field change.

Breaking schema changes require a separate issue and migration note.
