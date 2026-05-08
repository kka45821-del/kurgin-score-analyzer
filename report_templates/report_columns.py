BASE_COLUMNS = [
    "Report #",
    "Shape",
    "Kurgin Score",
    "Verdict Local",
]

SHORT_COLUMNS = BASE_COLUMNS + [
    "Tags Local",
    "Visual Check",
    "Critical Risk",
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
]

FULL_COLUMNS = DETAILED_COLUMNS + [
    "Engine Version",
    "Breakdown",
    "Calculation Status",
    "Validation Errors",
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
