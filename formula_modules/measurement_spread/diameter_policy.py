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


def _is_bad_roundness(status):
    return str(status) in {"Roundness Check", "Out-of-round Risk"}


def _is_bad_spread(status):
    return str(status) in {"Small for Weight", "Hidden Weight Risk", "Wide but Risky"}


def build_diameter_policy(row):
    """Research-oriented policy layer.

    It does not change official KURGIN Score.
    It explains whether the diameter/spread profile supports or challenges the current public class.
    """
    calc_status = str(row.get("Calculation Status", ""))
    if calc_status != "OK":
        return {
            "Diameter Policy Status": "Not available",
            "Diameter Policy Action": "No policy check",
            "Diameter Policy Reason": "KURGIN Score was not calculated",
            "High Score Diameter Flag": False,
        }

    score = _to_float(row.get("Kurgin Score"))
    spread = str(row.get("VisualSpreadStatus", ""))
    roundness = str(row.get("DiameterSymmetryStatus", ""))
    consistency = str(row.get("MeasurementConsistencyStatus", ""))
    parse_status = str(row.get("Measurement Parse Status", ""))
    conflict = str(row.get("Measurement Conflict", ""))

    reasons = []

    if parse_status in {"Missing", "Failed"}:
        return {
            "Diameter Policy Status": "Data warning",
            "Diameter Policy Action": "Do not use diameter for class decision",
            "Diameter Policy Reason": "Measurements are missing or not parsed",
            "High Score Diameter Flag": bool(score is not None and score >= 90),
        }

    if conflict == "Yes":
        reasons.append("measurement sources conflict")

    if consistency == "Warning":
        reasons.append("measurements conflict with Depth %")

    if _is_bad_spread(spread):
        reasons.append(f"visual spread status: {spread}")

    if _is_bad_roundness(roundness):
        reasons.append(f"diameter symmetry status: {roundness}")

    high_score = bool(score is not None and score >= 90)
    premium_score = bool(score is not None and score >= 95)
    elite_score = bool(score is not None and score >= 98.5)

    if elite_score and reasons:
        return {
            "Diameter Policy Status": "Class review",
            "Diameter Policy Action": "Review Elite class before public display",
            "Diameter Policy Reason": "; ".join(reasons),
            "High Score Diameter Flag": True,
        }

    if premium_score and reasons:
        return {
            "Diameter Policy Status": "Class review",
            "Diameter Policy Action": "Review Premium class before public display",
            "Diameter Policy Reason": "; ".join(reasons),
            "High Score Diameter Flag": True,
        }

    if high_score and reasons:
        return {
            "Diameter Policy Status": "Watch",
            "Diameter Policy Action": "Keep score, show diameter warning",
            "Diameter Policy Reason": "; ".join(reasons),
            "High Score Diameter Flag": True,
        }

    if reasons:
        return {
            "Diameter Policy Status": "Watch",
            "Diameter Policy Action": "Show warning only",
            "Diameter Policy Reason": "; ".join(reasons),
            "High Score Diameter Flag": False,
        }

    if spread in {"Good Spread", "Wide Spread"} and roundness in {"Excellent Roundness", "Good Roundness"}:
        return {
            "Diameter Policy Status": "Confirmed",
            "Diameter Policy Action": "No diameter restriction",
            "Diameter Policy Reason": "spread and roundness support the result",
            "High Score Diameter Flag": False,
        }

    return {
        "Diameter Policy Status": "Neutral",
        "Diameter Policy Action": "No action",
        "Diameter Policy Reason": "diameter policy does not change the result",
        "High Score Diameter Flag": False,
    }


def add_diameter_policy_columns(df):
    df = df.copy()
    rows = []
    for _, row in df.iterrows():
        rows.append(build_diameter_policy(row))

    import pandas as pd
    policy_df = pd.DataFrame(rows, index=df.index)
    for col in policy_df.columns:
        df[col] = policy_df[col]
    return df
