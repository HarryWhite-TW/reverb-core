import re


def collapse_spaces(text: str) -> str:
    return re.sub(" +", " ", text)
