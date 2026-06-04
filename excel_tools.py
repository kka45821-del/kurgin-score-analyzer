from datetime import datetime
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import re
import pandas as pd

from config_settings.engine_config import ENGINE_VERSION
from formula_client.engine_client import calculate_stone, get_formula_mode
from data_models.stone import StoneInput
from excel_processing.column_mapping import apply_column_mapping
from excel_processing.field_enrichment import enrich_dataframe_fields, enrich_series_fields
from excel_processing.upload_quality import add_upload_quality_columns
from platform_config.app_config import SUPPORTED_SHAPES, UNSUPPORTED_SHAPE_MESSAGE
from report_templates.report_columns import filter_report_dataframe
from report_templates.unified_report_schema import (
    DATA_DICTIONARY_ROWS,
    KURGIN_CARD_COLUMNS,
    REPORT_SCHEMA_VERSION,
    SECTION_ORDER,
    UNIFIED_REPORT_COLUMNS,
    select_existing,
)
from report_templates.pdf_single_stone_report import create_single_stone_pdf
from translations_lang.label_translator import translate_verdict, translate_tags
from formula_modules.interpretation.interpretation_engine import add_interpretation_columns
from formula_modules.measurement_spread.spread_engine import add_measurement_spread_columns
from formula_modules.measurement_spread.diameter_policy import add_diameter_policy_columns
from validation.input_validator import REQUIRED_COLUMNS, get_missing_columns, validate_row

ID_COLUMN = "Report #"

REPORT_TEMPLATE_VERSION = "KURGIN PDF v1.10.7"
FORMULA_OUTPUT_VERSION = "KURGIN Output v1.10.7"

PDF_REPORT_COLUMNS = [
    "KURGIN Report ID",
    "PDF Report Status",
    "PDF Report File",
    "PDF Report URL",
    "Report Template Version",
]

PLATFORM_IMPORT_COLUMNS = [
    "KURGIN Import ID",
    "Formula Output Version",
    "Data Completeness %",
    "Report Quality Status",
    "PDF Generation Mode",
    "platform_import_status",
    "recommended_pdf_priority",
    "Diameter Policy Status",
    "Diameter Policy Action",
    "Diameter Policy Reason",
    "High Score Diameter Flag",
    "tag_light",
    "tag_structure",
    "tag_spread",
    "tag_risk",
    "tag_certificate",
    "tag_commercial",
    "certificate_flags",
    "spread_score",
    "spread_status",
    "diameter_symmetry_score",
    "diameter_symmetry_status",
    "roundness_status",
    "commercial_view",
    "value_score",
]

TAG_COLUMNS = [f"tag{i}" for i in range(1, 7)]

RESULTS_COLUMNS = [
    "Stock #", "Availability", "Report #", "Lab", "Shape", "Weight", "Color", "Clarity",
    "Cut", "Polish", "Symmetry", "Fluorescence Intensity", "Measurements",
    "MinDiameter", "MaxDiameter", "AvgDiameter", "DepthMM", "DiameterDiff", "RoundnessDeviation",
    "ExpectedDiameter", "SpreadDelta %", "VisualSpreadStatus", "DiameterSymmetryStatus",
    "MeasurementConsistencyStatus", "DiameterSpreadModifierPreview", "ScoreClassCapPreview",
    "AdjustedKURGINScorePreview", "AdjustedScoreBandPreview",
    "Diameter Policy Status", "Diameter Policy Action", "Diameter Policy Reason", "High Score Diameter Flag",
    "TablePercent", "DepthPercent", "CrownAngle", "PavilionAngle", "CrownPercent", "PavilionPercent", "GirdlePercent",
    "Kurgin Score", "Verdict Local", "score_band_label_ru",
    "tags_all", "tag1", "tag2", "tag3", "tag4", "tag5", "tag6",
    "interpretation_short_ru", "recommendation_ru", "warning_ru",
    "Data Completeness %", "Report Quality Status",
    "platform_import_status", "recommended_pdf_priority",
    "PDF Report Status", "PDF Report File", "PDF Generation Mode",
    "Upload Quality Status", "Geometry Status", "Missing Geometry Fields", "Possible Scale Issues",
    "Column Recognition Status",
    "Calculation Status",
]

DETAILS_COLUMNS = [
    # Identification
    "KURGIN Import ID", "Stone Title", "Identification Line", "Stock #", "Availability", "Location", "Country", "State", "City",
    "Report #", "Lab", "Shape", "Weight", "Color", "Clarity",
    # Certificate details
    "Cut", "Polish", "Symmetry", "Hearts & Arrows", "Fluorescence", "Fluorescence Intensity", "Fluorescence Color",
    "Measurements", "Length", "Width", "Height", "Ratio", "Treatment", "Growth Method", "Diamond Type",
    "Origin Type", "Luster", "Category", "Inscription", "Cert comment", "Member Comment", "CertFile",
    "Report Issue Date", "Report Type", "Is Matched Pair Separable", "Country of Polishing",
    # Visual flags / inclusions
    "Shade", "Milky", "Eye Clean", "BGM", "KeyToSymbols", "White Inclusion", "Black Inclusion", "Open Inclusion",
    "Fancy Color", "Fancy Color Intensity", "Fancy Color Overtone",
    # Geometry and parsed dimensions
    "DepthPercent", "TablePercent", "CrownPercent", "CrownAngle", "PavilionPercent", "PavilionAngle",
    "GirdlePercent", "GirdleThin", "GirdleThick", "GirdleCondition", "CuletSize", "CuletCondition",
    "MinDiameter", "MaxDiameter", "AvgDiameter", "DepthMM", "DiameterDiff", "RoundnessDeviation",
    "Measurement Parse Status", "Measurement Source", "Measurement Warning", "Measurement Conflict", "Chosen Measurement Source", "Measurement Conflict", "Chosen Measurement Source",
    "ExpectedDiameter", "ExpectedDiameterModel", "SpreadDelta %", "VisualSpreadStatus",
    "DiameterSymmetryStatus", "DiameterSymmetryScore",
    "DepthFromMeasurements%", "MeasurementConsistencyDelta%", "MeasurementConsistencyStatus", "MeasurementConsistencyWarning",
    "DiameterSpreadModifierPreview", "ScoreClassCapPreview", "AdjustedKURGINScorePreview", "AdjustedScoreBandPreview",
    "Diameter Policy Status", "Diameter Policy Action", "Diameter Policy Reason", "High Score Diameter Flag",
    # Commercial / media
    "price_rub", "price_usd", "price_per_carat_usd", "supplier", "Diamond Video", "Diamond Image",
    # KURGIN result
    "Kurgin Score", "Verdict", "Verdict Local", "score_band", "score_band_label_ru",
    "Triple Score", "Structure Modifier", "Visual Check", "Critical Risk",
    "Nailhead", "Fisheye", "Fire Loss", "Depth Dev", "Crown Dev", "Pavilion Dev", "Balance Err", "Girdle Penalty",
    "Tags", "Tags Local", "tags_all", "tag1", "tag2", "tag3", "tag4", "tag5", "tag6",
    "tag_light", "tag_structure", "tag_spread", "tag_risk", "tag_certificate", "tag_commercial", "certificate_flags",
    "interpretation_short_ru", "interpretation_detail_ru", "recommendation_ru", "warning_ru", "disclaimer_ru",
    "KURGIN Import ID", "KURGIN Report ID", "PDF Report Status", "PDF Report File", "PDF Report URL", "PDF Generation Mode",
    "platform_import_status", "recommended_pdf_priority",
    "Report Template Version", "Formula Output Version", "Engine Version",
    "Upload Quality Status", "Geometry Status", "Missing Geometry Fields", "Possible Scale Issues", "Column Recognition Status",
    "Calculation Status", "Validation Errors",
    "spread_score", "spread_status", "diameter_symmetry_score", "diameter_symmetry_status", "roundness_status", "commercial_view", "value_score",
    "Breakdown",
]

