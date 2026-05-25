VERDICT_TEXTS = {
    "ELITE: Premium Build": {
        "short_ru": "Камень показывает уровень премиальной геометрической сбалансированности по текущей модели KURGIN Score.",
        "detail_ru": "Основные параметры круглой огранки демонстрируют сильную согласованность. По текущей модели не выявлено признаков критического оптического риска.",
        "short_en": "The diamond shows premium geometric balance under the current KURGIN Score model.",
        "detail_en": "The main round-brilliant parameters show strong consistency. No critical optical risk is detected by the current model.",
    },
    "TOP: Excellent Selection": {
        "short_ru": "Камень показывает высокий уровень геометрической сбалансированности и может рассматриваться как сильный кандидат.",
        "detail_ru": "Сочетание основных углов и пропорций находится в рабочей зоне для круглой бриллиантовой огранки. Критических оптических рисков по текущей модели не выявлено.",
        "short_en": "The diamond shows a high level of geometric balance and may be considered a strong candidate.",
        "detail_en": "The main angles and proportions are within the working zone for round brilliant cutting. No critical optical risks are detected by the current model.",
    },
    "HIGH: Great Quality": {
        "short_ru": "Камень имеет хороший уровень пропорций и может быть интересен для подбора при дополнительной визуальной проверке.",
        "detail_ru": "Параметры камня в целом находятся в приемлемой зоне. Отдельные особенности могут требовать сравнения с альтернативами близкого веса и класса.",
        "short_en": "The diamond has a good proportion profile and may be considered after visual confirmation.",
        "detail_en": "The stone parameters are generally within an acceptable zone. Some features may require comparison with similar alternatives.",
    },
    "STD: Commercial Grade": {
        "short_ru": "Камень относится к коммерческому уровню по текущей модели KURGIN Score.",
        "detail_ru": "Геометрия и структура не показывают премиального уровня сбалансированности. Камень может быть рассмотрен при подходящей цене и визуальном подтверждении.",
        "short_en": "The diamond is classified as commercial grade under the current KURGIN Score model.",
        "detail_en": "The geometry and structure do not show premium-level balance. The stone may still be considered if price and visual appearance are acceptable.",
    },
    "REJECT: Poor Performance": {
        "short_ru": "Камень требует осторожности: текущая модель указывает на слабое качество геометрической или оптической структуры.",
        "detail_ru": "По текущим параметрам камень может иметь выраженные признаки дисбаланса. Рекомендуется сравнить его с альтернативами с более стабильной геометрией.",
        "short_en": "Caution is required: the current model indicates weak geometric or optical structure.",
        "detail_en": "Based on the available parameters, the diamond may show notable imbalance. Comparison with more stable alternatives is recommended.",
    },
    "NOTICE: Visual Check Recommended": {
        "short_ru": "Камень требует визуальной проверки перед принятием решения.",
        "detail_ru": "По текущей модели выявлены признаки, которые не обязательно делают камень плохим, но требуют дополнительного визуального осмотра или сравнения.",
        "short_en": "Visual inspection is recommended before making a decision.",
        "detail_en": "The current model detected features that do not necessarily make the stone poor, but require additional visual review or comparison.",
    },
    "CAUTION: Critical Optical Risk": {
        "short_ru": "Обнаружен критический оптический риск. Камень требует повышенной осторожности.",
        "detail_ru": "Текущая модель выявляет признаки, которые могут существенно влиять на визуальное восприятие камня. Рекомендуется не принимать решение без визуального подтверждения и сравнения.",
        "short_en": "A critical optical risk is detected. The diamond requires increased caution.",
        "detail_en": "The current model detects features that may materially affect visual appearance. Do not make a decision without visual confirmation and comparison.",
    },
    "IN DEVELOPMENT": {
        "short_ru": "Данная огранка находится в разработке для KURGIN Score.",
        "detail_ru": "Текущая версия расчёта откалибрована для Round Brilliant. Для других огранок требуется отдельная модель анализа.",
        "short_en": "This shape is currently in development for KURGIN Score.",
        "detail_en": "The current scoring model is calibrated for Round Brilliant. Other shapes require separate analysis models.",
    },
    "ERROR": {
        "short_ru": "Расчёт не выполнен из-за ошибки или неполных данных.",
        "detail_ru": "Проверьте корректность параметров сертификата и числовых значений, необходимых для расчёта.",
        "short_en": "Calculation was not completed due to an error or incomplete data.",
        "detail_en": "Check the certificate parameters and numeric values required for calculation.",
    },
}


def get_verdict_text(verdict, language="RU", detail=False):
    item = VERDICT_TEXTS.get(verdict, VERDICT_TEXTS["ERROR"])
    key = ("detail_" if detail else "short_") + language.lower()
    return item.get(key, item.get("short_en", ""))
