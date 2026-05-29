# Candidate v2 Implementation Status

Version: v1.11.5  
Status: implemented for regression only  
Official formula changed: No

## Implemented

- Experimental formula runner:
  `formula_versions/experimental/v2_candidate/runner.py`

- Candidate mode:
  `class_cap_only`

- Regression runner now supports:
  `calculate_with_row(row, engine_kwargs)`

## Behavior

Candidate v2:

1. Runs current formula.
2. Reads measurement/spread fields from row.
3. Applies class cap only when reliable diameter/spread data challenges high public class.
4. Preserves base score in `candidate_base_score`.
5. Returns public capped score as experimental candidate score for regression visibility.

## Important

This is still not official KURGIN Score.

Do not promote without reviewing:
- synthetic golden regression
- real golden regression
- supplier baseline regression
- high score diameter cap cases
- false cap cases
