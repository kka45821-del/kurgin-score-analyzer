FORBIDDEN_PHRASES_RU = [
    "после визуальной проверки",
    "при подтверждении документа и визуального восприятия",
]


REPLACEMENTS_RU = {
    "после визуальной проверки": "если визуальный осмотр, фото или видео не выявляют нежелательных эффектов",
    "при подтверждении документа и визуального восприятия": "если данные сертификата проверены по номеру отчёта, а визуальный осмотр, фото или видео не выявляют нежелательных эффектов",
}


def clean_text_ru(text):
    if not text:
        return ""

    cleaned = str(text)
    for old, new in REPLACEMENTS_RU.items():
        cleaned = cleaned.replace(old, new)

    # normalize spaces
    cleaned = " ".join(cleaned.split())
    return cleaned


def join_sentences(sentences):
    clean = []
    for sentence in sentences:
        if not sentence:
            continue
        sentence = str(sentence).strip()
        if not sentence:
            continue
        if sentence[-1] not in ".!?":
            sentence += "."
        clean.append(sentence)
    return " ".join(clean)


def bullet_list(items):
    return "\n".join(f"• {item}" for item in items if item)
