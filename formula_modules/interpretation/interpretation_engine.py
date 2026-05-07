from formula_modules.tags.tag_registry import TAG_REGISTRY

def get_tag_interpretations(tags, language="RU"):
    result = []
    for tag in tags:
        meta = TAG_REGISTRY.get(tag)
        if not meta: continue
        result.append({
            "tag": tag,
            "category": meta["category"],
            "severity": meta["severity"],
            "description": meta["description_ru"] if language == "RU" else meta["description_en"],
        })
    return result
