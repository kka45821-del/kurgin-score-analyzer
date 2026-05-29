# KURGIN Output Contract Draft v1.12.0

Status: draft, not final production freeze.

## Stable fields for KURGIN Platform

These fields should be treated as stable candidates for platform integration:

```text
Calculation Status
Kurgin Score
Verdict
Verdict Local
score_band
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
Report #
Lab
Shape
Weight
Color
Clarity
Measurements
MinDiameter
MaxDiameter
AvgDiameter
DepthMM
DiameterDiff
RoundnessDeviation
VisualSpreadStatus
DiameterSymmetryStatus
Upload Quality Status
Geometry Status
PDF Report Status
PDF Report File
Engine Version
Formula Output Version
```

## Experimental / preview fields

These can be shown to internal users but must not be used as final public formula contract yet:

```text
AdjustedKURGINScorePreview
AdjustedScoreBandPreview
DiameterSpreadModifierPreview
ScoreClassCapPreview
Diameter Policy Status
Diameter Policy Action
Diameter Policy Reason
High Score Diameter Flag
```

## Non-goals

Do not include formula coefficients or internal commercial scoring weights in public API response.

## Status values

Stable status candidates:

```text
OK
UNSUPPORTED_SHAPE
CATALOG_DATA_ONLY
MISSING_GEOMETRY
POSSIBLE_SCALE_ISSUE
VALIDATION_ERROR
```

## Next freeze gate

Before freezing v1.0 production contract:

1. Run API contract tests.
2. Run regression dataset.
3. Validate JSON response examples.
4. Confirm platform fields needed by KURGIN Tools page.
