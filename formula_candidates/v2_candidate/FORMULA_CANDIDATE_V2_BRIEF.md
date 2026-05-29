# KURGIN Formula Candidate v2 — Design Brief

Version: v1.11.4  
Status: design only, no official formula change  
Base version: v1.11.3 Real Golden Dataset + Baseline Report

---

## 1. Purpose

The goal of Candidate v2 is not to redesign KURGIN Score from scratch.

The goal is to test whether the official score/class should be protected from visually or commercially inconsistent cases, especially:

- high score + small face-up diameter;
- high score + out-of-round diameter;
- high score + measurement conflict;
- wide but risky diameter;
- hidden weight that is not obvious enough in the current result.

The candidate must preserve the core identity of KURGIN Score:

```text
Base KURGIN Score = optics / geometry / structure
Diameter module = market/visual consistency check
```

---

## 2. Baseline facts from v1.11.3

Processed real supplier files:

```text
Total rows: 2569
OK rows: 2282
Issue rows: 287
Real golden cases selected: 114
Diameter/spread review cases: 121
High score + diameter review cases: 39
Average OK score: 86.748
```

Important observation:

The current formula is not obviously broken. Most strong stones already have acceptable spread. Therefore Candidate v2 must be conservative.

---

## 3. Non-negotiable principles

### 3.1 Do not let diameter create high score

Bad approach:

```text
larger diameter = higher KURGIN Score
```

Correct approach:

```text
good diameter allows high class
bad diameter can restrict high class
```

### 3.2 Do not punish dirty data as a stone defect

If measurement data is missing, conflicting or inconsistent, the formula must not directly penalize the stone.

It should produce:

```text
Measurement warning
Data quality warning
Issues entry
```

### 3.3 Avoid double penalty

The current formula already accounts for:

```text
Depth %
Crown %
Pavilion %
Girdle %
Structure Modifier
Hidden Weight tags
```

Small diameter can be caused by the same structural problems. Candidate v2 must avoid punishing the same problem twice.

### 3.4 Color, clarity and price remain outside core score

Do not include:

```text
Color
Clarity
Price
Lab
Fluorescence
Milky
Eye Clean
```

in the official core KURGIN Score.

These can be shown as certificate/commercial context only.

---

## 4. Candidate v2 scope

Candidate v2 may test:

1. Diameter/spread public class cap.
2. Light numerical modifier preview.
3. Roundness review logic.
4. Measurement consistency guard.
5. High-score diameter review logic.
6. Improved hidden weight signaling.

Candidate v2 must not modify:

1. Supplier upload recognition.
2. PDF layout logic.
3. Score band labels.
4. Core output field names.
5. Non-round shape models.

---

## 5. Proposed architecture

Candidate v2 should preserve two outputs:

```text
Base KURGIN Score
Adjusted KURGIN Score Preview
```

And add one public-facing class decision:

```text
Public Score Class Preview
```

Recommended structure:

```text
official_score = current_formula_score
diameter_policy = measurement_spread_policy(row)
adjusted_preview = official_score + conservative_modifier
public_class_preview = min(score_band(adjusted_preview), class_cap)
```

No official replacement until regression review passes.

---

## 6. Diameter / Spread rules

### 6.1 Expected diameter

For Round Brilliant:

```text
ExpectedDiameter = 6.45 × carat^(1/3)
```

This base is intentionally more practical than 6.50.

Reason:

- 6.50 is historically/market meaningful.
- But real supplier data showed 6.50 as too strict for automatic penalty.
- 6.45 is more stable for practical analysis.

### 6.2 SpreadDelta

```text
SpreadDelta % = (AvgDiameter - ExpectedDiameter) / ExpectedDiameter × 100
```

### 6.3 Visual Spread Status

| SpreadDelta | Status |
|---:|---|
| < -3.0% | Hidden Weight Risk |
| -3.0% to -1.5% | Small for Weight |
| -1.5% to +1.5% | Good Spread |
| +1.5% to +3.0% | Wide Spread |
| > +3.0% | Wide but Risky |

Additional rule:

```text
If SpreadDelta > +1.5% and DepthPercent < 59.0 → Wide but Risky
```

### 6.4 Diameter Symmetry

| RoundnessDeviation | Status |
|---:|---|
| <= 0.50% | Excellent Roundness |
| <= 1.00% | Good Roundness |
| <= 1.50% | Roundness Check |
| > 1.50% | Out-of-round Risk |

