import pandas as pd


ANALYSIS_ELEMENTS_VERSION = "KURGIN Analysis Elements v1.0"

ANALYSIS_ELEMENT_COLUMNS = [
    "KURGIN Analysis Elements Version",

    "Fire Profile",
    "Fire Explanation RU",
    "Fire Explanation EN",

    "Brilliance Profile",
    "Brilliance Explanation RU",
    "Brilliance Explanation EN",

    "Contrast Profile",
    "Contrast Explanation RU",
    "Contrast Explanation EN",

    "Balance Profile",
    "Balance Explanation RU",
    "Balance Explanation EN",

    "Perfect Build Status",
    "Perfect Build Explanation RU",
    "Perfect Build Explanation EN",

    "Hidden Weight Status",
    "Hidden Weight Explanation RU",
    "Hidden Weight Explanation EN",

    "Nailhead Risk Status",
    "Nailhead Risk Explanation RU",
    "Nailhead Risk Explanation EN",

    "Fisheye Risk Status",
    "Fisheye Risk Explanation RU",
    "Fisheye Risk Explanation EN",

    "Low Fire Status",
    "Low Fire Explanation RU",
    "Low Fire Explanation EN",

    "Active KURGIN Tags",
    "Card Tags",
]


CORE_TAGS = {
    "Perfect Build": {
        "status_col": "Perfect Build Status",
        "ru_col": "Perfect Build Explanation RU",
        "en_col": "Perfect Build Explanation EN",
        "ru": "Идеальная сборка",
        "en": "Perfect Build",
        "desc_ru": "Пропорции и структура камня близки к сильной сбалансированной модели KURGIN.",
        "desc_en": "The proportions and structure are close to a strong balanced KURGIN model.",
    },
    "Hidden Weight": {
        "status_col": "Hidden Weight Status",
        "ru_col": "Hidden Weight Explanation RU",
        "en_col": "Hidden Weight Explanation EN",
        "ru": "Скрытый вес",
        "en": "Hidden Weight",
        "desc_ru": "Часть массы может быть распределена так, что визуальный размер хуже ожидаемого для веса.",
        "desc_en": "Some weight may be distributed in a way that reduces the expected visual size for the carat weight.",
    },
    "Nailhead Risk": {
        "status_col": "Nailhead Risk Status",
        "ru_col": "Nailhead Risk Explanation RU",
        "en_col": "Nailhead Risk Explanation EN",
        "ru": "Риск тёмного центра",
        "en": "Nailhead Risk",
        "desc_ru": "Модель видит риск затемнения центральной зоны при текущей комбинации углов.",
        "desc_en": "The model detects a risk of dark-center appearance for the current angle combination.",
    },
    "Fisheye Risk": {
        "status_col": "Fisheye Risk Status",
        "ru_col": "Fisheye Risk Explanation RU",
        "en_col": "Fisheye Risk Explanation EN",
        "ru": "Риск рыбьего глаза",
        "en": "Fisheye Risk",
        "desc_ru": "Модель видит риск нежелательного эффекта рыбьего глаза.",
        "desc_en": "The model detects a risk of an undesirable fisheye effect.",
    },
    "Low Fire": {
        "status_col": "Low Fire Status",
        "ru_col": "Low Fire Explanation RU",
        "en_col": "Low Fire Explanation EN",
        "ru": "Слабая игра света",
        "en": "Low Fire",
        "desc_ru": "Возможна сниженная дисперсия и игра света относительно более сбалансированных вариантов.",
        "desc_en": "Reduced dispersion and fire potential is possible compared with more balanced alternatives.",
    },
}


def _num(value):
    if value is None:
        return None
    text = str(value).strip().replace(",", ".")
    if not text or text.lower() in {"nan", "none", "—", "-"}:
        return None
    cleaned = "".join(ch for ch in text if ch.isdigit() or ch in ".-")
    if cleaned in {"", ".", "-", "-."}:
        return None
    try:
        return float(cleaned)
    except Exception:
        return None


