# Formula Client Layer

This layer separates the Streamlit UI from the formula engine.

Modes:
- `local` — current fallback: formula runs inside the app.
- `cloud` — calls a closed HTTPS formula API.
- `cloud_fallback` — calls cloud first, falls back to local.

Environment variables / secrets:
- `FORMULA_MODE`
- `FORMULA_API_URL`
- `FORMULA_API_KEY`

Target next step: deploy formula to Yandex Cloud Function or another closed backend.
