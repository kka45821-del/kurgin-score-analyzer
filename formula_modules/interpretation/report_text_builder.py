from .disclaimer_templates import get_disclaimer
from .recommendation_templates import build_recommendation
from .risk_templates import build_risk_warning
from .score_band_interpreter import get_score_band, get_score_band_label
from .score_text_templates import get_band_text
from .tag_templates import get_tag_summary
from .text_style import bullet_list, clean_text_ru, join_sentences


def split_tags(tags_text, max_tags=6):
    tags = [tag.strip() for tag in str(tags_text or "").replace(";", ",").split(",") if tag.strip()]
    return tags[:max_tags]


def _format_weight(weight):
    text = str(weight or "").strip()
    if not text:
        return ""
    return text if "ct" in text.lower() else f"{text} ct"


def build_stone_title(row):
    shape = str(row.get("Shape", "") or "").strip()
    weight = _format_weight(row.get("Weight", ""))
    color = str(row.get("Color", "") or "").strip()
    clarity = str(row.get("Clarity", "") or "").strip()

    parts = [item for item in [shape, weight, color, clarity] if item]
    return " ".join(parts) if parts else "Diamond Analysis"


def build_identification_line(row):
    lab = str(row.get("Lab", "") or "").strip()
    report = str(row.get("Report #", "") or "").strip()

    parts = []
    if lab:
        parts.append(lab)
    if report:
        parts.append(f"Report # {report}")

    return " · ".join(parts)


def build_short_interpretation(row, language="RU"):
    status = str(row.get("Calculation Status", ""))
    if status != "OK":
        verdict = str(row.get("Verdict", "ERROR"))
        if verdict == "IN DEVELOPMENT":
            text = get_band_text("not_calculated", language=language, text_type="short")
        else:
            text = get_band_text("not_calculated", language=language, text_type="short")
        return clean_text_ru(text) if language == "RU" else text

    band = get_score_band(row.get("Kurgin Score"))
    base = get_band_text(band["key"], language=language, text_type="short")

    tags = split_tags(row.get("Tags", ""), max_tags=3)
    tag_summary = get_tag_summary(tags, language=language, max_items=2)

    text = join_sentences([base] + tag_summary)
    return clean_text_ru(text) if language == "RU" else text


def build_detail_interpretation(row, language="RU"):
    status = str(row.get("Calculation Status", ""))
    if status != "OK":
        verdict = str(row.get("Verdict", "ERROR"))
        if language == "RU":
            if verdict == "IN DEVELOPMENT":
                return "Данная огранка пока находится в разработке для KURGIN Score. Текущая версия модели откалибрована для Round Brilliant."
            return "Расчёт не выполнен из-за ошибки или неполных данных. Проверьте параметры сертификата и повторите анализ."
        if verdict == "IN DEVELOPMENT":
            return "This shape is currently in development for KURGIN Score. The current model is calibrated for Round Brilliant."
        return "Calculation was not completed due to an error or incomplete data. Check the certificate parameters and repeat the analysis."

    band = get_score_band(row.get("Kurgin Score"))
    base = get_band_text(band["key"], language=language, text_type="detail")

    tags = split_tags(row.get("Tags", ""), max_tags=6)
    tag_summary = get_tag_summary(tags, language=language, max_items=6)

    risk_warning = build_risk_warning(row, language=language)

    parts = [base]
    if tag_summary:
        parts.append(bullet_list(tag_summary))
    if risk_warning:
        parts.append(risk_warning)

    text = "\n\n".join(parts)
    return clean_text_ru(text) if language == "RU" else text


def build_executive_summary(row, language="RU"):
    title = build_stone_title(row)
    score = row.get("Kurgin Score")
    band_label = get_score_band_label(score, language=language)
    verdict = str(row.get("Verdict Local", row.get("Verdict", "")))

    if language == "RU":
        if score is None or str(score) == "nan":
            return f"{title}: расчёт KURGIN Score не выполнен."
        return f"{title}: {band_label}. Итоговый статус — {verdict}."

    if score is None or str(score) == "nan":
        return f"{title}: KURGIN Score was not calculated."
    return f"{title}: {band_label}. Final status — {verdict}."


def build_report_texts(row, language="RU"):
    tags = split_tags(row.get("Tags", ""), max_tags=6)
    band = get_score_band(row.get("Kurgin Score"))

    recommendation_ru = build_recommendation(row, language="RU")
    recommendation_en = build_recommendation(row, language="EN")
    warning_ru = build_risk_warning(row, language="RU")
    warning_en = build_risk_warning(row, language="EN")

    result = {
        "Stone Title": build_stone_title(row),
        "Identification Line": build_identification_line(row),
        "score_band": band["key"],
        "score_band_label_ru": get_score_band_label(row.get("Kurgin Score"), language="RU"),
        "score_band_label_en": get_score_band_label(row.get("Kurgin Score"), language="EN"),
        "tags_all": "; ".join(tags),

        "executive_summary_ru": build_executive_summary(row, language="RU"),
        "interpretation_short_ru": build_short_interpretation(row, language="RU"),
        "interpretation_detail_ru": build_detail_interpretation(row, language="RU"),
        "recommendation_ru": clean_text_ru(recommendation_ru),
        "warning_ru": clean_text_ru(warning_ru),
        "disclaimer_ru": get_disclaimer("RU"),

        "executive_summary_en": build_executive_summary(row, language="EN"),
        "interpretation_short_en": build_short_interpretation(row, language="EN"),
        "interpretation_detail_en": build_detail_interpretation(row, language="EN"),
        "recommendation_en": recommendation_en,
        "warning_en": warning_en,
        "disclaimer_en": get_disclaimer("EN"),
    }

    for i in range(6):
        result[f"tag{i + 1}"] = tags[i] if i < len(tags) else ""

    return result
