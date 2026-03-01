#FILE:test_preprocess_pipeline.py
from elysia_core.input.preprocess import preprocess_input


def test_whitespace_input_falls_back_and_is_invalid():
    #Arrange
    text = "     "

    #Act
    result = preprocess_input(text)

    #Assert
    assert result.processed_text == "…"
    assert result.is_valid is False

    #註解:integration只輕鎖「有走到fallback」，不鎖錯誤碼細節
    assert any(ev.name == "fallback_if_empty" for ev in result.events)


def test_mixed_symbols_are_normalized_and_records_symbol_cleaner_event():
    #Arrange
    text = "!!??!!"

    #Act
    result = preprocess_input(text)

    #Assert
    assert result.is_valid is True

      #檢查1：最終清理結果應縮減為 "！？"
    assert result.processed_text == "！？"
      #檢查2：events 應包含 symbol_cleaner 這一步
    assert any(ev.name == "symbol_cleaner" for ev in result.events)