from formula_versions.current.runner import calculate as current_calculate
from config_settings.engine_config import ENGINE_VERSION
from formula_modules.interpretation.score_band_interpreter import get_score_band_key, get_score_band_label
from formula_modules.measurement_spread.spread_engine import build_measurement_spread_metrics


FORMULA_VERSION_ID = "experimental_v2_candidate"
FORMULA_VERSION_NAME = "Experimental v2 Candidate — Class Cap Only"
FORMULA_VERSION_TYPE = "experimental"
FORMULA_CANDIDATE_MODE = "class_cap_only"


CLASS_MAX_SCORE = {
    "elite": 100.0,
    "premium": 98.49,
    "high": 94.99,
    "standard": 89.99,
    "fair": 79.99,
    "poor": 69.99,
    "rejected": 49.99,
}

CLASS_ORDER = ["rejected", "poor", "fair", "standard", "high", "premium", "elite"]


def _to_bool(value):
    if value in [True, 1, "1", "true", "True", "YES", "Yes", "yes"]:
        return True
    return False


def _str(value):
    return "" if value is None else str(value)


def _stricter_cap(current_cap, new_cap):
    if not current_cap:
        return new_cap
    try:
        return CLASS_ORDER[min(CLASS_ORDER.index(current_cap), CLASS_ORDER.index(new_cap))]
    except Exception:
        return current_cap or new_cap


def _cap_label_ru(cap_key):
    if not cap_key:
        return ""
    score = CLASS_MAX_SCORE.get(cap_key)
    if score is None:
        return ""
    return get_score_band_label(score, language="RU")


def _determine_cap(base_score, row, metrics):
    """Return cap_key, reason.

    This is class-cap-only. It does not reward large diameter and does not penalize
    measurement problems as stone defects.
    """
    base_key = get_score_band_key(base_score)
    spread = _str(metrics.get("VisualSpreadStatus"))
    roundness = _str(metrics.get("DiameterSymmetryStatus"))
    consistency = _str(metrics.get("MeasurementConsistencyStatus"))
    parse_status = _str(row.get("Measurement Parse Status", ""))
    conflict = _str(row.get("Measurement Conflict", ""))

    reasons = []
    cap = ""

    # Data quality guards: no cap if measurements are not reliable.
    if parse_status in {"Missing", "Failed"}:
        return "", "measurement data unavailable; class cap not applied"
    if conflict == "Yes":
        return "", "measurement sources conflict; review only"
    if consistency == "Warning":
        return "", "measurement consistency warning; review only"

    if spread == "Small for Weight":
        reasons.append("Small for Weight")
        if base_key == "elite":
            cap = _stricter_cap(cap, "premium")
        elif base_key == "premium":
            cap = _stricter_cap(cap, "high")
    elif spread == "Hidden Weight Risk":
        reasons.append("Hidden Weight Risk")
        if base_key == "elite":
            cap = _stricter_cap(cap, "high")
        elif base_key == "premium":
            cap = _stricter_cap(cap, "high")
        elif base_key == "high":
            cap = _stricter_cap(cap, "standard")
    elif spread == "Wide but Risky":
        reasons.append("Wide but Risky")
        if base_key in {"elite", "premium"}:
            cap = _stricter_cap(cap, "high")
        elif base_key == "high":
            cap = _stricter_cap(cap, "standard")

    if roundness == "Out-of-round Risk":
        reasons.append("Out-of-round Risk")
        if base_key in {"elite", "premium"}:
            cap = _stricter_cap(cap, "high")
        elif base_key == "high":
            cap = _stricter_cap(cap, "standard")
    elif roundness == "Roundness Check":
        reasons.append("Roundness Check")
        if base_key == "elite":
            cap = _stricter_cap(cap, "premium")

    return cap, "; ".join(reasons) if reasons else "no cap reason"


def calculate(engine_kwargs):
    """Compatibility method: without row data, candidate equals current formula.

    Class cap needs weight/measurements, so regression runner should call
    calculate_with_row(row, engine_kwargs).
    """
    result = current_calculate(engine_kwargs)
    result["candidate_mode"] = FORMULA_CANDIDATE_MODE
    result["candidate_class_cap"] = ""
    result["candidate_cap_reason"] = "row data unavailable"
    result["candidate_base_score"] = result.get("final_score")
    result["candidate_public_score"] = result.get("final_score")
    result["candidate_public_band_ru"] = get_score_band_label(result.get("final_score"), language="RU")
    result["candidate_public_band_key"] = get_score_band_key(result.get("final_score"))
    return result


def calculate_with_row(row, engine_kwargs):
    """Run current formula, then apply experimental class-cap-only candidate logic."""
    base_result = current_calculate(engine_kwargs)
    base_score = base_result.get("final_score")

    metrics = build_measurement_spread_metrics(row)
    cap_key, cap_reason = _determine_cap(base_score, row, metrics)

    public_score = base_score
    cap_applied = False
    if cap_key and cap_key in CLASS_MAX_SCORE:
        capped = min(float(base_score), CLASS_MAX_SCORE[cap_key])
        if capped < float(base_score):
            public_score = round(capped, 2)
            cap_applied = True

    public_band_key = get_score_band_key(public_score)
    public_band_ru = get_score_band_label(public_score, language="RU")

    result = dict(base_result)
    result["candidate_mode"] = FORMULA_CANDIDATE_MODE
    result["candidate_base_score"] = base_score
    result["candidate_public_score"] = public_score
    result["candidate_public_band_key"] = public_band_key
    result["candidate_public_band_ru"] = public_band_ru
    result["candidate_class_cap"] = cap_key
    result["candidate_class_cap_ru"] = _cap_label_ru(cap_key)
    result["candidate_cap_reason"] = cap_reason
    result["candidate_cap_applied"] = cap_applied

    # For regression visibility, candidate final_score is the public capped score.
    # The original base score is preserved in candidate_base_score.
    result["final_score"] = public_score
    result["final_verdict"] = f"{public_band_ru} — Candidate v2" if cap_applied else base_result.get("final_verdict")
    result["engine_version"] = f"{ENGINE_VERSION} + Candidate v2 class-cap-only"
    return result


def get_metadata():
    return {
        "version_id": FORMULA_VERSION_ID,
        "name": FORMULA_VERSION_NAME,
        "type": FORMULA_VERSION_TYPE,
        "engine_version": ENGINE_VERSION,
        "candidate_mode": FORMULA_CANDIDATE_MODE,
        "official_score_changed": False,
        "notes": "Experimental candidate. Applies public class cap only when reliable diameter/spread data challenges high class.",
    }
