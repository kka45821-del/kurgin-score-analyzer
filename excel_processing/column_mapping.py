import re
import pandas as pd

CANONICAL_COLUMNS = {
    "Report #": [
        "report #", "report", "report number", "certificate", "certificate number",
        "igi report", "gia report", "номер сертификата", "сертификат"
    ],
    "Shape": [
        "shape", "cut shape", "form", "форма", "огранка"
    ],
    "CrownAngle": [
        "crownangle", "crown angle", "crown ang", "crown_angle", "угол короны"
    ],
    "PavilionAngle": [
        "pavilionangle", "pavilion angle", "pavilion ang", "pavilion_angle", "угол павильона"
    ],
    "TablePercent": [
        "tablepercent", "table %", "table", "table percent", "table_pct", "площадка"
    ],
    "DepthPercent": [
        "depthpercent", "depth %", "depth", "depth percent", "depth_pct", "глубина"
    ],
    "CrownPercent": [
        "crownpercent", "crown %", "crown height %", "crown height", "crown_pct", "высота короны"
    ],
    "PavilionPercent": [
        "pavilionpercent", "pavilion %", "pavilion depth %", "pavilion depth", "pavilion_pct", "глубина павильона"
    ],
    "GirdlePercent": [
        "girdlepercent", "girdle %", "girdle", "girdle pct", "рундист"
    ],
}


def normalize_name(name):
    name = str(name).strip().lower()
    name = name.replace("\n", " ")
    name = re.sub(r"[_\-]+", " ", name)
    name = re.sub(r"\s+", " ", name)
    return name


def build_alias_map():
    alias_map = {}
    for canonical, aliases in CANONICAL_COLUMNS.items():
        alias_map[normalize_name(canonical)] = canonical
        for alias in aliases:
            alias_map[normalize_name(alias)] = canonical
    return alias_map


def apply_column_mapping(df):
    alias_map = build_alias_map()
    rename_map = {}
    mapping_rows = []

    for col in df.columns:
        normalized = normalize_name(col)
        canonical = alias_map.get(normalized)

        if canonical and canonical not in df.columns:
            rename_map[col] = canonical
            mapping_rows.append({
                "Original Column": col,
                "Mapped To": canonical,
                "Status": "mapped"
            })
        elif canonical and canonical == col:
            mapping_rows.append({
                "Original Column": col,
                "Mapped To": canonical,
                "Status": "already canonical"
            })
        else:
            mapping_rows.append({
                "Original Column": col,
                "Mapped To": "",
                "Status": "not mapped"
            })

    mapped_df = df.rename(columns=rename_map)
    mapping_df = pd.DataFrame(mapping_rows)
    return mapped_df, mapping_df
