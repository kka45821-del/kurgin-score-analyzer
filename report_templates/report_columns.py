BASE_COLUMNS = [
    "Stone Title",
    "Identification Line",
    "Report #",
    "Lab",
    "Shape",
    "Weight",
    "Color",
    "Clarity",
    "Kurgin Score",
    "Verdict Local",
    "score_band_label_ru",
    "tags_all",
    "interpretation_short_ru",
]

SHORT_COLUMNS = BASE_COLUMNS + [
    "Tags Local",
    "Visual Check",
    "Critical Risk",
    "recommendation_ru",
    "warning_ru",
]

DETAILED_COLUMNS = SHORT_COLUMNS + [
    "Triple Score",
    "Structure Modifier",
    "Nailhead",
    "Fisheye",
    "Fire Loss",
    "Depth Dev",
    "Crown Dev",
    "Pavilion Dev",
    "Balance Err",
    "Girdle Penalty",
    "interpretation_detail_ru",
]

FULL_COLUMNS = DETAILED_COLUMNS + [
    "Stock #",
    "Availability",
    "Location",
    "Country",
    "State",
    "City",
    "Cut",
    "Polish",
    "Symmetry",
    "Fluorescence",
    "Fluorescence Intensity",
    "Fluorescence Color",
    "Measurements",
    "Treatment",
    "Growth Method",
    "Diamond Type",
    "Inscription",
    "Cert comment",
    "KeyToSymbols",
    "White Inclusion",
    "Black Inclusion",
    "Open Inclusion",
    "GirdleThin",
    "GirdleThick",
    "GirdleCondition",
    "CuletSize",
    "CuletCondition",
    "MinDiameter",
    "MaxDiameter",
    "AvgDiameter",
    "DepthMM",
    "DiameterDiff",
    "RoundnessDeviation",
    "Engine Version",
    "Breakdown",
    "Calculation Status",
    "Validation Errors",
    "score_band",
    "executive_summary_ru",
    "disclaimer_ru",
]

PROFESSIONAL_COLUMNS = None


def get_columns_for_level(level, df):
    if level == "Score Only":
        wanted = BASE_COLUMNS
    elif level == "Short Report":
        wanted = SHORT_COLUMNS
    elif level == "Detailed Report":
        wanted = DETAILED_COLUMNS
    elif level == "Full Report":
        wanted = FULL_COLUMNS
    elif level == "Professional Report":
        return list(df.columns)
    else:
        wanted = BASE_COLUMNS

    return [col for col in wanted if col in df.columns]


def filter_report_dataframe(df, level):
    cols = get_columns_for_level(level, df)
    return df[cols].copy()
