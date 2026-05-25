SCORE_BANDS = [
    {
        "key": "elite",
        "min": 99,
        "max": 100,
        "label_ru": "Премиальный уровень",
        "label_en": "Premium level",
        "tone": "positive",
    },
    {
        "key": "top",
        "min": 95,
        "max": 98.999,
        "label_ru": "Сильный кандидат",
        "label_en": "Strong candidate",
        "tone": "positive",
    },
    {
        "key": "high",
        "min": 90,
        "max": 94.999,
        "label_ru": "Хороший уровень",
        "label_en": "Good level",
        "tone": "positive_careful",
    },
    {
        "key": "upper_commercial",
        "min": 85,
        "max": 89.999,
        "label_ru": "Верхняя коммерческая зона",
        "label_en": "Upper commercial zone",
        "tone": "careful",
    },
    {
        "key": "commercial",
        "min": 80,
        "max": 84.999,
        "label_ru": "Коммерческий уровень",
        "label_en": "Commercial level",
        "tone": "caution",
    },
    {
        "key": "weak",
        "min": 76,
        "max": 79.999,
        "label_ru": "Слабая зона",
        "label_en": "Weak zone",
        "tone": "negative_careful",
    },
    {
        "key": "reject",
        "min": 0,
        "max": 75.999,
        "label_ru": "Зона повышенной осторожности",
        "label_en": "High caution zone",
        "tone": "negative",
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
        }

    for band in SCORE_BANDS:
        if band["min"] <= score <= band["max"]:
            return band

    return {
        "key": "not_calculated",
        "label_ru": "Не рассчитано",
        "label_en": "Not calculated",
        "tone": "neutral",
    }


def get_score_band_key(score):
    return get_score_band(score)["key"]


def get_score_band_label(score, language="RU"):
    band = get_score_band(score)
    return band["label_ru"] if language == "RU" else band["label_en"]
