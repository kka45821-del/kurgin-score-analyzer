# SELECTEL_PRIVATE_BOUNDARY.md

## Purpose

This document defines the boundary between the future private Selectel Formula Service and the public/client Analyzer repository.

This is a planning document only. It does not move files, delete modules, change formula logic, change scoring behavior, change Excel/PDF outputs, change API behavior, or deploy Selectel.

## Current state

The Analyzer currently supports three formula execution modes through `formula_client/engine_client.py`:

- `local` — run the formula inside the current repository/process.
- `cloud` — call a private formula API.
- `cloud_fallback` — try cloud first, then fall back to local if cloud fails.

The current repository still contains formula implementation files. Before a production public/client deployment, commercial formula internals must be removed from the public/client repo and kept only in a private service.

## Private Selectel Formula Service

The private Selectel service should contain all commercial formula logic, tuning material, candidate logic, regression material, and any source files that allow reconstruction of formula behavior.

### Must be private

The following files and directories should move to the private Selectel Formula Service when extraction is implemented:

```text
core_formula/
config_settings/engine_config.py
formula_modules/
formula_versions/
formula_candidates/
formula_comparison/
golden_dataset/
formula_client/local_client.py
```

Also private:

- regression datasets;
- baseline reports used for formula comparison;
- candidate formula rules;
- candidate review artifacts;
- formula promotion gates;
- visual/market validation datasets if they reveal score behavior or thresholds;
- any file containing weights, thresholds, penalties, caps, score bands, or internal scoring decisions;
- any local-only runner that can reproduce commercial formula output without the private API.

### Private service responsibilities

The private Selectel Formula Service is responsible for:

- executing official KURGIN Score calculations;
- owning formula coefficients, thresholds, penalties and candidate formula logic;
- validating canonical formula input;
- returning a stable formula result contract;
- exposing version metadata for reproducibility;
- rejecting malformed input safely;
- enforcing authentication for all non-health endpoints;
- logging operational failures without exposing formula internals to public clients.

## Public/client Analyzer repository

The public/client repo may keep only public-safe client, UI, adapter, and export logic.

### May remain public/client-side

The following may remain in the public/client repo after formula extraction, provided they do not contain commercial formula internals:

```text
formula_client/cloud_client.py
formula_client/engine_client.py
kurgin_core/ public-safe SDK wrappers
api/ client-safe API wrappers or proxy adapters
platform_integration/
Streamlit/service UI files
public-safe PDF/Excel export logic
report_templates/ if templates do not reveal scoring internals
excel_processing/ if it only maps/enriches public supplier data
validation/ if it validates input format only and does not encode formula logic
```

### Public/client responsibilities

The public/client repo is responsible for:

- collecting user or supplier input;
- normalizing public/certificate fields;
- calling the private Formula API;
- rendering public-safe results;
- generating public-safe Excel/PDF reports when allowed;
- building public/platform cards from filtered result fields;
- handling user-facing error states without leaking private formula details.

## Boundary rules

### Public clients must not receive

Public UI, public API responses, platform cards, and client-side bundles must not expose:

- formula weights;
- thresholds;
- penalties;
- cap rules;
- internal candidate formula rules;
- regression rows or golden datasets;
- raw candidate comparison output;
- internal formula source code;
- private formula diagnostics that allow reverse engineering;
- stack traces from private formula execution;
- private API keys, service URLs, deployment metadata, or secrets.

### KURGIN Score public response

A public-safe KURGIN Score response may contain:

- `Kurgin Score` or `final_score`;
- public class/verdict label;
- public-safe tags;
- public-safe warnings;
- public-safe recommendation text;
- calculation status;
- formula/output version identifiers;
- report/PDF availability status.

The public response should not explain the exact formula math. It should explain the result in commercial/user-facing language without exposing coefficients or thresholds.

### `breakdown` policy

`breakdown` should be treated as internal by default.

Current local formula output may include `breakdown` for development and professional debugging, but after Selectel extraction:

- public production responses should not return raw `breakdown`;
- public UI should use a public-safe explanation field instead;
- Admin/professional internal tools may request a controlled diagnostic explanation only if access is authenticated and logged;
- if `breakdown` remains available in staging, it must be explicitly marked non-public.

### `diagnostics` policy

Raw `diagnostics` should be treated as internal by default because it can reveal formula behavior.

Allowed production alternatives:

- boolean/public flags such as `visual_check`, `critical_risk`, `needs_review`;
- public-safe status labels such as `review_required`, `geometry_warning`, `unsupported_shape`;
- controlled public warning text without numeric internal loss values.

If diagnostics are needed for Admin/professional workflows, expose them only through authenticated internal endpoints, not public/client responses.

### `structure_tags` policy

`structure_tags` may be public only after filtering and translation.

Allowed:

- public-safe tags such as `Perfect Build`, `Hidden Weight`, `Visual Check`, or localized equivalents when they are approved for buyer/professional display.

