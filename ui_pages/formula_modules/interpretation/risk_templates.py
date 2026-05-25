from .text_style import join_sentences


def _has_tag(row, tag):
    return tag.lower() in str(row.get("Tags", "")).lower()


def build_risk_warning(row, language="RU"):
    critical = bool(row.get("Critical Risk", False))
    visual = bool(row.get("Visual Check", False))

    if language == "RU":
        if critical:
            return "Выявлен критический оптический риск. Не рекомендуется принимать решение без профессионального визуального осмотра и сравнения с альтернативами."
        if visual:
            return "Модель рекомендует дополнительный визуальный контроль: фото, видео или очный осмотр должны подтвердить отсутствие нежелательных эффектов."

        warnings = []
        if _has_tag(row, "Low Fire"):
            warnings.append("Возможна сниженная игра света по сравнению с более сбалансированными вариантами.")
        if _has_tag(row, "Hidden Weight"):
            warnings.append("Есть признаки скрытого веса: часть массы может не давать ожидаемого визуального размера.")
        if _has_tag(row, "Nailhead Risk"):
            warnings.append("Есть риск затемнения центральной зоны.")
        if _has_tag(row, "Fisheye Risk"):
            warnings.append("Есть риск эффекта «рыбьего глаза».")

        if warnings:
            return join_sentences(warnings)

        return "Критических предупреждений по текущей модели не выявлено."

    if critical:
        return "A critical optical risk is detected. Do not make a decision without professional visual inspection and comparison with alternatives."
    if visual:
        return "The model recommends additional visual control: photo, video or direct inspection should confirm absence of undesirable effects."

    warnings = []
    if _has_tag(row, "Low Fire"):
        warnings.append("Reduced fire potential is possible compared with more balanced alternatives.")
    if _has_tag(row, "Hidden Weight"):
        warnings.append("Possible hidden weight: part of the mass may not contribute to expected visual size.")
    if _has_tag(row, "Nailhead Risk"):
        warnings.append("There is a risk of central darkening.")
    if _has_tag(row, "Fisheye Risk"):
        warnings.append("There is a risk of fisheye effect.")

    if warnings:
        return join_sentences(warnings)

    return "No critical warnings are detected by the current model."
