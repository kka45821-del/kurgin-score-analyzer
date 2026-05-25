from .score_band_interpreter import get_score_band_key
from .score_text_templates import get_band_text


def build_recommendation(row, language="RU"):
    verdict = str(row.get("Verdict", ""))
    critical = bool(row.get("Critical Risk", False))
    status = str(row.get("Calculation Status", ""))

    if status != "OK":
        if language == "RU":
            if verdict == "IN DEVELOPMENT":
                return "Для данной огранки рекомендуется дождаться отдельной версии модели KURGIN Score или использовать экспертную оценку."
            return "Проверьте исходные параметры и повторите расчёт."
        if verdict == "IN DEVELOPMENT":
            return "For this shape, wait for a dedicated KURGIN Score model or use expert evaluation."
        return "Check the source parameters and run the calculation again."

    if critical:
        if language == "RU":
            return "Не рекомендуется принимать решение без профессионального визуального осмотра и сравнения с альтернативами."
        return "Do not make a decision without professional visual inspection and comparison with alternatives."

    band_key = get_score_band_key(row.get("Kurgin Score"))
    return get_band_text(band_key, language=language, text_type="recommendation")