Not allowed:

- tags that reveal internal thresholds, candidate formula behavior, exact penalties, or scoring caps.

### Public-safe field filtering

Public/client adapters should maintain an allowlist of public-safe fields. The allowlist should be reviewed before production and should exclude raw formula internals by default.

Recommended public-safe groups:

- identity fields: report number, lab, stock number, shape, weight, color, clarity;
- score fields: score, public class, public verdict;
- public tags and warning labels;
- public summary/recommendation text;
- report metadata: PDF availability, output version, engine version;
- status fields: calculation status, unsupported shape, needs review.

## Execution mode policy

### Development

Development may use:

```text
FORMULA_MODE=local
```

Development may also use:

```text
FORMULA_MODE=cloud_fallback
```

when testing the cloud boundary. Local mode is acceptable in development because the repository still contains formula files during the transition period.

### Staging

Selectel staging should prefer:

```text
FORMULA_MODE=cloud_fallback
```

only while validating endpoint stability, timeouts, deployment health and result equivalence.

Staging must log fallback reason before it is considered production-ready. If fallback happens frequently, staging is not ready.

### Production

Production public/client deployments should use:

```text
FORMULA_MODE=cloud
```

Production should fail closed if the private Formula API is unavailable, unless a separate explicit business/security decision allows fallback.

Production public/client repos should not contain commercial formula code. If a production build contains `core_formula/`, `engine_config.py`, formula candidates, golden datasets or local formula runners, the boundary is not complete.

## Secrets handling

### `FORMULA_API_URL`

`FORMULA_API_URL` must be stored in server-side environment variables or deployment secrets.

Allowed:

- private backend env vars;
- Selectel secret/config storage;
- server-side CI/CD deployment variables.

Not allowed:

- browser code;
- public static bundles;
- committed `.env` files;
- Streamlit UI text;
- public documentation containing production endpoints.

### `FORMULA_API_KEY`

`FORMULA_API_KEY` must be treated as a secret credential.

Allowed:

- server-side env vars;
- secret manager;
- deployment secrets;
- rotated staging/production keys.

Not allowed:

- committed files;
- frontend code;
- public issue comments;
- logs;
- PDF/Excel/System sheets;
- public API responses.

### Logging rule

Logs may include:

- request id;
- status code;
- timeout/failure category;
- formula service version;
- sanitized input id such as report number or internal request id.

Logs must not include:

- API keys;
- full formula internals;
- private coefficients;
- private diagnostic math;
- raw stack traces returned to public clients.

## Formula API response contract

The private Formula API may internally return the full formula result, but public adapters should filter it.

### Internal formula response may contain

```text
engine_version
final_score
final_verdict
triple_score
structure_modifier
structure_tags
visual_check
critical_risk
diagnostics
breakdown
```

### Public/client response should normally contain

```text
score
class/verdict
public-safe tags
public-safe warning/recommendation
calculation_status
needs_review
engine_version or output_version
```

`triple_score`, `structure_modifier`, raw `diagnostics`, and raw `breakdown` are internal unless explicitly approved for authenticated professional/Admin surfaces.

## Excel and PDF boundary

Excel/PDF export logic may remain public-safe if it uses already-filtered public fields and does not reveal formula internals.

Before production:

- `Results` may be used as a public/admin import base only after field allowlist freeze;
- `Details` must be reviewed for internal diagnostic leakage;
- `System` must not expose secrets or private endpoints;
- PDF templates must use public-safe explanations, not raw formula breakdown;
- package filenames may remain public-safe if based on report number, stock number, or generated ids.

## Migration sequence

Recommended order before production extraction:

1. Keep current repo stable and green.
2. Freeze this private/public boundary document.
3. Add response filtering tests for public/client adapters.
4. Add cloud schema validation for formula responses.
5. Add cloud timeout and fail-closed tests.
6. Deploy private Selectel staging service with formula code.
7. Run local vs cloud equivalence tests on golden dataset.
8. Switch staging to `cloud_fallback` and monitor fallback events.
9. Remove commercial formula files from public/client repo in a separate approved task.
10. Switch production public/client deployment to `FORMULA_MODE=cloud`.
11. Verify no private formula files or secrets exist in public/client build artifacts.

## Acceptance criteria for boundary completion

The boundary is complete only when:

- private formula source files exist only in private Selectel service;
- public/client repo has no commercial formula coefficients or candidate logic;
- public/client repo calls only cloud formula API in production;
- public responses are filtered through an allowlist;
- secrets are server-side only;
- CI covers local, cloud, and cloud failure behavior;
- staging/prod behavior is documented and tested.

## Non-goals of this document

This document does not:

- deploy Selectel;
- move files;
- remove local formula;
- change scoring behavior;
- change formula weights;
- change Excel output;
- change PDF output;
- change API routes;
- change Streamlit UI;
- change Admin/Public/PWA integration.
