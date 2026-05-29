import re
import pandas as pd


def _empty(value):
    if value is None:
        return True
    text = str(value).strip()
    return text == "" or text.lower() in {"nan", "none", "—", "-"}


def _as_text(value):
    return "" if _empty(value) else str(value).strip()


def _to_float(value):
    if _empty(value):
        return None
    try:
        text = str(value).strip().replace(",", ".")
        # remove common symbols while keeping decimal point
        text = re.sub(r"[^0-9.\-]+", "", text)
        if text in {"", "-", ".", "-."}:
            return None
        return float(text)
    except Exception:
        return None


def build_measurement_metrics(length, width, height):
    length = _to_float(length)
    width = _to_float(width)
    height = _to_float(height)

    if length is None or width is None or height is None:
        return {}

    min_d = min(length, width)
    max_d = max(length, width)
    avg_d = (min_d + max_d) / 2
    diff = max_d - min_d
    roundness = (diff / avg_d * 100) if avg_d else None

    return {
        "MinDiameter": round(min_d, 3),
        "MaxDiameter": round(max_d, 3),
        "AvgDiameter": round(avg_d, 3),
        "DepthMM": round(height, 3),
        "DiameterDiff": round(diff, 3),
        "RoundnessDeviation": round(roundness, 3) if roundness is not None else None,
    }


def parse_measurements(value):
    """
    Parse common round diamond measurements:
    - 6.360x6.400x3.970
    - 6.36 - 6.40 x 3.97 mm
    - 6.36*6.40*3.97
    Returns min/max/avg diameter and depth in mm.
    """
    text = _as_text(value).lower()
    if not text:
        return {}

    text = text.replace(",", ".")
    text = text.replace("×", "x").replace("*", "x")
    text = text.replace("mm", " ")
    nums = re.findall(r"\d+(?:\.\d+)?", text)

    if len(nums) < 3:
        return {}

    return build_measurement_metrics(nums[0], nums[1], nums[2])


def parse_cert_comment(value):
    text = _as_text(value)
    low = text.lower().replace(" ", "")
    result = {}

    if not text:
        return result

    if "chemicalvapordeposition" in low or "cvd" in low:
        result["Growth Method"] = "CVD"
    elif "highpressure" in low or "hpht" in low:
        result["Growth Method"] = "HPHT"

    type_match = re.search(r"type\s*([ivx]+[a-z]?)", text, flags=re.IGNORECASE)
    if not type_match:
        type_match = re.search(r"type([ivx]+[a-z]?)", low, flags=re.IGNORECASE)

    if type_match:
        result["Diamond Type"] = "Type " + type_match.group(1).upper()

    if "postgrowth" in low or "post-growth" in text.lower() or "treated" in low or "treatment" in low:
        result["Treatment"] = text

    return result


def _depth_consistency_delta(metrics, depth_percent):
    if not metrics:
        return None

    avg = _to_float(metrics.get("AvgDiameter"))
    depth_mm = _to_float(metrics.get("DepthMM"))
    stated = _to_float(depth_percent)

    if avg is None or depth_mm is None or stated is None or avg <= 0:
        return None

    calculated = depth_mm / avg * 100
    return abs(calculated - stated)


def _candidate_measurements(row):
    candidates = []

    measurements_metrics = parse_measurements(row.get("Measurements"))
    if measurements_metrics:
        candidates.append(("Measurements", measurements_metrics))

    length_metrics = {}
    if all(not _empty(row.get(col)) for col in ["Length", "Width", "Height"]):
        length_metrics = build_measurement_metrics(row.get("Length"), row.get("Width"), row.get("Height"))
    if length_metrics:
        candidates.append(("Length/Width/Height", length_metrics))

    explicit_metrics = {}
    if all(not _empty(row.get(col)) for col in ["MinDiameter", "MaxDiameter", "DepthMM"]):
        explicit_metrics = build_measurement_metrics(row.get("MinDiameter"), row.get("MaxDiameter"), row.get("DepthMM"))
    if explicit_metrics:
        candidates.append(("Explicit Dimensions", explicit_metrics))

    return candidates


def _metrics_differ(a, b, tolerance=0.03):
    if not a or not b:
        return False
    for key in ["MinDiameter", "MaxDiameter", "DepthMM"]:
        av = _to_float(a.get(key))
        bv = _to_float(b.get(key))
        if av is None or bv is None:
            continue
        if abs(av - bv) > tolerance:
            return True
    return False


