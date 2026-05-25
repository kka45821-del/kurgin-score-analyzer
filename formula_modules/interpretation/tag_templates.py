TAG_TEXTS = {
    "Perfect Build": {
        "ru": "Структура камня выглядит очень сбалансированной по текущим параметрам.",
        "en": "The stone structure appears highly balanced under the current parameters.",
    },
    "Hidden Weight": {
        "ru": "Есть признаки скрытого веса: часть массы может не давать ожидаемого визуального размера.",
        "en": "Possible hidden weight: part of the mass may not contribute to expected visual size.",
    },
    "Nailhead Risk": {
        "ru": "Есть риск затемнения центральной зоны, требующий визуального контроля.",
        "en": "There is a risk of central darkening that requires visual control.",
    },
    "Fisheye Risk": {
        "ru": "Есть риск эффекта «рыбьего глаза», связанный с особенностями оптической геометрии.",
        "en": "There is a fisheye risk related to optical geometry.",
    },
    "Low Fire": {
        "ru": "Возможна сниженная игра света по сравнению с более сбалансированными вариантами.",
        "en": "Reduced fire potential compared with more balanced alternatives is possible.",
    },
}


def get_tag_text(tag, language="RU"):
    item = TAG_TEXTS.get(tag)
    if not item:
        return ""
    return item["ru"] if language == "RU" else item["en"]


def get_tag_summary(tags, language="RU", max_items=4):
    result = []
    for tag in tags[:max_items]:
        text = get_tag_text(tag, language=language)
        if text:
            result.append(text)
    return result
