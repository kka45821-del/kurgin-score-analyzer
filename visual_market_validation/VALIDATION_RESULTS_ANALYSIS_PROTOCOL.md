# KURGIN v1.11.8 Visual Validation Results Analyzer

## Purpose

This stage creates the analyzer that will process a filled visual/market validation workbook.

It does not change official KURGIN Score.

## Input

A filled workbook based on:

```text
kurgin_v1_11_7_visual_market_validation_template.xlsx
```

Required sheet:

```text
Validation Form
```

Optional sheet:

```text
Review Queue
```

## Command

```bash
python scripts/analyze_visual_validation.py \
  --input path/to/filled_validation_workbook.xlsx \
  --output-dir output/visual_validation_results
```

## Output

The analyzer creates:

```text
summary.csv
decision.csv
validation_rows.csv
completion_issues.csv
completeness.csv
visual_validation_results.md
visual_validation_results_manifest.json
```

## Promotion Gate

The analyzer can recommend:

```text
NO DATA
INSUFFICIENT DATA
INSUFFICIENT CAP REVIEW
NEEDS MORE MEDIA
PASS FOR PUBLIC CLASS CAP
REVISE CANDIDATE
MIXED REVIEW
```

It does not promote formula automatically.

## Professional rule

No promotion to official formula unless:

1. enough validation rows are complete;
2. cap-applied cases mostly receive reviewer agreement;
3. high-score controls do not show false concerns;
4. "Needs more data" rows are not excessive.
