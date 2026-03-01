#FILE:test_preprocess_units.py
from elysia_core.input.preprocess import (
    collapse_spaces,
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


def test_symbol_cleaner_collapses_chinese_periods_to_ellipsis():
    #Arrange
    s = "。。。。"

    #Act
    out = symbol_cleaner(s)

    #Assert
    assert out == "…"


def test_symbol_cleaner_normalizes_mixed_exclamation_and_question():
    #Arrange
    s = "!!??!!"

    #Act
    out = symbol_cleaner(s)

    #Assert
    assert out == "！？"


def test_symbol_cleaner_with_collapse_spaces_produces_expected_tokens():
    #Arrange
    s = "。。  ...  。。"

    #Act
    out = symbol_cleaner(collapse_spaces(s))

    #Assert
    assert out == "… … …"