ISSUES_COLUMNS = [
    "Issue Type", "Stock #", "Report #", "Lab", "Shape", "Weight", "Color", "Clarity",
    "Calculation Status", "Problem", "Validation Errors", "Missing Fields",
    "Measurement Parse Status", "Measurement Source", "Measurement Warning", "Measurement Conflict", "Chosen Measurement Source",
    "Upload Quality Status", "Geometry Status", "Missing Geometry Fields", "Possible Scale Issues",
    "Data Completeness %", "Report Quality Status", "platform_import_status",
    "Diameter Policy Status", "Diameter Policy Action", "Diameter Policy Reason", "High Score Diameter Flag",
    "recommendation_ru", "PDF Report Status",
]

SUMMARY_COLUMNS = ["Metric", "Value", "Comment"]



def _empty_result(verdict, status, breakdown, engine_version=None):
    return pd.Series({
        "Engine Version": engine_version,
        "Kurgin Score": None,
        "Verdict": verdict,
        "Triple Score": None,
        "Structure Modifier": None,
        "Visual Check": None,
        "Critical Risk": None,
        "Tags": "",
        "Breakdown": breakdown,
        "Nailhead": None,
        "Fisheye": None,
        "Fire Loss": None,
        "Depth Dev": None,
        "Crown Dev": None,
        "Pavilion Dev": None,
        "Balance Err": None,
        "Girdle Penalty": None,
        "Validation Errors": "",
        "Calculation Status": status
    })


def _empty_value(value):
    if value is None:
        return True
    text = str(value).strip()
    return text == "" or text.lower() in {"nan", "none", "—", "-"}


def _missing_required_values(row):
    return [col for col in REQUIRED_COLUMNS if _empty_value(row.get(col))]


def analyze_row(row, language="RU"):
    try:
        shape = str(row.get("Shape", "ROUND")).upper()
        if shape != "ROUND":
            return _empty_result(
                verdict="IN DEVELOPMENT",
                status="UNSUPPORTED_SHAPE",
                breakdown=f"""
Shape: {shape}

{UNSUPPORTED_SHAPE_MESSAGE.get(language, UNSUPPORTED_SHAPE_MESSAGE['EN'])}
"""
            )
        missing_values = _missing_required_values(row)
        if len(missing_values) == len(REQUIRED_COLUMNS):
            result = _empty_result(
                "ERROR",
                "CATALOG_DATA_ONLY",
                "Missing all required geometry fields: " + ", ".join(missing_values)
            )
            result["Validation Errors"] = "Missing all required geometry fields: " + ", ".join(missing_values)
            return result

        if missing_values:
            result = _empty_result(
                "ERROR",
                "MISSING_GEOMETRY",
                "Missing required geometry fields: " + ", ".join(missing_values)
            )
            result["Validation Errors"] = "Missing required geometry fields: " + ", ".join(missing_values)
            return result

        possible_scale = str(row.get("Possible Scale Issues", "") or "").strip()
        if possible_scale:
            result = _empty_result(
                "ERROR",
                "POSSIBLE_SCALE_ISSUE",
                possible_scale
            )
            result["Validation Errors"] = possible_scale
            return result

        validation_errors = validate_row(row)
        if validation_errors:
            result = _empty_result("ERROR", "VALIDATION_ERROR", "\n".join(validation_errors))
            result["Validation Errors"] = "; ".join(validation_errors)
            return result
        stone = StoneInput.from_row(row)
        result = calculate_stone(stone.to_engine_kwargs())
        return pd.Series({
            "Engine Version": result["engine_version"],
            "Kurgin Score": result["final_score"],
            "Verdict": result["final_verdict"],
            "Triple Score": result["triple_score"],
            "Structure Modifier": result["structure_modifier"],
            "Visual Check": result["visual_check"],
            "Critical Risk": result["critical_risk"],
            "Tags": ", ".join(result["structure_tags"]),
            "Breakdown": result["breakdown"],
            "Nailhead": result["diagnostics"]["nailhead"],
            "Fisheye": result["diagnostics"]["fisheye"],
            "Fire Loss": result["diagnostics"]["fire_loss"],
            "Depth Dev": result["diagnostics"]["depth_dev"],
            "Crown Dev": result["diagnostics"]["crown_dev"],
            "Pavilion Dev": result["diagnostics"]["pavilion_dev"],
            "Balance Err": result["diagnostics"]["balance_err"],
            "Girdle Penalty": result["diagnostics"]["girdle_penalty"],
            "Validation Errors": "",
            "Calculation Status": "OK"
        })
    except Exception as e:
        return _empty_result("ERROR", str(e), str(e))


def localize_dataframe(df, language):
    df = df.copy()
    df["Verdict Local"] = df["Verdict"].apply(lambda x: translate_verdict(x, language))
    df["Tags Local"] = df["Tags"].apply(lambda x: translate_tags(x, language))
    df = add_interpretation_columns(df, language=language)
    # Ensure tag columns always exist, even if no tags were generated.
    for col in TAG_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    if "tags_all" not in df.columns:
        df["tags_all"] = ""
    return df


def _safe_file_token(value):
    text = str(value or "").strip()
    if not text or text.lower() in {"nan", "none", "—", "-"}:
        return ""
    text = re.sub(r"[^A-Za-z0-9А-Яа-я_-]+", "_", text)
    text = text.strip("_")
    return text[:80]


def _report_id_for_row(row, index=None):
    report = _safe_file_token(row.get("Report #", ""))
    stock = _safe_file_token(row.get("Stock #", ""))
    if report:
        return report
    if stock:
        return stock
    if index is not None:
        return f"row_{index + 1}"
    return "manual"


