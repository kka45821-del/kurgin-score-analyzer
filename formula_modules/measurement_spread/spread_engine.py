from formula_modules.interpretation.score_band_interpreter import get_score_band_label, get_score_band_key

EXPECTED_DIAMETER_BASE = 6.45
EXPECTED_DIAMETER_MODEL = "6.45 × carat^(1/3)"


def _to_float(value):
    try:
        if value is None:
            return None
        text = str(value).strip().replace(",", ".")
        if text == "" or text.lower() in {"nan", "none", "—", "-"}:
            return None
        return float(text)
    except Exception:
        return None


def expected_diameter(weight):
    weight = _to_float(weight)
    if weight is None or weight <= 0:
        return None
    return EXPECTED_DIAMETER_BASE * (weight ** (1 / 3))


def spread_delta_percent(avg_diameter, weight):
    avg = _to_float(avg_diameter)
    expected = expected_diameter(weight)
    if avg is None or expected is None or expected <= 0:
        return None
    return (avg - expected) / expected * 100


def visual_spread_status(spread_delta, depth_percent=None):
    delta = _to_float(spread_delta)
    depth = _to_float(depth_percent)

    if delta is None:
        return "Not calculated"

    # If face-up is wide and the diamond is shallow, treat it as riskier.
    if delta > 1.5 and depth is not None and depth < 59.0:
        return "Wide but Risky"

    if delta < -3.0:
        return "Hidden Weight Risk"
    if delta < -1.5:
        return "Small for Weight"
    if delta <= 1.5:
        return "Good Spread"
    if delta <= 3.0:
        return "Wide Spread"
    return "Wide but Risky"


def diameter_symmetry_status(roundness_deviation):
    value = _to_float(roundness_deviation)
    if value is None:
        return "Not calculated"
    if value <= 0.50:
        return "Excellent Roundness"
    if value <= 1.00:
        return "Good Roundness"
    if value <= 1.50:
        return "Roundness Check"
    return "Out-of-round Risk"


def diameter_symmetry_score(roundness_deviation):
    value = _to_float(roundness_deviation)
    if value is None:
        return "Not calculated"
    score = max(0, min(100, 100 - value * 25))
    return round(score, 2)


def depth_from_measurements_percent(avg_diameter, depth_mm):
    avg = _to_float(avg_diameter)
    depth = _to_float(depth_mm)
    if avg is None or depth is None or avg <= 0:
        return None
    return depth / avg * 100


def measurement_consistency(avg_diameter, depth_mm, depth_percent):
    calculated = depth_from_measurements_percent(avg_diameter, depth_mm)
    stated = _to_float(depth_percent)

    if calculated is None or stated is None:
        return {
            "DepthFromMeasurements%": None,
            "MeasurementConsistencyDelta%": None,
            "MeasurementConsistencyStatus": "Not calculated",
            "MeasurementConsistencyWarning": "",
        }

    delta = calculated - stated
    abs_delta = abs(delta)

    if abs_delta <= 0.30:
        status = "OK"
        warning = ""
    elif abs_delta <= 0.70:
        status = "Check"
        warning = "Small mismatch between measurements and Depth %"
    else:
        status = "Warning"
        warning = "Measurements and Depth % are inconsistent"

    return {
        "DepthFromMeasurements%": round(calculated, 3),
        "MeasurementConsistencyDelta%": round(delta, 3),
        "MeasurementConsistencyStatus": status,
        "MeasurementConsistencyWarning": warning,
    }


def diameter_spread_modifier_preview(spread_status, symmetry_status, spread_delta=None, depth_percent=None):
    """Preview-only modifier. It does not change official KURGIN Score."""
    modifier = 0.0
    delta = _to_float(spread_delta)
    depth = _to_float(depth_percent)

    if spread_status == "Small for Weight":
        modifier -= 1.0
        if delta is not None and delta < -2.25:
            modifier -= 0.5
    elif spread_status == "Hidden Weight Risk":
        modifier -= 2.5
        if delta is not None and delta < -5.0:
            modifier -= 1.0
    elif spread_status == "Wide but Risky":
        modifier -= 1.5
        if depth is not None and depth < 57.5:
            modifier -= 0.75

    if symmetry_status == "Roundness Check":
        modifier -= 0.75
    elif symmetry_status == "Out-of-round Risk":
        modifier -= 1.5

    # Good diameter should not materially increase the score.
    return round(max(-4.0, min(0.5, modifier)), 2)


