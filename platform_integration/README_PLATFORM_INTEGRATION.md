# KURGIN Platform Integration Adapter v1.12.1

## Purpose

Prepare a stable integration layer between KURGIN Platform Tools and the private Formula API.

## Added endpoint

```text
POST /v1/platform/stone-card
```

This endpoint returns a compact card payload:

```text
identity
stone
score
tags
summary
measurements
quality
report
version
actions
experimental
```

## Why this matters

KURGIN Platform should not understand formula internals.

Recommended flow:

```text
KURGIN Platform Tools page
  -> Platform backend route
    -> Selectel Formula API
      -> /v1/platform/stone-card
        -> render card + optional PDF action
```

## Public vs experimental

Stable/public sections:

```text
identity, stone, score, tags, summary, measurements, quality, report, version, actions
```

Experimental section:

```text
experimental
```

Keep experimental fields internal/preview until final promotion.

## Client examples

- `formula_api_client.py`
- `formula_api_client.ts`
- `nextjs_route_handler_example.ts`
