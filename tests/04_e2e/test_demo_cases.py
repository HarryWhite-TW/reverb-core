# 對外展示案例的最後 smoke test 保護層。

from elysia_core.input.preprocess import preprocess_input

def test_demo_case_symbol_normalization_remains_valid():
    result = preprocess_input("What!!??")

    assert result.processed_text == "What！？"
    assert result.is_valid is True
    assert result.errors == []
    assert any(ev.name == "symbol_cleaner" for ev in result.events)

def test_demo_case_empty_input_falls_back_safely():
    result = preprocess_input("   ")

    assert result.processed_text == "…"
    assert result.is_valid is False
    assert any(e.code == "EMPTY_INPUT" for e in result.errors)
    assert any(ev.name == "fallback_if_empty" for ev in result.events)
    assert not any(ev.name == "symbol_cleaner" for ev in result.events)
