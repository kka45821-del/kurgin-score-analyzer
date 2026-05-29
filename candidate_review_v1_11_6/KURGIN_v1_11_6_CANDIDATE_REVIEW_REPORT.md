# KURGIN v1.11.6 Candidate Review Report

Date: 2026-05-29T01:42:50Z  
Candidate: experimental_v2_candidate  
Mode: class_cap_only  
Official current formula changed: No

---

## 1. Executive conclusion

PASS FOR REVIEW. Keep as experimental; recommended next step is more real visual validation before promotion.

The candidate is intentionally conservative. On the real golden dataset it changed only a very small number of stones.

---

## 2. Regression summary

| Dataset   |   Rows |   OK Rows |   Avg Delta |   Min Delta |   Max Delta |   Band Changes |   Cap Applied |   Verdict Changes |
|:----------|-------:|----------:|------------:|------------:|------------:|---------------:|--------------:|------------------:|
| real      |    114 |        94 |       -0.01 |       -0.94 |           0 |              1 |             1 |                 1 |
| synthetic |     10 |         7 |        0    |        0    |           0 |              0 |             0 |                 0 |

---

## 3. Acceptance checks

| Check                               | Result   | Value   | Threshold           | Notes                                                  |
|:------------------------------------|:---------|:--------|:--------------------|:-------------------------------------------------------|
| Average score delta stable          | PASS     | -0.01   | -0.75 to 0.00       | Candidate should be conservative                       |
| Class change rate acceptable        | PASS     | 1.06%   | <= 5%               | Only explainable caps should change class              |
| Hard fail class change rate avoided | PASS     | 1.06%   | <= 10%              | Hard fail if above 10%                                 |
| Candidate is not aggressive         | PASS     | 1       | <= max(1, 2% of OK) | First class-cap candidate should catch rare cases only |
| Synthetic unchanged                 | PASS     | 0       | 0 class changes     | Synthetic cases remain stable in first candidate       |

---

## 4. Cap-applied cases

- Dataset `real`, Report `LG780619291`, Stock `VDC-49-14`: 95.93 → 94.99; reason: Out-of-round Risk


---

## 5. Professional interpretation

The candidate did what it was supposed to do:

- it did not rewrite the formula;
- it did not add positive bonuses for large diameter;
- it did not broadly penalize the dataset;
- it only applied a cap where diameter/spread policy gave a reason.

This supports the current strategy:

```text
Keep Base KURGIN Score as optics/geometry/structure.
Use diameter/spread first as class review and cap logic.
Do not introduce aggressive numerical modifier yet.
```

---

## 6. Decision recommendation

Recommended next step:

```text
v1.11.7 Visual/Market Validation Set
```

Before promoting v2 candidate to official behavior, add manual/visual validation examples:

- photos/videos where available;
- known preferred stones;
- known rejected stones;
- high score + spread review cases;
- marketable but not optically strong cases.

If visual validation confirms the cap logic, then consider:

```text
Option C: apply public class cap only
```

Do not yet apply numerical modifier to official KURGIN Score.
