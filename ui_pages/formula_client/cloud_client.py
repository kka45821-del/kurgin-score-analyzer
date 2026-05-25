import json
import os
from urllib import request, error


class CloudFormulaError(RuntimeError):
    pass


def calculate_stone_cloud(engine_kwargs, endpoint=None, api_key=None, timeout=20):
    """Call a closed formula API.

    Expected response JSON shape is the same as core_formula.main_engine.get_final_diamond_analysis.
    Environment variables / Streamlit secrets can provide:
      FORMULA_API_URL
      FORMULA_API_KEY
    """
    endpoint = endpoint or os.getenv("FORMULA_API_URL", "").strip()
    api_key = api_key or os.getenv("FORMULA_API_KEY", "").strip()
    if not endpoint:
        raise CloudFormulaError("FORMULA_API_URL is not configured")

    payload = json.dumps({"stone": engine_kwargs}, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = request.Request(endpoint, data=payload, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except error.HTTPError as e:
        details = e.read().decode("utf-8", errors="ignore")
        raise CloudFormulaError(f"Cloud formula HTTP {e.code}: {details}") from e
    except Exception as e:
        raise CloudFormulaError(f"Cloud formula request failed: {e}") from e