def _boolish(value):
    if value is True:
        return True
    if value is False or value is None:
        return False
    return str(value).strip().lower() in {"true", "yes", "1", "да", "y"}


def _tag_text(row):
    return " ".join([
        str(row.get("Tags", "") or ""),
        str(row.get("tags_all", "") or ""),
        str(row.get("Tags Local", "") or ""),
    ]).lower()


def _tag_is_active(row, tag):
    text = _tag_text(row)
    meta = CORE_TAGS.get(tag, {})
    return tag.lower() in text or str(meta.get("ru", "")).lower() in text


def _not_calculated():
    return {
        "Fire Profile": "Not calculated / Не рассчитано",
        "Fire Explanation RU": "Расчёт KURGIN Score не выполнен или данных недостаточно.",
        "Fire Explanation EN": "KURGIN Score was not calculated or the data is insufficient.",

        "Brilliance Profile": "Not calculated / Не рассчитано",
        "Brilliance Explanation RU": "Расчёт KURGIN Score не выполнен или данных недостаточно.",
        "Brilliance Explanation EN": "KURGIN Score was not calculated or the data is insufficient.",

        "Contrast Profile": "Not calculated / Не рассчитано",
        "Contrast Explanation RU": "Расчёт KURGIN Score не выполнен или данных недостаточно.",
        "Contrast Explanation EN": "KURGIN Score was not calculated or the data is insufficient.",

        "Balance Profile": "Not calculated / Не рассчитано",
        "Balance Explanation RU": "Расчёт KURGIN Score не выполнен или данных недостаточно.",
        "Balance Explanation EN": "KURGIN Score was not calculated or the data is insufficient.",
    }


def _fire_profile(row):
    fire_loss = _num(row.get("Fire Loss"))
    if fire_loss is None:
        return (
            "Not calculated / Не рассчитано",
            "Показатель огня не рассчитан из-за неполных данных.",
            "Fire indication was not calculated because the data is incomplete.",
        )
    if fire_loss <= 0.07:
        return (
            "High / Высокий",
            "Модель не видит заметного снижения игры света.",
            "The model does not detect a notable reduction in fire potential.",
        )
    if fire_loss <= 0.15:
        return (
            "Good / Хороший",
            "Игра света выглядит приемлемой по текущей модели.",
            "Fire potential appears acceptable under the current model.",
        )
    if fire_loss <= 0.25:
        return (
            "Reduced / Сниженный",
            "Есть риск сниженной игры света относительно более сбалансированных вариантов.",
            "Reduced fire potential is possible compared with more balanced alternatives.",
        )
    return (
        "Low / Низкий",
        "Модель видит выраженный риск слабой игры света.",
        "The model detects a notable risk of weak fire potential.",
    )


def _brilliance_profile(row):
    score = _num(row.get("Kurgin Score"))
    modifier = _num(row.get("Structure Modifier"))
    critical = _boolish(row.get("Critical Risk"))
    visual = _boolish(row.get("Visual Check"))

    if critical:
        return (
            "Risk / Риск",
            "Есть критический риск, поэтому блеск требует отдельной проверки.",
            "A critical risk is present, so brilliance requires separate review.",
        )
    if modifier is not None and modifier >= 0.995 and not visual:
        return (
            "High / Высокий",
            "Структура и пропорции поддерживают высокий возврат света по модели.",
            "The structure and proportions support high light return under the model.",
        )
    if visual:
        return (
            "Needs review / Требует проверки",
            "Модель рекомендует визуальную проверку блеска по фото, видео или осмотру.",
            "The model recommends visual review of brilliance by photo, video or inspection.",
        )
    if score is not None and score >= 90:
        return (
            "Good / Хороший",
            "Общий результат указывает на хороший потенциал блеска.",
            "The overall result indicates good brilliance potential.",
        )
    return (
        "Medium / Средний",
        "Блеск оценивается как средний по текущему набору параметров.",
        "Brilliance is estimated as medium for the current parameter set.",
    )