def _choose_measurement_source(row):
    candidates = _candidate_measurements(row)

    if not candidates:
        # detect attempted but failed input
        if not _empty(row.get("Measurements")):
            return {}, "Failed", "Measurements", "Could not parse measurements", "No", ""
        if any(not _empty(row.get(col)) for col in ["Length", "Width", "Height"]):
            return {}, "Failed", "Length/Width/Height", "Length, Width and Height must all be present", "No", ""
        if any(not _empty(row.get(col)) for col in ["MinDiameter", "MaxDiameter", "DepthMM"]):
            return {}, "Failed", "Explicit Dimensions", "MinDiameter, MaxDiameter and DepthMM must all be present", "No", ""
        return {}, "Missing", "", "Measurements not found", "No", ""

    conflict = "No"
    warning = ""

    # Check if sources conflict.
    if len(candidates) > 1:
        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                if _metrics_differ(candidates[i][1], candidates[j][1]):
                    conflict = "Yes"

    # Choose the candidate that best matches DepthPercent if possible.
    scored = []
    for source, metrics in candidates:
        delta = _depth_consistency_delta(metrics, row.get("DepthPercent"))
        # If no depth consistency available, use preference order.
        preference = {"Explicit Dimensions": 0, "Length/Width/Height": 1, "Measurements": 2}.get(source, 9)
        score = delta if delta is not None else 999 + preference
        scored.append((score, preference, source, metrics, delta))

    scored.sort(key=lambda x: (x[0], x[1]))
    _, _, chosen_source, chosen_metrics, chosen_delta = scored[0]

    if conflict == "Yes":
        warning = "Measurement sources conflict; selected source with best Depth % consistency"
    elif chosen_delta is not None and chosen_delta > 0.70:
        warning = "Measurements and Depth % are inconsistent"

    return chosen_metrics, "OK", chosen_source, warning, conflict, chosen_source


def add_measurement_parse_status(df):
    df = df.copy()

    for key in ["MinDiameter", "MaxDiameter", "AvgDiameter", "DepthMM", "DiameterDiff", "RoundnessDeviation"]:
        if key not in df.columns:
            df[key] = None

    statuses = []
    sources = []
    warnings = []
    conflicts = []
    chosen_sources = []

    for idx, row in df.iterrows():
        metrics, status, source, warning, conflict, chosen = _choose_measurement_source(row)

        if metrics:
            for key, value in metrics.items():
                df.at[idx, key] = value
            if "Measurements" not in df.columns:
                df["Measurements"] = None
            if _empty(df.at[idx, "Measurements"]):
                df.at[idx, "Measurements"] = f"{metrics['MinDiameter']:.3f}x{metrics['MaxDiameter']:.3f}x{metrics['DepthMM']:.3f}"

        statuses.append(status)
        sources.append(source)
        warnings.append(warning)
        conflicts.append(conflict)
        chosen_sources.append(chosen)

    df["Measurement Parse Status"] = statuses
    df["Measurement Source"] = sources
    df["Measurement Warning"] = warnings
    df["Measurement Conflict"] = conflicts
    df["Chosen Measurement Source"] = chosen_sources
    return df


def enrich_dataframe_fields(df):
    df = df.copy()

    if "Shape" in df.columns:
        df["Shape"] = df["Shape"].astype(str).str.upper().str.strip()

    if "Fluorescence Intensity" in df.columns and "Fluorescence" not in df.columns:
        df["Fluorescence"] = df["Fluorescence Intensity"]

    if "Treatment" in df.columns:
        if "Growth Method" not in df.columns:
            df["Growth Method"] = None
        df["Growth Method"] = df.apply(
            lambda row: row.get("Growth Method") if not _empty(row.get("Growth Method")) else (
                str(row.get("Treatment")).upper().strip()
                if str(row.get("Treatment")).upper().strip() in {"CVD", "HPHT"}
                else row.get("Growth Method")
            ),
            axis=1
        )

    if "Cert comment" in df.columns:
        parsed_comments = df["Cert comment"].apply(parse_cert_comment)
        for key in ["Growth Method", "Diamond Type", "Treatment"]:
            if key not in df.columns:
                df[key] = parsed_comments.apply(lambda x: x.get(key))
            else:
                df[key] = df.apply(
                    lambda row: row[key] if not _empty(row.get(key)) else parse_cert_comment(row.get("Cert comment")).get(key),
                    axis=1
                )

    df = add_measurement_parse_status(df)
    return df


def enrich_series_fields(row):
    df = pd.DataFrame([row])
    return enrich_dataframe_fields(df).iloc[0]
