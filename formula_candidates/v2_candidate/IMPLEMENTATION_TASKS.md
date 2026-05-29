# v1.11.5 Implementation Tasks — Experimental Candidate v2

## Scope

Implement class-cap-only experimental candidate.

## Files to touch

```text
formula_versions/experimental/v2_candidate/runner.py
formula_versions/experimental/v2_candidate/metadata.json
formula_versions/experimental/v2_candidate/v2_rules.json
formula_comparison/regression_runner.py only if output fields need extension
```

## Implementation steps

1. Load current formula result.
2. Calculate measurement/spread metrics from input row or reconstructed fields.
3. Determine base score band.
4. Apply class cap policy.
5. Return:
   - base score
   - candidate score
   - candidate public class
   - cap reason
   - candidate status.
6. Keep current formula unchanged.
7. Run regression:
   - synthetic golden dataset
   - real golden dataset
   - supplier baseline.
8. Generate decision log.

## Do not implement yet

- No price logic.
- No color/clarity score logic.
- No fancy shape scoring.
- No aggressive numeric modifier.
