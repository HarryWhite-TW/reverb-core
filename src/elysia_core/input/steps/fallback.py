def fallback_if_empty(text: str) -> dict:
    if str(text).strip() == "":
        return {"text": "\u2026", "reason": "fallback"}
    return {"text": text, "reason": "normal"}
