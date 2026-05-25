VERDICT_TRANSLATIONS = {
    "ELITE: Premium Build": {"RU": "ЭЛИТА: Премиальная сборка", "EN": "ELITE: Premium Build"},
    "TOP: Excellent Selection": {"RU": "ТОП: Отличный выбор", "EN": "TOP: Excellent Selection"},
    "HIGH: Great Quality": {"RU": "ВЫСОКИЙ: Хорошее качество", "EN": "HIGH: Great Quality"},
    "STD: Commercial Grade": {"RU": "СТАНДАРТ: Коммерческое качество", "EN": "STD: Commercial Grade"},
    "REJECT: Poor Performance": {"RU": "ОТКЛОНЕНО: Слабая оптика", "EN": "REJECT: Poor Performance"},
    "NOTICE: Visual Check Recommended": {"RU": "ВНИМАНИЕ: Нужна визуальная проверка", "EN": "NOTICE: Visual Check Recommended"},
    "CAUTION: Critical Optical Risk": {"RU": "РИСК: Критическая оптическая проблема", "EN": "CAUTION: Critical Optical Risk"},
    "IN DEVELOPMENT": {"RU": "В РАЗРАБОТКЕ", "EN": "IN DEVELOPMENT"},
    "ERROR": {"RU": "ОШИБКА", "EN": "ERROR"},
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
    tags = [tag.strip() for tag in str(tags_text).split(",") if tag.strip()]
    return ", ".join(translate_tag(tag, language) for tag in tags)