def add_pdf_report_columns(df, base_dir="reports"):
    df = df.copy()
    report_ids = []
    statuses = []
    files = []
    urls = []
    versions = []

    for index, row in df.iterrows():
        report_id = _report_id_for_row(row, index=index)
        status = str(row.get("Calculation Status", ""))
        if status == "OK":
            pdf_status = "ready_to_generate"
            pdf_file = f"{base_dir}/{report_id}_KURGIN_Report.pdf"
        elif status == "UNSUPPORTED_SHAPE":
            pdf_status = "not_available_unsupported_shape"
            pdf_file = ""
        elif status == "CATALOG_DATA_ONLY":
            pdf_status = "not_available_catalog_data_only"
            pdf_file = ""
        elif status == "MISSING_GEOMETRY":
            pdf_status = "not_available_missing_geometry"
            pdf_file = ""
        elif status == "POSSIBLE_SCALE_ISSUE":
            pdf_status = "not_available_possible_scale_issue"
            pdf_file = ""
        else:
            pdf_status = "not_available_validation_or_error"
            pdf_file = ""

        report_ids.append(report_id)
        statuses.append(pdf_status)
        files.append(pdf_file)
        urls.append("")
        versions.append(REPORT_TEMPLATE_VERSION)

    df["KURGIN Report ID"] = report_ids
    df["PDF Report Status"] = statuses
    df["PDF Report File"] = files
    df["PDF Report URL"] = urls
    df["Report Template Version"] = versions
    return df


def _not_empty_value(value):
    if value is None:
        return False
    text = str(value).strip()
    return text != "" and text.lower() not in {"nan", "none", "—", "-"}


def _data_completeness(row):
    fields = [
        "Report #", "Lab", "Shape", "Weight", "Color", "Clarity",
        "Cut", "Polish", "Symmetry", "Fluorescence", "Fluorescence Intensity",
        "Measurements", "DepthPercent", "TablePercent", "CrownPercent",
        "CrownAngle", "PavilionPercent", "PavilionAngle", "GirdlePercent",
        "GirdleThin", "GirdleThick", "CuletSize",
    ]
    present = sum(1 for field in fields if _not_empty_value(row.get(field)))
    return round((present / len(fields)) * 100, 1)


def _geometry_complete(row):
    fields = [
        "DepthPercent", "TablePercent", "CrownPercent", "CrownAngle",
        "PavilionPercent", "PavilionAngle", "GirdlePercent"
    ]
    return all(_not_empty_value(row.get(field)) for field in fields)


def _report_quality_status(row):
    status = str(row.get("Calculation Status", ""))
    completeness = _data_completeness(row)

    if status == "UNSUPPORTED_SHAPE":
        return "Unsupported Shape"
    if status == "CATALOG_DATA_ONLY":
        return "Catalog Data Only"
    if status == "MISSING_GEOMETRY":
        return "Missing Geometry"
    if status == "POSSIBLE_SCALE_ISSUE":
        return "Possible Scale Issue"
    if status != "OK":
        return "Validation Warning"

    if completeness >= 80:
        return "Complete"
    if _geometry_complete(row) and completeness < 55:
        return "Geometry Only"
    if completeness >= 55:
        return "Partial Data"
    return "Limited Data"


def _certificate_flags(row):
    flags = []

    fluor = " ".join([
        str(row.get("Fluorescence", "")),
        str(row.get("Fluorescence Intensity", "")),
        str(row.get("Fluorescence Color", "")),
    ]).lower()
    if "strong" in fluor:
        flags.append("Strong Fluorescence")
    elif "medium" in fluor:
        flags.append("Medium Fluorescence")

    for field, label in [
        ("Milky", "Milky Check"),
        ("Shade", "Shade Check"),
        ("Black Inclusion", "Black Inclusion Note"),
        ("Open Inclusion", "Open Inclusion Note"),
        ("White Inclusion", "White Inclusion Note"),
        ("Inscription", "Inscription Available"),
        ("Cert comment", "Certificate Comment Available"),
    ]:
        if _not_empty_value(row.get(field)):
            flags.append(label)

    growth = str(row.get("Growth Method", "")).upper()
    if "CVD" in growth:
        flags.append("CVD Growth")
    if "HPHT" in growth:
        flags.append("HPHT Growth")

    dtype = str(row.get("Diamond Type", ""))
    if dtype:
        flags.append(dtype)

    return "; ".join(dict.fromkeys(flags))


def _tag_categories(row):
    tags = [tag.strip() for tag in str(row.get("Tags", "")).split(",") if tag.strip()]
    tags_lower = [tag.lower() for tag in tags]
    result = {
        "tag_light": "",
        "tag_structure": "",
        "tag_spread": "",
        "tag_risk": "",
        "tag_certificate": "",
        "tag_commercial": "",
    }

    if "low fire" in tags_lower:
        result["tag_light"] = "Low Fire"

    structure_tags = [tag for tag in tags if tag in {"Perfect Build", "Hidden Weight"}]
    if structure_tags:
        result["tag_structure"] = "; ".join(structure_tags)

    risk_tags = [tag for tag in tags if tag in {"Nailhead Risk", "Fisheye Risk"}]
    if bool(row.get("Visual Check", False)):
        risk_tags.append("Visual Check")
    if bool(row.get("Critical Risk", False)):
        risk_tags.append("Critical Risk")
    if risk_tags:
        result["tag_risk"] = "; ".join(dict.fromkeys(risk_tags))

    spread_status = str(row.get("VisualSpreadStatus", ""))
    roundness = str(row.get("DiameterSymmetryStatus", "")) or _roundness_status(row)
    spread_parts = []
    if spread_status and spread_status != "Not calculated":
        spread_parts.append(spread_status)
    if roundness and roundness != "Not calculated":
        spread_parts.append(f"Roundness: {roundness}")
    if spread_parts:
        result["tag_spread"] = "; ".join(spread_parts)

    cert_flags = _certificate_flags(row)
    if cert_flags:
        result["tag_certificate"] = cert_flags

    band = str(row.get("score_band", ""))
    if band in {"standard", "fair", "poor", "rejected"}:
        result["tag_commercial"] = band.replace("_", " ").title()

    return result


def _roundness_status(row):
    try:
        value = float(row.get("RoundnessDeviation"))
    except Exception:
        return "Not calculated"

    if value <= 0.50:
        return "Excellent Roundness"
    if value <= 1.00:
        return "Good Roundness"
    return "Roundness Check"


def _diameter_symmetry_score(row):
    try:
        value = float(row.get("RoundnessDeviation"))
    except Exception:
        return "Not calculated"

    # Display score only. It is not part of the core KURGIN Score yet.
    score = max(0, min(100, 100 - value * 25))
    return round(score, 2)


