#FILE:test_preprocess_unexpected_type.py
import pytest
import re
from elysia_core.input.preprocess import preprocess_input
from elysia_core.input.preprocess import trim_edges
from elysia_core.contracts import ProcessingResult  #註解:用來確認 contract 一致

#設計動機:uuid.uuid4().hex 應該永遠是 32 碼、且只包含 0-9 a-f
def test_correlation_id_is_uuid4_hex():
    result = preprocess_input("hi")

    assert isinstance(result.correlation_id, str)
    assert len(result.correlation_id) == 32
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None

def test_preprocess_unexpected_type_fallback():
    #準備：非字串輸入
    obj = [1, 2, 3]

    #動作
    result = preprocess_input(obj)

    #檢查1：回傳格式必須是 ProcessingResult
    assert isinstance(result, ProcessingResult)

    #檢查2：fallback text
    assert result.processed_text == "…"

    #檢查3：errors 應該有 UNEXPECTED_TYPE
    assert any(err.code == "UNEXPECTED_TYPE" for err in result.errors)

    #檢查4：events 應該記到 type_guard
    assert any(ev.name == "type_guard" for ev in result.events)

    #檢查5：整體 valid 應為 False
    assert result.is_valid is False


def test_symbol_mixed_cleaning():
    text = "!!??!!"
    result = preprocess_input(text)

    #檢查1：最終清理結果應縮減為 "！？"
    assert result.processed_text == "！？"

    #檢查2：events 應包含 symbol_cleaner 這一步
    assert any(ev.name == "symbol_cleaner" for ev in result.events)

def test_all_steps_generate_events():
    text = "  !!hello??  "
    result = preprocess_input(text)

    step_names = [ev.name for ev in result.events]

    assert "strip_spaces" in step_names
    assert "trim_edges" in step_names
    assert "collapse_spaces" in step_names
    assert "symbol_cleaner" in step_names


def test_trim_edges_removes_only_outer_noise():
    #註解:頭尾雜訊要被剔除，中間內容不應被動到
    s = "###你好，world!!###"
    assert trim_edges(s) == "你好，world!!"


def test_trim_edges_keeps_valid_edge_chars():
    #註解:合法字元在頭尾時不應被剔除
    s = "你好，world!!"
    assert trim_edges(s) == "你好，world!!"


def test_unexpected_type_contract_locked():
    obj = [1, 2, 3] #它不是 str。 其用意是拿來測試「如果輸入不是 str，系統會不會崩潰？」

    result = preprocess_input(obj)

    #註解:1)回傳結構必須一致
    assert hasattr(result, "processed_text")
    assert hasattr(result, "is_valid")
    assert hasattr(result, "events")
    assert hasattr(result, "errors")

    #註解:2)fallback結果必須固定
    assert result.is_valid is False
    assert result.processed_text == "…"

    #註解:3)錯誤證據鏈必須存在且可被精準assert
    assert any(
        (e.code == "UNEXPECTED_TYPE" and e.step == "type_guard" and e.severity == "warn")
        for e in result.errors
    )

#END