def score_class_cap_preview(spread_status, symmetry_status, spread_delta=None):
    """Preview class cap. This is a research tool, not official score logic."""
    delta = _to_float(spread_delta)

    cap = ""
    if spread_status == "Hidden Weight Risk":
        cap = "High"
        if delta is not None and delta < -5.0:
            cap = "Standard"
    elif spread_status == "Small for Weight":
        cap = "Premium"
    elif spread_status == "Wide but Risky":
        cap = "High"

    if symmetry_status == "Out-of-round Risk":
        cap = "High" if cap == "" else min_cap(cap, "High")
    elif symmetry_status == "Roundness Check":
        cap = "Premium" if cap == "" else min_cap(cap, "Premium")

    return cap


_CAP_MAX_SCORE = {
    "Elite": 100.0,
    "Premium": 98.49,
    "High": 94.99,
    "Standard": 89.99,
    "Fair": 79.99,
    "Poor": 69.99,
    "Rejected": 49.99,
}

_CAP_ORDER = ["Rejected", "Poor", "Fair", "Standard", "High", "Premium", "Elite"]


def min_cap(current_cap, new_cap):
    """Return the stricter of two caps."""
    if not current_cap:
        return new_cap
    try:
        return _CAP_ORDER[min(_CAP_ORDER.index(current_cap), _CAP_ORDER.index(new_cap))]
    except Exception:
        return current_cap or new_cap


def adjusted_score_preview(base_score, modifier, cap):
    score = _to_float(base_score)
    mod = _to_float(modifier)
    if score is None:
        return None
    if mod is None:
        mod = 0.0
    adjusted = max(0.0, min(100.0, score + mod))

    if cap in _CAP_MAX_SCORE:
        adjusted = min(adjusted, _CAP_MAX_SCORE[cap])

    return round(adjusted, 2)


def build_measurement_spread_metrics(row):
    expected = expected_diameter(row.get("Weight"))
    spread_delta = spread_delta_percent(row.get("AvgDiameter"), row.get("Weight"))
    spread_status = visual_spread_status(spread_delta, row.get("DepthPercent"))
    symmetry_status = diameter_symmetry_status(row.get("RoundnessDeviation"))
    symmetry_score = diameter_symmetry_score(row.get("RoundnessDeviation"))

    consistency = measurement_consistency(
        row.get("AvgDiameter"),
        row.get("DepthMM"),
        row.get("DepthPercent"),
    )

    modifier = diameter_spread_modifier_preview(
        spread_status,
        symmetry_status,
        spread_delta=spread_delta,
        depth_percent=row.get("DepthPercent"),
    )

    cap = score_class_cap_preview(
        spread_status,
        symmetry_status,
        spread_delta=spread_delta,
    )

    adjusted = adjusted_score_preview(row.get("Kurgin Score"), modifier, cap)

    result = {
        "ExpectedDiameter": round(expected, 3) if expected is not None else None,
        "ExpectedDiameterModel": EXPECTED_DIAMETER_MODEL,
        "SpreadDelta %": round(spread_delta, 3) if spread_delta is not None else None,
        "VisualSpreadStatus": spread_status,
        "DiameterSymmetryStatus": symmetry_status,
        "DiameterSymmetryScore": symmetry_score,
        "DiameterSpreadModifierPreview": modifier,
        "ScoreClassCapPreview": cap,
        "AdjustedKURGINScorePreview": adjusted,
        "AdjustedScoreBandPreview": get_score_band_label(adjusted, language="RU") if adjusted is not None else "Not calculated",
    }
    result.update(consistency)
    return result


def add_measurement_spread_columns(df):
    df = df.copy()
    if df.empty:
        return df

    rows = []
    for _, row in df.iterrows():
        rows.append(build_measurement_spread_metrics(row))

    import pandas as pd
    metrics_df = pd.DataFrame(rows, index=df.index)

    for col in metrics_df.columns:
        df[col] = metrics_df[col]

    return df
