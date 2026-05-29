#FILE:test_preprocess_units.py
from elysia_core.input.preprocess import (
    collapse_spaces,
    fallback_if_empty,
    symbol_cleaner,
    trim_edges,
    strip_spaces,
)


def test_trim_edges_removes_only_outer_noise():
    #Arrange
    s = "###你好，world!!###"

    #Act
    out = trim_edges(s)

    #Assert
    assert out == "你好，world!!"


def test_trim_edges_keeps_valid_edge_chars():
    #Arrange
    s = "你好，world!!"

    #Act
    out = trim_edges(s)

    #Assert
    assert out == "你好，world!!"


def test_strip_spaces_removes_leading_and_trailing_spaces():
    #Arrange
    s = "  hi  "

    #Act
    out = strip_spaces(s)

    #Assert
    assert out == "hi"


def test_collapse_spaces_compresses_multiple_spaces_to_single():
    #Arrange
    s = "我    是   學生"

    #Act
    out = collapse_spaces(s)

    #Assert
    assert out == "我 是 學生"


def test_fallback_if_empty_returns_fallback_for_empty_string():
    #Arrange
    s = ""

    #Act
    out = fallback_if_empty(s)

    #Assert
    assert out == {"text": "…", "reason": "fallback"}


def test_fallback_if_empty_returns_fallback_for_whitespace_only_string():
    #Arrange
    s = "   "

    #Act
    out = fallback_if_empty(s)

    #Assert
    assert out == {"text": "…", "reason": "fallback"}


def test_fallback_if_empty_returns_normal_for_text():
    #Arrange
    s = "hello"

    #Act
    out = fallback_if_empty(s)

    #Assert
    assert out == {"text": "hello", "reason": "normal"}


def test_symbol_cleaner_collapses_ascii_periods_to_ellipsis():
    #Arrange
    s = "...."

    #Act
    out = symbol_cleaner(s)

    #Assert
    assert out == "…"


def test_symbol_cleaner_collapses_chinese_periods_to_ellipsis():
    #Arrange
    s = "。。。。"

    #Act
    out = symbol_cleaner(s)

    #Assert
    assert out == "…"


def test_symbol_cleaner_collapses_repeated_exclamation_marks():
    #Arrange
    s = "!!!!"

    #Act
    out = symbol_cleaner(s)

    #Assert
    assert out == "！"


def test_symbol_cleaner_collapses_repeated_question_marks():
    #Arrange
    s = "????"

    #Act
    out = symbol_cleaner(s)

    #Assert
    assert out == "？"


def test_symbol_cleaner_collapses_repeated_tildes():
    #Arrange
    s = "~~~~"

    #Act
    out = symbol_cleaner(s)

    #Assert
    assert out == "～"


def test_symbol_cleaner_normalizes_mixed_exclamation_and_question():
    #Arrange
    s = "!!??!!"

    #Act
    out = symbol_cleaner(s)

    #Assert
    assert out == "！？"


def test_symbol_cleaner_keeps_already_normalized_representative_string_stable():
    #Arrange
    s = "你好…！？～"

    #Act
    out = symbol_cleaner(s)

    #Assert
    assert out == "你好…！？～"


def test_symbol_cleaner_with_collapse_spaces_produces_expected_tokens():
    #Arrange
    s = "。。  ...  。。"

    #Act
    out = symbol_cleaner(collapse_spaces(s))

    #Assert
    assert out == "… … …"
