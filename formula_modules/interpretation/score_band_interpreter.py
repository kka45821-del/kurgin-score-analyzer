SCORE_BANDS = [
    {
        "key": "elite",
        "min": 98.5,
        "max": 100,
        "label_ru": "Элитный",
        "label_en": "Elite",
        "tone": "elite",
        "comment_ru": "Максимальный уровень построения по KURGIN Score.",
        "comment_en": "Maximum build level under KURGIN Score.",
    },
    {
        "key": "premium",
        "min": 95,
        "max": 98.499,
        "label_ru": "Премиальный",
        "label_en": "Premium",
        "tone": "premium",
        "comment_ru": "Премиальный ювелирный класс, сильный кандидат для подбора.",
        "comment_en": "Premium jewelry class, strong candidate for selection.",
    },
    {
        "key": "high",
        "min": 90,
        "max": 94.999,
        "label_ru": "Высокое качество",
        "label_en": "High",
        "tone": "positive",
        "comment_ru": "Хороший уровень построения.",
        "comment_en": "Good build quality level.",
    },
    {
        "key": "standard",
        "min": 80,
        "max": 89.999,
        "label_ru": "Стандартный",
        "label_en": "Standard",
        "tone": "commercial",
        "comment_ru": "Коммерческий диапазон; требует учёта цены и визуальных факторов.",
        "comment_en": "Commercial range; price and visual factors should be considered.",
    },
    {
        "key": "fair",
        "min": 70,
        "max": 79.999,
        "label_ru": "Среднее качество",
        "label_en": "Fair",
        "tone": "caution",
        "comment_ru": "Умеренный результат; нужна осторожность и сравнение с альтернативами.",
        "comment_en": "Moderate result; caution and comparison with alternatives are recommended.",
    },
    {
        "key": "poor",
        "min": 50,
        "max": 69.999,
        "label_ru": "Низкое качество",
        "label_en": "Poor",
        "tone": "negative",
        "comment_ru": "Слабый уровень построения по текущей модели.",
        "comment_en": "Weak build level under the current model.",
    },
    {
        "key": "rejected",
        "min": 0,
        "max": 49.999,
        "label_ru": "Не рекомендуется",
        "label_en": "Rejected",
        "tone": "reject",
        "comment_ru": "Зона отказа для ювелирного подбора по KURGIN Score.",
        "comment_en": "Rejection zone for jewelry selection under KURGIN Score.",
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