def _platform_import_status(row):
    status = str(row.get("Calculation Status", ""))
    if status == "UNSUPPORTED_SHAPE":
        return "unsupported_shape"
    if status == "CATALOG_DATA_ONLY":
        return "catalog_data_only"
    if status == "MISSING_GEOMETRY":
        return "missing_geometry"
    if status == "POSSIBLE_SCALE_ISSUE":
        return "possible_scale_issue"
    if status != "OK":
        return "validation_error"

    quality = str(row.get("Report Quality Status", ""))
    measurement_status = str(row.get("Measurement Parse Status", ""))

    if quality in {"Geometry Only", "Limited Data"}:
        return "ready_for_score_needs_review"
    if measurement_status in {"Missing", "Failed"}:
        return "ready_for_score_measurements_missing"
    return "ready_for_catalog_and_pdf"


def _recommended_pdf_priority(row):
    status = str(row.get("Calculation Status", ""))
    if status != "OK":
        return "not_available"

    try:
        score = float(row.get("Kurgin Score"))
    except Exception:
        score = None

    critical = bool(row.get("Critical Risk", False))
    visual = bool(row.get("Visual Check", False))

    if critical:
        return "review"
    if score is not None and score >= 95 and not visual:
        return "high"
    if score is not None and score >= 90:
        return "medium"
    if visual:
        return "review"
    return "low"


def add_platform_import_columns(df):
    df = df.copy()

    import_ids = []
    completeness_values = []
    quality_statuses = []
    pdf_modes = []
    platform_statuses = []
    pdf_priorities = []
    tag_light = []
    tag_structure = []
    tag_spread = []
    tag_risk = []
    tag_certificate = []
    tag_commercial = []
    certificate_flags = []
    roundness_statuses = []
    diameter_scores = []
    diameter_statuses = []

    for index, row in df.iterrows():
        report_id = str(row.get("KURGIN Report ID", "")).strip() or _report_id_for_row(row, index=index)
        import_ids.append(f"KRG-{report_id}")

        completeness = _data_completeness(row)
        completeness_values.append(completeness)
        quality_statuses.append(_report_quality_status(row))

        status = str(row.get("Calculation Status", ""))
        pdf_modes.append("on_demand" if status == "OK" else "not_available")
        platform_statuses.append(_platform_import_status(row))
        pdf_priorities.append(_recommended_pdf_priority(row))

        cats = _tag_categories(row)
        tag_light.append(cats["tag_light"])
        tag_structure.append(cats["tag_structure"])
        tag_spread.append(cats["tag_spread"])
        tag_risk.append(cats["tag_risk"])
        tag_certificate.append(cats["tag_certificate"])
        tag_commercial.append(cats["tag_commercial"])
        certificate_flags.append(_certificate_flags(row))

        round_status = row.get("DiameterSymmetryStatus") or _roundness_status(row)
        roundness_statuses.append(round_status)
        diameter_scores.append(row.get("DiameterSymmetryScore") if row.get("DiameterSymmetryScore") not in [None, ""] else _diameter_symmetry_score(row))
        diameter_statuses.append(round_status)

    df["KURGIN Import ID"] = import_ids
    df["Formula Output Version"] = FORMULA_OUTPUT_VERSION
    df["Data Completeness %"] = completeness_values
    df["Report Quality Status"] = quality_statuses
    df["PDF Generation Mode"] = pdf_modes
    df["platform_import_status"] = platform_statuses
    df["recommended_pdf_priority"] = pdf_priorities
    df["tag_light"] = tag_light
    df["tag_structure"] = tag_structure
    df["tag_spread"] = tag_spread
    df["tag_risk"] = tag_risk
    df["tag_certificate"] = tag_certificate
    df["tag_commercial"] = tag_commercial
    df["certificate_flags"] = certificate_flags
    df["spread_score"] = df.get("SpreadDelta %", "Not calculated")
    df["spread_status"] = df.get("VisualSpreadStatus", "Not calculated")
    df["diameter_symmetry_score"] = diameter_scores
    df["diameter_symmetry_status"] = diameter_statuses
    df["roundness_status"] = roundness_statuses
    df["commercial_view"] = "Not calculated"
    df["value_score"] = "Not calculated"
    return df


def process_dataframe(df, language="RU"):
    df, mapping_df = apply_column_mapping(df)
    df = enrich_dataframe_fields(df)
    missing_columns = get_missing_columns(df)
    for column in missing_columns:
        df[column] = None
    df = add_upload_quality_columns(df, mapping_df=mapping_df)
    df_result = df.apply(lambda row: analyze_row(row, language=language), axis=1)
    df = pd.concat([df, df_result], axis=1)
    if ID_COLUMN not in df.columns:
        df[ID_COLUMN] = df.index + 1
    df = localize_dataframe(df, language)
    df = add_pdf_report_columns(df)
    df = add_measurement_spread_columns(df)
    df = add_diameter_policy_columns(df)
    df = add_platform_import_columns(df)
    return df, [], mapping_df


def make_analytics(df):
    ok_df = df[df["Calculation Status"] == "OK"].copy()
    total = len(df)
    successful = len(ok_df)
    errors = total - successful
    avg_score = ok_df["Kurgin Score"].mean()
    verdict_col = "Verdict Local" if "Verdict Local" in df.columns else "Verdict"
    verdict_counts = df[verdict_col].value_counts().reset_index()
    verdict_counts.columns = ["Verdict", "Count"]
    bins = [0, 50, 70, 80, 90, 95, 98.5, 100]
    labels = ["Rejected", "Poor", "Fair", "Standard", "High", "Premium", "Elite"]
    ok_df["Score Range"] = pd.cut(ok_df["Kurgin Score"], bins=bins, labels=labels, include_lowest=True)
    score_ranges = ok_df["Score Range"].value_counts().sort_index().reset_index()
    score_ranges.columns = ["Score Range", "Count"]
    top_10 = ok_df.sort_values("Kurgin Score", ascending=False).head(10)
    worst_10 = ok_df.sort_values("Kurgin Score", ascending=True).head(10)
    risk_df = df[(df["Critical Risk"] == True) | (df["Visual Check"] == True) | (df["Tags"].astype(str).str.len() > 0)]
    critical_df = df[df["Critical Risk"] == True]
    unsupported_df = df[df["Calculation Status"] == "UNSUPPORTED_SHAPE"].copy()
    errors_df = df[(df["Calculation Status"] != "OK") & (df["Calculation Status"] != "UNSUPPORTED_SHAPE")].copy()
    return {
        "ok_df": ok_df,
        "total": total,
        "successful": successful,
        "errors": errors,
        "avg_score": avg_score,
        "verdict_counts": verdict_counts,
        "score_ranges": score_ranges,
        "top_10": top_10,
        "worst_10": worst_10,
        "risk_df": risk_df,
        "critical_df": critical_df,
        "unsupported_df": unsupported_df,
        "errors_df": errors_df,
    }


def _existing_columns(df, columns):
    cols = []
    seen = set()
    for col in columns:
        if col in df.columns and col not in seen:
            cols.append(col)
            seen.add(col)
    return cols


