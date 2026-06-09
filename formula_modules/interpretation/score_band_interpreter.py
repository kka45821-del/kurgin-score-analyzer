SCORE_BANDS = [
    {
        "key": "elite",
        "min": 95,
        "max": 100,
        "label_ru": "Элитный",
        "label_en": "Elite",
        "tone": "elite",
        "comment_ru": "Элитный диапазон KURGIN Score.",
        "comment_en": "Elite KURGIN Score range.",
    },
    {
        "key": "premium",
        "min": 90,
        "max": 94.999,
        "label_ru": "Премиальный",
        "label_en": "Premium",
        "tone": "premium",
        "comment_ru": "Премиальный диапазон KURGIN Score.",
        "comment_en": "Premium KURGIN Score range.",
    },
    {
        "key": "high",
        "min": 80,
        "max": 89.999,
        "label_ru": "Высокое качество",
        "label_en": "High Quality",
        "tone": "positive",
        "comment_ru": "Диапазон высокого качества по KURGIN Score.",
        "comment_en": "High-quality KURGIN Score range.",
    },
    {
        "key": "standard",
        "min": 70,
        "max": 79.999,
        "label_ru": "Стандартный",
        "label_en": "Standard",
        "tone": "commercial",
        "comment_ru": "Стандартный диапазон KURGIN Score.",
        "comment_en": "Standard KURGIN Score range.",
    },
    {
        "key": "fair",
        "min": 60,
        "max": 69.999,
        "label_ru": "Среднее качество",
        "label_en": "Fair Quality",
        "tone": "caution",
        "comment_ru": "Диапазон среднего качества по KURGIN Score.",
        "comment_en": "Fair-quality KURGIN Score range.",
    },
    {
        "key": "poor",
        "min": 0,
        "max": 59.999,
        "label_ru": "Низкое качество",
        "label_en": "Low Quality",
        "tone": "negative",
        "comment_ru": "Диапазон низкого качества по KURGIN Score.",
        "comment_en": "Low-quality KURGIN Score range.",
    },
]


def to_float(value):
    try:
        return float(value)
    except Exception:
        return None


def get_score_band(score):
    score = to_float(score)

    if score is None:
        return {
            "key": "not_calculated",
            "label_ru": "Не рассчитано",
            "label_en": "Not calculated",
            "tone": "neutral",
            "comment_ru": "Расчёт не выполнен.",
            "comment_en": "Calculation was not completed.",
        }

    for band in SCORE_BANDS:
        if band["min"] <= score <= band["max"]:
            return band

    return {
        "key": "not_calculated",
        "label_ru": "Не рассчитано",
        "label_en": "Not calculated",
        "tone": "neutral",
        "comment_ru": "Расчёт не выполнен.",
        "comment_en": "Calculation was not completed.",
    }


def get_score_band_key(score):
    return get_score_band(score)["key"]


def get_score_band_label(score, language="RU"):
    band = get_score_band(score)
    return band["label_ru"] if language == "RU" else band["label_en"]


def get_score_band_comment(score, language="RU"):
    band = get_score_band(score)
    return band["comment_ru"] if language == "RU" else band["comment_en"]
