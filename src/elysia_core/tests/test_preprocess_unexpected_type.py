#FILE: test_preprocess_unexpected_type.py
import inspect
import elysia_core.input.preprocess as pp
print("🔥 pytest 真的跑到這份 test 了嗎？", __file__)
print("🔥 preprocess 實際路徑：", inspect.getfile(pp))

from elysia_core.input.preprocess import preprocess_input


def test_preprocess_unexpected_type_fallback():
    #準備：非字串輸入
    obj = [1,2,3]

    #動作：呼叫 preprocess_input，不應拋出例外
    result_obj = preprocess_input(obj)

    #檢查1：回傳格式必須是 dict
    assert isinstance(result_obj, dict)

    #檢查2：text 必須為字串或 fallback（"…"）
    assert isinstance(result_obj["text"], str)

    #檢查3：非字串 → 直接 fallback（你的 preprocess.py 就是這樣設計）
    assert result_obj["text"] == "…"

    #檢查4：errors 應包含 fallback 的紀錄
    assert any("fallback" in err for err in result_obj["errors"])

    #檢查5：reasons 必須標記為 fallback
    assert "fallback" in result_obj["reasons"]

    #補充：空白字串也要 fallback（獨立測）
    result_blank = preprocess_input("     ")
    assert result_blank.processed_text == "…"
    assert result_blank.is_valid is False

    # errors 現在是 ErrorItem list，不是字串
    assert any(
        err.code == "fallback" or "fallback" in err.message
        for err in result_blank.errors
    )


def test_symbol_mixed_cleaning():
    #準備：全形×半形混用符號
    text = "!!??!!"

    #動作：呼叫 preprocess
    result = preprocess_input(text)

    #檢查1：最終清理結果應縮減為 "！？"
    assert result.processed_text == "！？"

    #檢查2：應紀錄 symbol_cleaner 的行為
    assert any(ev.name == "symbol_cleaner" for ev in result.events)

#END