def _select_columns(df, columns):
    cols = _existing_columns(df, columns)
    return df[cols].copy() if cols else pd.DataFrame()


def _summary_dataframe(df, analytics, report_level):
    top_count = int((analytics["ok_df"]["Kurgin Score"] >= 95).sum()) if len(analytics["ok_df"]) else 0
    high_count = int(((analytics["ok_df"]["Kurgin Score"] >= 90) & (analytics["ok_df"]["Kurgin Score"] < 95)).sum()) if len(analytics["ok_df"]) else 0
    risk_count = len(analytics.get("risk_df", pd.DataFrame()))
    unsupported_count = len(analytics.get("unsupported_df", pd.DataFrame()))
    validation_count = len(analytics.get("errors_df", pd.DataFrame()))
    pdf_ready_count = int((df.get("PDF Report Status", pd.Series(dtype=str)) == "ready_to_generate").sum()) if "PDF Report Status" in df.columns else 0
    complete_count = int((df.get("Report Quality Status", pd.Series(dtype=str)) == "Complete").sum()) if "Report Quality Status" in df.columns else 0
    import_ready_count = int((df.get("Calculation Status", pd.Series(dtype=str)) == "OK").sum()) if "Calculation Status" in df.columns else 0

    rows = [
        ("Total Stones", analytics["total"], "Всего строк в файле"),
        ("Calculated", analytics["successful"], "Успешно рассчитано"),
        ("Unsupported Shapes", unsupported_count, "Огранки в разработке"),
        ("Validation / Errors", validation_count, "Ошибки данных или расчёта"),
        ("Average KURGIN Score", round(float(analytics["avg_score"]), 2) if pd.notna(analytics["avg_score"]) else "—", "Средний показатель по рассчитанным камням"),
        ("TOP Stones 95+", top_count, "Камни 95+"),
        ("HIGH Stones 90-94", high_count, "Камни 90-94"),
        ("Risk Stones", risk_count, "Есть теги, Visual Check или Critical Risk"),
        ("PDF Reports Ready", pdf_ready_count, "PDF можно создать для рассчитанных OK-камней"),
        ("Import Ready Stones", import_ready_count, "Строки, готовые для импорта в платформу KURGIN"),
        ("Complete Data Rows", complete_count, "Строки с высоким уровнем полноты данных"),
        ("Report Template Version", REPORT_TEMPLATE_VERSION, "Версия шаблона PDF отчёта"),
        ("Formula Output Version", FORMULA_OUTPUT_VERSION, "Версия стандарта Excel/выдачи"),
        ("Engine Version", ENGINE_VERSION, "Версия расчётного ядра"),
        ("Formula Mode", get_formula_mode(), "local / cloud / cloud_fallback"),
        ("Supported Shapes", ", ".join(SUPPORTED_SHAPES), "Огранки, доступные для расчёта"),
        ("Report Level", report_level, "Уровень выгрузки"),
        ("Generated UTC", datetime.utcnow().isoformat(timespec="seconds"), "Дата формирования файла"),
    ]
    return pd.DataFrame(rows, columns=["Metric", "Value", "Comment"])


def _formula_version_dataframe():
    rows = [
        ("Engine Name", "KURGIN Round Engine"),
        ("Engine Version", ENGINE_VERSION),
        ("Formula Mode", get_formula_mode()),
        ("Supported Shape", ", ".join(SUPPORTED_SHAPES)),
        ("Score Type", "Optical / Geometry / Structure"),
        ("Color Included In Score", "No"),
        ("Clarity Included In Score", "No"),
        ("Fluorescence Included In Score", "No"),
        ("Price Included In Score", "No"),
        ("Tag Columns", "tag1, tag2, tag3, tag4, tag5, tag6"),
        ("PDF Report Columns", "KURGIN Report ID, PDF Report Status, PDF Report File, PDF Report URL"),
        ("Report Template Version", REPORT_TEMPLATE_VERSION),
        ("Formula Output Version", FORMULA_OUTPUT_VERSION),
        ("Unified Report Schema", REPORT_SCHEMA_VERSION),
        ("Platform Import Columns", "KURGIN Import ID, Data Completeness %, Report Quality Status, PDF Generation Mode"),
        ("Future Module Columns", "spread_score, diameter_symmetry_score, certificate_flags, commercial_view, value_score"),
        ("Interpretation Columns", "interpretation_short_ru, interpretation_detail_ru, recommendation_ru, warning_ru"),
    ]
    return pd.DataFrame(rows, columns=["Parameter", "Value"])


def _import_ready_dataframe(df):
    columns = [
        "KURGIN Import ID", "Stock #", "Availability", "Report #", "Lab",
        "Shape", "Weight", "Color", "Clarity", "Cut", "Polish", "Symmetry",
        "Fluorescence", "Fluorescence Intensity", "Fluorescence Color", "Measurements",
        "Location", "Country", "State", "City",
        "price_rub", "price_usd", "supplier",
        "Kurgin Score", "Verdict Local", "score_band_label_ru",
        "tags_all", "tag1", "tag2", "tag3", "tag4", "tag5", "tag6",
        "tag_light", "tag_structure", "tag_spread", "tag_risk", "tag_certificate", "tag_commercial",
        "interpretation_short_ru", "recommendation_ru", "warning_ru",
        "Data Completeness %", "Report Quality Status",
        "KURGIN Report ID", "PDF Report Status", "PDF Report File", "PDF Report URL",
        "PDF Generation Mode", "Report Template Version", "Formula Output Version",
        "Engine Version", "Calculation Status", "Validation Errors",
    ]
    return _select_columns(df, columns)


def _data_dictionary_dataframe():
    return pd.DataFrame(
        DATA_DICTIONARY_ROWS,
        columns=["Column", "Meaning", "Used In Score", "Used In PDF", "Used For Import", "Notes"]
    )


def _unified_report_dataframe(df):
    cols = select_existing(df, UNIFIED_REPORT_COLUMNS)
    return df[cols].copy() if cols else pd.DataFrame()


def _kurgin_card_dataframe(df):
    cols = select_existing(df, KURGIN_CARD_COLUMNS)
    return df[cols].copy() if cols else pd.DataFrame()


def _schema_sections_dataframe():
    rows = []
    for section, columns in SECTION_ORDER:
        for order, column in enumerate(columns, start=1):
            rows.append({
                "Section": section,
                "Order": order,
                "Column": column,
            })
    return pd.DataFrame(rows)



