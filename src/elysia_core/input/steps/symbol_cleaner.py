import re


def symbol_cleaner(text: str) -> str:
    text = re.sub(r"\.{2,}", "\u2026", text)
    text = re.sub(r"\u3002{2,}", "\u2026", text)
    text = re.sub(r"\?{2,}", "\uFF1F", text)
    text = re.sub(r"!{2,}", "\uFF01", text)
    text = re.sub(r"~{2,}", "\uFF5E", text)

    def normalize(block: str) -> str:
        unique = []
        for ch in block:
            if ch not in unique:
                unique.append(ch)

        full = []
        for ch in unique[:2]:
            if ch in ["!", "\uFF01"]:
                full.append("\uFF01")
            elif ch in ["?", "\uFF1F"]:
                full.append("\uFF1F")
        return "".join(full)

    text = re.sub(r"[!?\uFF01\uFF1F]+", lambda m: normalize(m.group(0)), text)

    return text
