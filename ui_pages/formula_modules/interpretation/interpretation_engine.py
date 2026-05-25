from formula_modules.tags.tag_registry import TAG_REGISTRY
from .report_text_builder import build_report_texts, split_tags


def get_tag_interpretations(tags, language="RU"):
    result = []
    for tag in tags:
        meta = TAG_REGISTRY.get(tag)
        if not meta:
            continue

        result.append({
            "tag": tag,
            "category": meta["category"],
            "severity": meta["severity"],
            "description": meta["description_ru"] if language == "RU" else meta["description_en"],
        })

    return result


def add_interpretation_columns(df, language="RU"):
    df = df.copy()

    if df.empty:
        return df

    rows = []
    for _, row in df.iterrows():
        rows.append(build_report_texts(row, language=language))

    import pandas as pd
    text_df = pd.DataFrame(rows, index=df.index)

    for col in text_df.columns:
        df[col] = text_df[col]

    return df
