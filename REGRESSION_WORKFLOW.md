# KURGIN Regression Workflow

## Goal

Before changing formula logic, run regression comparison.

## Step 1 — Add or update golden dataset

File:

```text
golden_dataset/golden_dataset_template.xlsx
```

Include:

- ideal stones
- premium/high/standard stones
- known weak stones
- hidden weight cases
- diameter/spread edge cases
- dirty data cases
- unsupported shapes

## Step 2 — Run comparison

```bash
python -m formula_comparison.regression_runner \
  --input golden_dataset/golden_dataset_template.xlsx \
  --output output/regression_report.csv \
  --summary output/regression_summary.csv \
  --versions current experimental_v2_candidate
```

## Step 3 — Review

Check:

- score deltas
- class changes
- tag changes
- visual/critical risk changes
- unexpected changes for known stones
- high score + diameter warning cases

## Step 4 — Decide

Only after review:

- reject candidate
- keep preview-only
- update candidate
- promote candidate to current
