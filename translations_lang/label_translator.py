VERDICT_TRANSLATIONS = {
    "ELITE: Elite": {"RU": "Элитный", "EN": "Elite"},
    "PREMIUM: Premium": {"RU": "Премиальный", "EN": "Premium"},
    "HIGH: High Quality": {"RU": "Высокое качество", "EN": "High Quality"},
    "STANDARD: Standard": {"RU": "Стандартный", "EN": "Standard"},
    "FAIR: Fair Quality": {"RU": "Среднее качество", "EN": "Fair Quality"},
    "POOR: Low Quality": {"RU": "Низкое качество", "EN": "Low Quality"},

    # Backward-compatible old engine labels. They must not expose "ОТКЛОНЕНО" publicly.
    "ELITE: Premium Build": {"RU": "Элитный", "EN": "Elite"},
    "TOP: Excellent Selection": {"RU": "Премиальный", "EN": "Premium"},
    "HIGH: Great Quality": {"RU": "Высокое качество", "EN": "High Quality"},
    "STD: Commercial Grade": {"RU": "Стандартный", "EN": "Standard"},
    "REJECT: Poor Performance": {"RU": "Низкое качество", "EN": "Low Quality"},

    "NOTICE: Visual Check Recommended": {"RU": "Требует визуальной проверки", "EN": "Visual Check Recommended"},
    "CAUTION: Critical Optical Risk": {"RU": "Критический оптический риск", "EN": "Critical Optical Risk"},
    "IN DEVELOPMENT": {"RU": "В разработке", "EN": "In development"},
    "ERROR": {"RU": "Ошибка", "EN": "Error"},
}

TAG_TRANSLATIONS = {
    "Perfect Build": {"RU": "Идеальная сборка", "EN": "Perfect Build"},
    "Hidden Weight": {"RU": "Скрытый вес", "EN": "Hidden Weight"},
    "Nailhead Risk": {"RU": "Риск тёмного центра", "EN": "Nailhead Risk"},
    "Fisheye Risk": {"RU": "Риск рыбьего глаза", "EN": "Fisheye Risk"},
    "Low Fire": {"RU": "Слабая игра света", "EN": "Low Fire"},
}


def translate_verdict(verdict, language):
    return VERDICT_TRANSLATIONS.get(verdict, {"RU": verdict, "EN": verdict}).get(language, verdict)


def translate_tag(tag, language):
    return TAG_TRANSLATIONS.get(tag, {"RU": tag, "EN": tag}).get(language, tag)


def translate_tags(tags_text, language):
    if not tags_text:
        return ""
    tags = [tag.strip() for tag in str(tags_text).replace(";", ",").split(",") if tag.strip()]
    return ", ".join(translate_tag(tag, language) for tag in tags)
