import re


def trim_edges(text: str) -> str:
    allowed_chars = (
        r"A-Za-z0-9"
        r"\u4e00-\u9fff"
        r"\.\,\?\!"
        r"\uFF1F\uFF01\uFF5E\u2026"
    )
    text = re.sub(rf"^[^{allowed_chars}]+", "", text)
    text = re.sub(rf"[^{allowed_chars}]+$", "", text)
    return text
