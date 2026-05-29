# Candidate v2 Acceptance Criteria

## Candidate objective

Candidate v2 must improve public trust of Elite/Premium/High classes without destabilizing the formula.

## Must pass

- Official current formula remains untouched.
- All changes happen under `formula_versions/experimental/v2_candidate`.
- Regression report must be generated before any promotion.
- Good Spread stones must not be penalized.
- Measurement conflicts must not become direct score penalties.
- Weak stones must not be upgraded due to large diameter.
- Catalog-only and unsupported rows remain non-calculated.

## Quantitative thresholds

| Metric | Pass threshold |
|---|---:|
| Average score delta | -0.75 to 0.00 |
| OK stones changing class | <= 5% |
| Hard fail class change rate | > 10% |
| Good Spread false penalty | 0 allowed |
| Dirty measurement direct penalty | 0 allowed |
| Positive boost from large diameter alone | 0 allowed |

## Review questions

1. Which Elite/Premium stones were capped?
2. Were caps explainable by spread/roundness?
3. Did any good known stone drop unexpectedly?
4. Did the candidate create too many warnings?
5. Are texts/PDF explanations aligned with the new decision?

## Recommended decision path

1. Test class-cap-only candidate.
2. If stable, consider adding tiny numerical modifier later.
3. Do not combine multiple aggressive changes in one candidate.
