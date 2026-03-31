from elysia_core.input.preprocess import preprocess_input
import pytest

#展示:
#1. invalid input 會回傳預期錯誤身分
#2. valid input 會正常處理且無錯誤
#3. mixed valid case 仍可正規化並保持有效
#4. fallback_if_empty 觸發 early return 後，symbol_cleaner 不得再介入


@pytest.mark.parametrize(
    "raw_input, expected_output, expected_valid, expected_event, expected_error_code",
    [
        ("", "…", False, "fallback_if_empty", "EMPTY_INPUT"),
        (123, "…", False, "type_guard", "UNEXPECTED_TYPE"),
    ],
)
def test_invalid_inputs_return_expected_error_identity(
    raw_input,
    expected_output,
    expected_valid,
    expected_event,
    expected_error_code,
):
    result = preprocess_input(raw_input)

    assert result.processed_text == expected_output
    assert result.is_valid is expected_valid
    assert any(ev.name == expected_event for ev in result.events)
    assert any(e.code == expected_error_code for e in result.errors)


@pytest.mark.parametrize(
    "raw_input, expected_output, expected_valid, expected_event",
    [
        (" Hello world ", "Hello world", True, "strip_spaces"),
        ("What!!??", "What！？", True, "symbol_cleaner"),
    ],
)
def test_valid_inputs_are_processed_without_errors(
    raw_input,
    expected_output,
    expected_valid,
    expected_event,
):
    result = preprocess_input(raw_input)

    assert result.processed_text == expected_output
    assert result.is_valid is expected_valid
    assert any(ev.name == expected_event for ev in result.events)
    assert result.errors == []


def test_mixed_symbols_and_outer_noise_are_normalized_and_remain_valid():
    result = preprocess_input("***Hello... world!!!***")

    assert result.processed_text == "Hello… world！"
    assert result.is_valid is True
    assert any(ev.name == "symbol_cleaner" for ev in result.events)
    assert result.errors == []


def test_fallback_text_is_not_modified_after_empty_input_early_return():
    result = preprocess_input("   ")

    assert result.processed_text == "…"
    assert result.is_valid is False
    assert any(ev.name == "fallback_if_empty" for ev in result.events)
    assert not any(ev.name == "symbol_cleaner" for ev in result.events)
    assert any(e.code == "EMPTY_INPUT" for e in result.errors)

def test_non_string_input_stops_pipeline_before_string_steps():
    result = preprocess_input(123)

    assert result.processed_text == "…"
    assert result.is_valid is False
    assert any(ev.name == "type_guard" for ev in result.events)
    assert not any(ev.name == "strip_spaces" for ev in result.events)
    assert not any(ev.name == "trim_edges" for ev in result.events)
    assert not any(ev.name == "collapse_spaces" for ev in result.events)
    assert not any(ev.name == "symbol_cleaner" for ev in result.events)
    assert any(e.code == "UNEXPECTED_TYPE" for e in result.errors) 
    