### 6.5 Measurement Consistency

Calculate:

```text
DepthFromMeasurements% = DepthMM / AvgDiameter × 100
MeasurementConsistencyDelta = DepthFromMeasurements% - DepthPercent
```

Status:

| Absolute delta | Status |
|---:|---|
| <= 0.30 | OK |
| <= 0.70 | Check |
| > 0.70 | Warning |

If status is Warning, do not apply score penalty. Treat as data warning.

---

## 7. Recommended Candidate v2 behavior

### 7.1 Public class cap

Candidate v2 should test class caps before heavy numerical penalty.

| Situation | Cap |
|---|---|
| Elite score + Small for Weight | Premium |
| Elite score + Hidden Weight Risk | High or Standard |
| Premium score + Hidden Weight Risk | High |
| High score + Hidden Weight Risk | Standard |
| Any high class + Out-of-round Risk | High |
| Any high class + Measurement Conflict | Review only, no cap unless conflict source chosen is unreliable |
| Wide but Risky | High |
| Measurement Consistency Warning | Review only |

### 7.2 Numerical modifier preview

Keep modifier conservative.

| Situation | Modifier preview |
|---|---:|
| Good Spread | 0 |
| Wide Spread with safe geometry | 0 |
| Small for Weight | -0.5 to -1.5 |
| Hidden Weight Risk | -2.0 to -3.0 |
| Wide but Risky | -1.0 to -2.5 |
| Roundness Check | -0.5 to -1.0 |
| Out-of-round Risk | -1.0 to -2.0 |
| Measurement inconsistency | 0, warning only |

Hard bounds:

```text
max positive modifier: +0.0 or +0.3
max negative modifier: -4.0
```

Recommendation:

```text
Candidate v2 should start with +0.0 maximum.
```

Good diameter should not raise score. It should only support the existing class.

---

## 8. Acceptance criteria

Candidate v2 may be accepted only if it passes these tests.

### 8.1 Stability

On real baseline dataset:

```text
Average score delta must be between -0.75 and 0.00
Class changes should be below 5% of OK stones
Elite/Premium class changes must be explainable by spread/roundness/measurement policy
```

### 8.2 Protection

Candidate should catch:

```text
High score + Hidden Weight Risk
High score + Out-of-round Risk
High score + Wide but Risky
```

### 8.3 No false aggression

Candidate must not:

```text
downgrade Good Spread stones without reason
penalize measurement conflicts as stone defects
raise weak stones because they have large diameter
change Catalog Data Only / Unsupported / Missing Geometry logic
```

### 8.4 Golden dataset

On golden cases:

```text
Ideal baseline must remain Elite/Premium
Catalog-only must remain non-calculated
Unsupported shape must remain unsupported
Scale issue must remain possible scale issue
Small spread check must show cap/review behavior
Out-of-round case must show review behavior
```

---

## 9. Failure criteria

Reject Candidate v2 if:

```text
More than 10% of OK stones change class
Premium stones drop to Standard too often
Good Spread stones receive penalties
Wide shallow stones receive positive boost
Dirty measurement rows affect official score
Average score drops more than 1.0
High quality known cases become unstable
```

---

## 10. Implementation plan for v1.11.5

1. Copy current experimental runner.
2. Add Candidate v2 policy wrapper.
3. Do not touch current formula.
4. Add config file for v2 rules.
5. Produce both:
   - current_score
   - v2_candidate_score
   - v2_candidate_class
   - v2_candidate_reason
6. Run regression on:
   - golden synthetic dataset;
   - real golden dataset;
   - supplier baseline.
7. Generate comparison report.

---

## 11. Decision rule

Candidate v2 is not automatically official.

After regression:

```text
Option A: reject v2
Option B: keep diameter as preview only
Option C: apply public class cap only
Option D: apply class cap + light modifier
Option E: promote v2 to current
```

The safest likely path is:

```text
Option C first: public class cap only
```

Then test numerical modifier later.

---

## 12. Current recommendation

Do not change official KURGIN Score yet.

Next step:

```text
v1.11.5 Experimental Candidate v2 — Class Cap Only
```

Reason:

- It is safer than changing numeric score.
- It addresses market/visual inconsistency.
- It avoids double penalty.
- It protects Elite/Premium public trust.