def _write_sheet(writer, sheet_name, df, widths=None, freeze=True, pdf_links=False):
    if df is None:
        df = pd.DataFrame()
    if df.empty:
        df = pd.DataFrame({"Message": ["No data"]})

    df.to_excel(writer, index=False, sheet_name=sheet_name)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    header_format = workbook.add_format({
        "bold": True,
        "bg_color": "#0B1220",
        "font_color": "#FFFFFF",
        "border": 1,
        "align": "center",
        "valign": "vcenter",
    })
    body_format = workbook.add_format({
        "border": 1,
        "valign": "top",
        "text_wrap": True,
    })
    score_format = workbook.add_format({
        "border": 1,
        "num_format": "0.00",
        "valign": "top",
    })
    link_format = workbook.add_format({
        "border": 1,
        "valign": "top",
        "text_wrap": True,
        "font_color": "#2563EB",
        "underline": True,
    })

    for col_idx, col in enumerate(df.columns):
        worksheet.write(0, col_idx, col, header_format)
        series = df[col].astype(str).fillna("")
        max_len = max([len(str(col))] + [len(x) for x in series.head(500).tolist()])
        width = min(max(max_len + 2, 10), 42)
        if widths and col in widths:
            width = widths[col]
        fmt = score_format if col in ["Kurgin Score", "Triple Score", "Structure Modifier"] else body_format
        worksheet.set_column(col_idx, col_idx, width, fmt)

    if pdf_links and "PDF Report File" in df.columns:
        pdf_col = df.columns.get_loc("PDF Report File")
        for row_idx, value in enumerate(df["PDF Report File"].fillna("").astype(str).tolist(), start=1):
            if value.strip():
                worksheet.write_url(row_idx, pdf_col, "external:" + value, link_format, string="Open PDF")
            else:
                worksheet.write(row_idx, pdf_col, "Not available", body_format)

    if freeze:
        worksheet.freeze_panes(1, 0)
    worksheet.autofilter(0, 0, max(len(df), 1), max(len(df.columns) - 1, 0))

    # Conditional formatting for score columns
    if "Kurgin Score" in df.columns and len(df) > 0:
        score_col = df.columns.get_loc("Kurgin Score")
        first = 1
        last = len(df)
        worksheet.conditional_format(first, score_col, last, score_col, {
            "type": "3_color_scale",
            "min_color": "#FCA5A5",
            "mid_color": "#FDE68A",
            "max_color": "#86EFAC",
        })


def _ok_rows(df):
    if "Calculation Status" not in df.columns:
        return df.copy()
    return df[df["Calculation Status"] == "OK"].copy()


def _results_dataframe(df):
    return _select_columns(_ok_rows(df), RESULTS_COLUMNS)


def _details_dataframe(df):
    ok_df = _ok_rows(df)
    detail_df = _select_columns(ok_df, DETAILS_COLUMNS)
    return detail_df if not detail_df.empty else ok_df.copy()


def _missing_formula_fields(row):
    required = [
        "CrownAngle", "PavilionAngle", "TablePercent", "DepthPercent",
        "CrownPercent", "PavilionPercent", "GirdlePercent"
    ]
    missing = []
    for field in required:
        value = row.get(field)
        if value is None or str(value).strip() == "" or str(value).lower() in {"nan", "none", "—", "-"}:
            missing.append(field)
    return ", ".join(missing)


def _issue_recommendation(issue_type):
    if issue_type == "UNSUPPORTED_SHAPE":
        return "Огранка пока не поддерживается текущей моделью KURGIN Score."
    if issue_type == "VALIDATION_ERROR":
        return "Проверьте обязательные геометрические параметры и формат чисел."
    if issue_type == "MISSING_GEOMETRY":
        return "Добавьте отсутствующие геометрические параметры сертификата."
    if issue_type == "CATALOG_DATA_ONLY":
        return "Файл можно использовать для каталога, но для Score нужны углы и пропорции."
    if issue_type == "POSSIBLE_SCALE_ISSUE":
        return "Проверьте масштаб числа: возможно, 345 должно быть 34.5."
    if issue_type == "MEASUREMENT_MISSING":
        return "Добавьте Measurements или Length/Width/Height, если нужен анализ размеров."
    if issue_type == "MEASUREMENT_PARSE_FAILED":
        return "Проверьте формат размеров, например 6.360x6.400x3.970."
    if issue_type == "LIMITED_DATA":
        return "Добавьте сертификатные данные для более полного отчёта."
    if issue_type == "HIGH_SCORE_DIAMETER_REVIEW":
        return "Проверьте, должен ли высокий публичный класс сохраняться с учётом diameter/spread."
    return "Проверьте исходные данные."


def _issues_dataframe(df):
    if df.empty:
        return pd.DataFrame(columns=ISSUES_COLUMNS)

    rows = []
    for _, row in df.iterrows():
        status = str(row.get("Calculation Status", ""))
        measurement_status = str(row.get("Measurement Parse Status", ""))
        quality = str(row.get("Report Quality Status", ""))

        issue_types = []

        if status != "OK":
            if status == "UNSUPPORTED_SHAPE":
                issue_types.append("UNSUPPORTED_SHAPE")
            elif status == "VALIDATION_ERROR":
                issue_types.append("VALIDATION_ERROR")
            elif status == "MISSING_GEOMETRY":
                issue_types.append("MISSING_GEOMETRY")
            elif status == "CATALOG_DATA_ONLY":
                issue_types.append("CATALOG_DATA_ONLY")
            elif status == "POSSIBLE_SCALE_ISSUE":
                issue_types.append("POSSIBLE_SCALE_ISSUE")
            else:
                issue_types.append(status or "ERROR")

        if measurement_status == "Missing":
            issue_types.append("MEASUREMENT_MISSING")
        elif measurement_status == "Failed":
            issue_types.append("MEASUREMENT_PARSE_FAILED")

        if status == "OK" and quality in {"Geometry Only", "Limited Data"}:
            issue_types.append("LIMITED_DATA")

        if row.get("High Score Diameter Flag") is True:
            issue_types.append("HIGH_SCORE_DIAMETER_REVIEW")

        for issue_type in dict.fromkeys(issue_types):
            problem = ""
            if issue_type in {"VALIDATION_ERROR", "ERROR"} or status not in {"OK", "UNSUPPORTED_SHAPE"}:
                problem = str(row.get("Validation Errors") or row.get("Breakdown") or status)
            elif issue_type == "UNSUPPORTED_SHAPE":
                problem = f"Shape {row.get('Shape', '')} is not supported by current ROUND model"
            elif issue_type == "MISSING_GEOMETRY":
                problem = "Missing required geometry fields: " + str(row.get("Missing Geometry Fields", ""))
            elif issue_type == "CATALOG_DATA_ONLY":
                problem = "No required geometry fields available for KURGIN Score"
            elif issue_type == "POSSIBLE_SCALE_ISSUE":
                problem = str(row.get("Possible Scale Issues", ""))
            elif issue_type.startswith("MEASUREMENT"):
                problem = str(row.get("Measurement Warning", ""))
            elif issue_type == "LIMITED_DATA":
                problem = f"Report Quality Status: {quality}"
            elif issue_type == "HIGH_SCORE_DIAMETER_REVIEW":
                problem = str(row.get("Diameter Policy Reason", ""))

            rows.append({
                "Issue Type": issue_type,
                "Stock #": row.get("Stock #", ""),
                "Report #": row.get("Report #", ""),
                "Lab": row.get("Lab", ""),
                "Shape": row.get("Shape", ""),
                "Weight": row.get("Weight", ""),
                "Color": row.get("Color", ""),
                "Clarity": row.get("Clarity", ""),
                "Calculation Status": status,
                "Problem": problem,
                "Validation Errors": row.get("Validation Errors", ""),
                "Missing Fields": _missing_formula_fields(row),
                "Measurement Parse Status": row.get("Measurement Parse Status", ""),
                "Measurement Source": row.get("Measurement Source", ""),
                "Measurement Warning": row.get("Measurement Warning", ""),
                "Measurement Conflict": row.get("Measurement Conflict", ""),
                "Chosen Measurement Source": row.get("Chosen Measurement Source", ""),
                "Upload Quality Status": row.get("Upload Quality Status", ""),
                "Geometry Status": row.get("Geometry Status", ""),
                "Missing Geometry Fields": row.get("Missing Geometry Fields", ""),
                "Possible Scale Issues": row.get("Possible Scale Issues", ""),
                "Data Completeness %": row.get("Data Completeness %", ""),
                "Report Quality Status": quality,
                "platform_import_status": row.get("platform_import_status", ""),
                "Diameter Policy Status": row.get("Diameter Policy Status", ""),
                "Diameter Policy Action": row.get("Diameter Policy Action", ""),
                "Diameter Policy Reason": row.get("Diameter Policy Reason", ""),
                "High Score Diameter Flag": row.get("High Score Diameter Flag", ""),
                "recommendation_ru": _issue_recommendation(issue_type),
                "PDF Report Status": row.get("PDF Report Status", ""),
            })

    return pd.DataFrame(rows, columns=ISSUES_COLUMNS)