def _contrast_profile(row):
    nailhead = _num(row.get("Nailhead")) or 0
    fisheye = _num(row.get("Fisheye")) or 0
    critical = _boolish(row.get("Critical Risk"))
    visual = _boolish(row.get("Visual Check"))

    if critical or nailhead >= 0.4 or fisheye >= 0.4:
        return (
            "Risk / Риск",
            "Есть риск нежелательного контрастного рисунка.",
            "There is a risk of an undesirable contrast pattern.",
        )
    if visual or nailhead > 0 or fisheye > 0:
        return (
            "Needs review / Требует проверки",
            "Контраст желательно подтвердить фото, видео или прямым осмотром.",
            "Contrast should be confirmed by photo, video or direct inspection.",
        )
    return (
        "Stable / Стабильный",
        "Модель не видит выраженного риска по контрастному рисунку.",
        "The model does not detect a notable contrast-pattern risk.",
    )


def _balance_profile(row):
    balance = _num(row.get("Balance Err"))
    if balance is None:
        return (
            "Not calculated / Не рассчитано",
            "Баланс не рассчитан из-за неполных данных.",
            "Balance was not calculated because the data is incomplete.",
        )
    if balance <= 0.75:
        return (
            "Strong / Сильный",
            "Глубина, корона и павильон находятся в сильной согласованной связке.",
            "Depth, crown and pavilion are in a strong coordinated relationship.",
        )
    if balance <= 1.50:
        return (
            "Good / Хороший",
            "Баланс основных пропорций выглядит хорошим.",
            "The balance of the main proportions appears good.",
        )
    if balance <= 3.00:
        return (
            "Needs review / Требует проверки",
            "Баланс пропорций требует дополнительной проверки.",
            "The proportion balance requires additional review.",
        )
    return (
        "Weak / Слабый",
        "Модель видит слабый баланс между основными пропорциями.",
        "The model detects weak balance between the main proportions.",
    )


def _build_record(row):
    status = str(row.get("Calculation Status", "") or "")

    record = {"KURGIN Analysis Elements Version": ANALYSIS_ELEMENTS_VERSION}

    if status != "OK":
        record.update(_not_calculated())
    else:
        for prefix, func in [
            ("Fire", _fire_profile),
            ("Brilliance", _brilliance_profile),
            ("Contrast", _contrast_profile),
            ("Balance", _balance_profile),
        ]:
            profile, ru, en = func(row)
            record[f"{prefix} Profile"] = profile
            record[f"{prefix} Explanation RU"] = ru
            record[f"{prefix} Explanation EN"] = en

    active_tags = []
    for tag, meta in CORE_TAGS.items():
        active = status == "OK" and _tag_is_active(row, tag)
        if active:
            active_tags.append(tag)

        if status != "OK":
            record[meta["status_col"]] = "Not calculated / Не рассчитано"
        elif active:
            record[meta["status_col"]] = "Active / Активен"
        else:
            record[meta["status_col"]] = "Not triggered / Не выявлен"

        record[meta["ru_col"]] = meta["desc_ru"]
        record[meta["en_col"]] = meta["desc_en"]

    record["Active KURGIN Tags"] = "; ".join(active_tags)
    record["Card Tags"] = "; ".join([
        f"Огонь: {record.get('Fire Profile', '')}",
        f"Блеск: {record.get('Brilliance Profile', '')}",
        f"Контраст: {record.get('Contrast Profile', '')}",
        f"Баланс: {record.get('Balance Profile', '')}",
    ])

    return record


def add_kurgin_analysis_elements(df):
    df = df.copy()
    if df.empty:
        for col in ANALYSIS_ELEMENT_COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df

    records = [_build_record(row) for _, row in df.iterrows()]
    element_df = pd.DataFrame(records, index=df.index)

    for col in ANALYSIS_ELEMENT_COLUMNS:
        df[col] = element_df[col] if col in element_df.columns else ""

    return df
