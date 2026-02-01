from elysia_core.input.preprocess import (
    preprocess_input,
    collapse_spaces,
    symbol_cleaner
)


def test_empty_input_to_fallback():
    # 輸入是只有空白，例如 "     "
    # 呼叫 preprocess_input()
    # 結果應該要等於 "..."
    # 使用 assert 進行斷言
    result = preprocess_input("     ")
    assert result.processed_text == "…"
    assert result.is_valid is False
    #斷言空白 = ...

def test_collapse_spaces():
    assert collapse_spaces("我    是   駿弘") == "我 是 駿弘"  #斷言複數空白會被壓縮成單一空白

def test_chinese_period_to_ellipsis():
    assert symbol_cleaner("。。。。") == "…"  #斷言"。。。。" = "…"

def test_mixed_periods_with_spaces():
    # collapse_spaces 會把多空白壓成單一空白
    # symbol_cleaner 會把所有句點類符號連續兩個以上變為單一的「…」
    assert symbol_cleaner(collapse_spaces("。。  ...  。。")) == "… … …"

    