def _summary_compact_dataframe(df, analytics, report_level):
    ok_count = int((df.get("Calculation Status", pd.Series(dtype=str)) == "OK").sum()) if "Calculation Status" in df.columns else 0
    unsupported_count = int((df.get("Calculation Status", pd.Series(dtype=str)) == "UNSUPPORTED_SHAPE").sum()) if "Calculation Status" in df.columns else 0
    validation_count = int((df.get("Calculation Status", pd.Series(dtype=str)) == "VALIDATION_ERROR").sum()) if "Calculation Status" in df.columns else 0
    missing_geometry_count = int((df.get("Calculation Status", pd.Series(dtype=str)) == "MISSING_GEOMETRY").sum()) if "Calculation Status" in df.columns else 0
    catalog_only_count = int((df.get("Calculation Status", pd.Series(dtype=str)) == "CATALOG_DATA_ONLY").sum()) if "Calculation Status" in df.columns else 0
    scale_issue_count = int((df.get("Calculation Status", pd.Series(dtype=str)) == "POSSIBLE_SCALE_ISSUE").sum()) if "Calculation Status" in df.columns else 0
    error_count = len(df) - ok_count - unsupported_count - validation_count - missing_geometry_count - catalog_only_count - scale_issue_count
    pdf_ready = int((df.get("PDF Report Status", pd.Series(dtype=str)) == "ready_to_generate").sum()) if "PDF Report Status" in df.columns else 0
    measurement_missing = int((df.get("Measurement Parse Status", pd.Series(dtype=str)) == "Missing").sum()) if "Measurement Parse Status" in df.columns else 0
    measurement_failed = int((df.get("Measurement Parse Status", pd.Series(dtype=str)) == "Failed").sum()) if "Measurement Parse Status" in df.columns else 0
    hidden_weight_spread = int((df.get("VisualSpreadStatus", pd.Series(dtype=str)) == "Hidden Weight Risk").sum()) if "VisualSpreadStatus" in df.columns else 0
    wide_risky_spread = int((df.get("VisualSpreadStatus", pd.Series(dtype=str)) == "Wide but Risky").sum()) if "VisualSpreadStatus" in df.columns else 0
    high_score_diameter_flags = int((df.get("High Score Diameter Flag", pd.Series(dtype=bool)) == True).sum()) if "High Score Diameter Flag" in df.columns else 0
    class_review_count = int((df.get("Diameter Policy Status", pd.Series(dtype=str)) == "Class review").sum()) if "Diameter Policy Status" in df.columns else 0
    issues_count = len(_issues_dataframe(df))
    avg_score = analytics.get("avg_score")
    rows = [
        ("Total Stones", len(df), "Всего строк в загруженном файле"),
        ("Calculated OK", ok_count, "Камни, для которых рассчитан KURGIN Score"),
        ("Unsupported Shapes", unsupported_count, "Огранки, которые пока не поддерживаются"),
        ("Validation Errors", validation_count, "Строки с ошибками данных"),
        ("Missing Geometry", missing_geometry_count, "Нет части обязательных геометрических параметров"),
        ("Catalog Data Only", catalog_only_count, "Файл/строка пригодны для каталога, но не для KURGIN Score"),
        ("Possible Scale Issues", scale_issue_count, "Похоже, число записано в неверном масштабе"),
        ("Other Errors", error_count, "Прочие ошибки обработки"),
        ("Average KURGIN Score", round(avg_score, 2) if pd.notna(avg_score) else "—", "Средний score по OK-камням"),
        ("PDF Ready", pdf_ready, "Для этих камней можно создать PDF"),
        ("Report Level", report_level, "Запрошенный уровень отчёта"),
        ("Engine Version", ENGINE_VERSION, "Версия расчётного ядра"),
        ("Report Template Version", REPORT_TEMPLATE_VERSION, "Версия PDF-шаблона"),
        ("Formula Output Version", FORMULA_OUTPUT_VERSION, "Версия Excel/output стандарта"),
        ("Formula Mode", get_formula_mode(), "local / cloud / cloud_fallback"),
    ]
    return pd.DataFrame(rows, columns=SUMMARY_COLUMNS)


