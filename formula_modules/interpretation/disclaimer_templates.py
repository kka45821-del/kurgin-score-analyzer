DISCLAIMER = {
    "RU": "KURGIN Score не является лабораторным сертификатом и не заменяет заключение IGI, GIA или другой геммологической лаборатории. Анализ основан на параметрах, предоставленных пользователем, импортированных из таблицы или извлечённых из документа. Цвет, чистота, масса, цена и лаборатория отображаются как отдельные характеристики и не входят в основной KURGIN Score.",
    "EN": "KURGIN Score is not a laboratory certificate and does not replace an IGI, GIA or other gemological laboratory report. The analysis is based on parameters provided by the user, imported from a table or extracted from a document. Color, clarity, carat weight, price and laboratory are displayed as separate characteristics and are not included in the core KURGIN Score.",
}


def get_disclaimer(language="RU"):
    return DISCLAIMER.get(language, DISCLAIMER["EN"])
