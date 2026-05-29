from validation.input_validator import REQUIRED_COLUMNS, SOFT_LIMITS


def _empty(value):
    if value is None:
        return True
    text = str(value).strip()
    return text == "" or text.lower() in {"nan", "none", "—", "-"}


def _to_float(value):
    if _empty(value):
        return None
    try:
        return float(str(value).replace(",", "."))
    except Exception:
        return None


def _missing_required_values(row):
    return [col for col in REQUIRED_COLUMNS if _empty(row.get(col))]


def _all_required_missing(row):
    return len(_missing_required_values(row)) == len(REQUIRED_COLUMNS)


def _possible_scale_issue(value, column):
    number = _to_float(value)
    if number is None or column not in SOFT_LIMITS:
        return ""

    low, high = SOFT_LIMITS[column]
    if low <= number <= high:
        return ""

    candidates = []
    for divisor in [10, 100]:
        adjusted = number / divisor
        if low <= adjusted <= high:
            candidates.append(f"{column}={value} maybe {adjusted:g}")

    return "; ".join(candidates)


def _row_scale_issues(row):
    issues = []
    for column in REQUIRED_COLUMNS:
        issue = _possible_scale_issue(row.get(column), column)
        if issue:
            issues.append(issue)
    return "; ".join(issues)


def _geometry_status(row):
    missing = _missing_required_values(row)
    if len(missing) == len(REQUIRED_COLUMNS):
        return "Catalog Data Only"
    if missing:
        return "Missing Geometry"
    scale = _row_scale_issues(row)
    if scale:
        return "Possible Scale Issue"
    return "Geometry Ready"


def _upload_quality_status(row):
    geometry = _geometry_status(row)
    measurement = str(row.get("Measurement Parse Status", ""))
    conflict = str(row.get("Measurement Conflict", ""))

    if geometry != "Geometry Ready":
        return geometry
    if conflict == "Yes":
        return "Needs Review: Measurement Conflict"
    if measurement == "Failed":
        return "Needs Review: Measurement Failed"
    if measurement == "Missing":
        return "Ready: Geometry Only"
    return "Ready"


def column_recognition_summary(mapping_df):
    if mapping_df is None or mapping_df.empty:
        return "mapping unavailable"

    total = len(mapping_df)
    mapped = int((mapping_df["Status"].astype(str) != "not mapped").sum()) if "Status" in mapping_df.columns else 0
    unmapped = total - mapped
    return f"{mapped}/{total} recognized; {unmapped} not mapped"


def add_upload_quality_columns(df, mapping_df=None):
    df = df.copy()
    summary = column_recognition_summary(mapping_df)

    missing_values = []
    scale_issues = []
    geometry_statuses = []
    upload_statuses = []

    for _, row in df.iterrows():
        missing = _missing_required_values(row)
        missing_values.append(", ".join(missing))
        scale_issues.append(_row_scale_issues(row))
        geometry_statuses.append(_geometry_status(row))
        upload_statuses.append(_upload_quality_status(row))

    df["Missing Geometry Fields"] = missing_values
    df["Possible Scale Issues"] = scale_issues
    df["Geometry Status"] = geometry_statuses
    df["Upload Quality Status"] = upload_statuses
    df["Column Recognition Status"] = summary
    return df