def _system_dataframe(df, analytics, mapping_df=None, report_level="Professional Report"):
    """Single technical/support sheet: summary + issues + mapping + versions.

    Keeps workbook compact without losing audit information.
    """
    rows = []

    def add(section, field, value="", detail=""):
        rows.append({
            "Section": section,
            "Field": field,
            "Value": value,
            "Detail": detail,
        })

    summary = _summary_compact_dataframe(df, analytics, report_level)
    for _, row in summary.iterrows():
        add("Summary", row.get("Metric", ""), row.get("Value", ""), row.get("Comment", ""))

    add("Versions", "Engine Version", ENGINE_VERSION, "Formula calculation engine")
    add("Versions", "Report Template Version", REPORT_TEMPLATE_VERSION, "PDF report template")
    add("Versions", "Formula Output Version", FORMULA_OUTPUT_VERSION, "Excel/output schema")
    add("Versions", "Formula Mode", get_formula_mode(), "local / cloud / cloud_fallback")
    add("Versions", "Supported Shapes", ", ".join(SUPPORTED_SHAPES), "Current formula scope")

    issues_df = _issues_dataframe(df)
    if not issues_df.empty:
        add("Issues", "See Issues sheet", len(issues_df), "All unsupported, validation and measurement issues are separated from Results")
    else:
        add("Issues", "No issues", "OK", "All rows calculated successfully")

    if mapping_df is not None and not mapping_df.empty:
        total_cols = len(mapping_df)
        mapped_cols = int((mapping_df["Status"].astype(str) != "not mapped").sum()) if "Status" in mapping_df.columns else 0
        add("Upload Recognition", "Columns recognized", f"{mapped_cols}/{total_cols}", "Mapped or already canonical columns")
        if "Confidence" in mapping_df.columns:
            avg_conf = round(float(mapping_df["Confidence"].mean()), 3)
            add("Upload Recognition", "Average mapping confidence", avg_conf, "1.0 means fully recognized")
        for _, row in mapping_df.iterrows():
            detail = row.get("Status", "")
            if "Confidence" in mapping_df.columns:
                detail = f"{detail}; confidence={row.get('Confidence', '')}; {row.get('Note', '')}"
            add("Column Mapping", row.get("Original Column", ""), row.get("Mapped To", ""), detail)

    # Compact dictionary only for key result fields, not every internal column.
    dictionary_rows = [
        ("Kurgin Score", "Main geometry/optics/structure score"),
        ("Verdict Local", "Localized final verdict"),
        ("tag1-tag6", "Generated tags for filtering and explanation"),
        ("Min/Max/Avg Diameter", "Parsed from Measurements or explicit size columns"),
        ("DepthMM", "Parsed physical height/depth in millimeters"),
        ("RoundnessDeviation", "Diameter deviation percentage; separate display module"),
        ("ExpectedDiameter", "Expected face-up diameter based on carat using 6.45 × carat^(1/3)"),
        ("SpreadDelta %", "Difference between AvgDiameter and ExpectedDiameter"),
        ("VisualSpreadStatus", "Good Spread / Small for Weight / Hidden Weight Risk / Wide but Risky"),
        ("DiameterSpreadModifierPreview", "Research-only preview modifier; official KURGIN Score is unchanged"),
        ("AdjustedKURGINScorePreview", "Preview score after measurement/spread module; not official"),
        ("Diameter Policy Status", "Research policy: confirms, warns or requests class review"),
        ("High Score Diameter Flag", "True when high score has diameter/spread issue"),
        ("Data Completeness %", "How complete the source data is"),
        ("Report Quality Status", "Complete / Partial Data / Geometry Only / Validation Warning"),
        ("PDF Report File", "Relative path to generated report in package"),
    ]
    for field, detail in dictionary_rows:
        add("Data Dictionary", field, "", detail)

    return pd.DataFrame(rows, columns=["Section", "Field", "Value", "Detail"])


def _build_export_frames(df, analytics, mapping_df=None, report_level="Professional Report"):
    df = add_pdf_report_columns(df)
    df = add_measurement_spread_columns(df)
    df = add_diameter_policy_columns(df)
    df = add_platform_import_columns(df)
    return {
        "Results": _results_dataframe(df),
        "Details": _details_dataframe(df),
        "Issues": _issues_dataframe(df),
        "System": _system_dataframe(df, analytics, mapping_df=mapping_df, report_level=report_level),
    }


def _write_export_workbook(output, frames, pdf_links=False):
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        _write_sheet(writer, "Results", frames["Results"], pdf_links=pdf_links)
        _write_sheet(writer, "Details", frames["Details"], pdf_links=pdf_links)
        _write_sheet(writer, "Issues", frames["Issues"], widths={"Issue Type": 24, "Problem": 52, "Recommendation": 52}, pdf_links=pdf_links)
        _write_sheet(writer, "System", frames["System"], widths={"Section": 18, "Field": 28, "Value": 32, "Detail": 70})

def create_excel_output(df, analytics, mapping_df=None, report_level="Professional Report"):
    """Create compact KURGIN Excel output.

    Sheet 1 (Results) contains the essential list of all stones and the same fields
    that form the PDF report. Other sheets are support/technical sheets only.
    """
    output = BytesIO()
    frames = _build_export_frames(df, analytics, mapping_df=mapping_df, report_level=report_level)
    _write_export_workbook(output, frames, pdf_links=False)
    return output.getvalue()


def create_analysis_package(df, analytics, mapping_df=None, report_level="Professional Report", pdf_mode="all_ok", max_pdfs=None):
    """Create ZIP package with compact Excel and PDF report per calculated OK stone."""
    package_buffer = BytesIO()
    df = add_pdf_report_columns(df)
    df = add_measurement_spread_columns(df)
    df = add_diameter_policy_columns(df)
    df = add_platform_import_columns(df)
    frames = _build_export_frames(df, analytics, mapping_df=mapping_df, report_level=report_level)

    excel_bytes = BytesIO()
    _write_export_workbook(excel_bytes, frames, pdf_links=True)

    with ZipFile(package_buffer, "w", ZIP_DEFLATED) as zf:
        zf.writestr("kurgin_score_result.xlsx", excel_bytes.getvalue())
        if pdf_mode == "top_only":
            ok_df = df[
                (df["Calculation Status"] == "OK")
                & (df["Kurgin Score"].astype(float) >= 95)
                & (df["Critical Risk"] != True)
            ].copy()
        elif pdf_mode == "none":
            ok_df = df.iloc[0:0].copy()
        else:
            ok_df = df[df["Calculation Status"] == "OK"].copy()

        if max_pdfs is not None:
            try:
                limit = int(max_pdfs)
            except (TypeError, ValueError):
                limit = None
            if limit is not None and limit >= 0:
                ok_df = ok_df.head(limit)

        for _, row in ok_df.iterrows():
            pdf_file = str(row.get("PDF Report File", "")).strip()
            if not pdf_file:
                continue
            try:
                pdf_bytes = create_single_stone_pdf(row, language="MULTI")
                zf.writestr(pdf_file, pdf_bytes)
            except Exception:
                continue
    return package_buffer.getvalue()


def process_single_stone(params):
    row = pd.Series(params)
    row = enrich_series_fields(row)
    row = add_upload_quality_columns(pd.DataFrame([row])).iloc[0]
    result = analyze_row(row, language=params.get("language", "RU"))
    output = pd.concat([row, result])
    df = pd.DataFrame([output])
    df = localize_dataframe(df, params.get("language", "RU"))
    df = add_pdf_report_columns(df)
    df = add_measurement_spread_columns(df)
    df = add_diameter_policy_columns(df)
    df = add_platform_import_columns(df)
    return df.iloc[0]
