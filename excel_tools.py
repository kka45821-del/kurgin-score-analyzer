from io import BytesIO
import pandas as pd

from core_formula.main_engine import get_final_diamond_analysis
from data_models.stone import StoneInput
from excel_processing.column_mapping import apply_column_mapping
from platform_config.app_config import UNSUPPORTED_SHAPE_MESSAGE
from report_templates.report_columns import filter_report_dataframe
from translations_lang.label_translator import translate_verdict, translate_tags
from validation.input_validator import get_missing_columns, validate_row

ID_COLUMN = "Report #"

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
        validation_errors = validate_row(row)
        if validation_errors:
            result = _empty_result("ERROR", "VALIDATION_ERROR", "\n".join(validation_errors))
            result["Validation Errors"] = "; ".join(validation_errors)
            return result
        stone = StoneInput.from_row(row)
        result = get_final_diamond_analysis(**stone.to_engine_kwargs())
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
    return df

def process_dataframe(df, language="RU"):
    df, mapping_df = apply_column_mapping(df)
    missing_columns = get_missing_columns(df)
    if missing_columns:
        return df, missing_columns, mapping_df
    df_result = df.apply(lambda row: analyze_row(row, language=language), axis=1)
    df = pd.concat([df, df_result], axis=1)
    if ID_COLUMN not in df.columns:
        df[ID_COLUMN] = df.index + 1
    df = localize_dataframe(df, language)
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
    bins = [0, 80, 90, 95, 99, 100]
    labels = ["<80", "80-90", "90-95", "95-99", "99-100"]
    ok_df["Score Range"] = pd.cut(ok_df["Kurgin Score"], bins=bins, labels=labels, include_lowest=True)
    score_ranges = ok_df["Score Range"].value_counts().sort_index().reset_index()
    score_ranges.columns = ["Score Range", "Count"]
    top_10 = ok_df.sort_values("Kurgin Score", ascending=False).head(10)
    worst_10 = ok_df.sort_values("Kurgin Score", ascending=True).head(10)
    risk_df = df[(df["Critical Risk"] == True) | (df["Visual Check"] == True) | (df["Tags"].astype(str).str.len() > 0)]
    critical_df = df[df["Critical Risk"] == True]
    return {"ok_df": ok_df, "total": total, "successful": successful, "errors": errors, "avg_score": avg_score, "verdict_counts": verdict_counts, "score_ranges": score_ranges, "top_10": top_10, "worst_10": worst_10, "risk_df": risk_df, "critical_df": critical_df}

def create_excel_output(df, analytics, mapping_df=None, report_level="Professional Report"):
    output = BytesIO()
    report_df = filter_report_dataframe(df, report_level)
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        report_df.to_excel(writer, index=False, sheet_name="Report")
        df.to_excel(writer, index=False, sheet_name="All Data")
        analytics["top_10"].to_excel(writer, index=False, sheet_name="Top 10")
        analytics["worst_10"].to_excel(writer, index=False, sheet_name="Worst 10")
        analytics["risk_df"].to_excel(writer, index=False, sheet_name="Risks")
        analytics["verdict_counts"].to_excel(writer, index=False, sheet_name="Verdicts")
        analytics["score_ranges"].to_excel(writer, index=False, sheet_name="Score Ranges")
        if mapping_df is not None:
            mapping_df.to_excel(writer, index=False, sheet_name="Column Mapping")
    return output.getvalue()

def process_single_stone(params):
    row = pd.Series(params)
    result = analyze_row(row, language=params.get("language", "RU"))
    output = pd.concat([row, result])
    df = pd.DataFrame([output])
    return localize_dataframe(df, params.get("language", "RU")).iloc[0]
