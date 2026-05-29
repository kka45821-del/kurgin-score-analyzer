# KURGIN Formula Versioning Guide

## Purpose

Formula changes must be measurable, reversible and comparable.

## Version groups

```text
formula_versions/current       baseline official formula
formula_versions/legacy        old formulas from previous experiments
formula_versions/experimental  candidate formulas
```

## Runner interface

Every version must implement:

```python
def calculate(engine_kwargs: dict) -> dict:
    ...
```

Optional:

```python
def get_metadata() -> dict:
    ...
```

## Do not replace current formula directly

Professional route:

1. add candidate under `formula_versions/experimental/`
2. run regression comparison
3. inspect class changes, score deltas, tag/risk changes
4. approve or reject candidate
5. only then promote candidate to current

## Key comparison questions

- How many stones changed score by > 1.0?
- How many changed KURGIN band?
- Did Elite/Premium become more realistic?
- Did weak stones become over-rewarded?
- Did diameter/spread module create false penalties?
- Are changes explainable in PDF/Excel?
