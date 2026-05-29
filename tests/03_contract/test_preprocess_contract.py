#FILE:test_preprocess_contract.py
import re
import pytest
from elysia_core.input.preprocess import preprocess_input
from elysia_core.contracts import ProcessingResult



#設計動機:uuid.uuid4().hex 應該永遠是 32 碼、且只包含 0-9 a-f
def test_preprocess_input_generates_uuid4_hex_correlation_id():
    #Arrange
    text = "hi"

    #Act
    result = preprocess_input(text)

    #Assert
    assert isinstance(result, ProcessingResult)
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None


def test_preprocess_input_records_all_expected_step_events():
    #Arrange
    text = "  !!hello??  "

    #Act
    result = preprocess_input(text)

    #Assert
    step_names = {ev.name for ev in result.events}
    assert "strip_spaces" in step_names
    assert "trim_edges" in step_names
    assert "collapse_spaces" in step_names
    assert "symbol_cleaner" in step_names


def test_non_string_input_returns_fallback_and_records_type_guard_error():
    #Arrange
    obj = [1, 2, 3]

    #Act
    result = preprocess_input(obj)

    #Assert
    assert isinstance(result, ProcessingResult)
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None
    assert result.is_valid is False
    assert result.processed_text == "…"
    assert any(e.code == "UNEXPECTED_TYPE" and e.step == "type_guard" for e in result.errors)
    assert any(e.severity == "warn" for e in result.errors)
    assert any(ev.name == "type_guard" for ev in result.events)
    assert any(ev.name == "type_guard" and ev.severity == "warn" for ev in result.events)
    assert result.original_input == obj


def test_empty_input_returns_fallback_contract():
    #Arrange
    text = "   "

    #Act
    result = preprocess_input(text)

    #Assert
    assert isinstance(result, ProcessingResult)
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None
    assert result.processed_text == "…"
    assert result.is_valid is False
    assert any(e.code == "EMPTY_INPUT" for e in result.errors)
    assert any(e.step == "fallback_if_empty" for e in result.errors)
    assert any(ev.name == "fallback_if_empty" for ev in result.events)
    assert any(e.severity == "warn" for e in result.errors)
    assert any(ev.name == "fallback_if_empty" and ev.severity == "warn" for ev in result.events)

def test_valid_input_returns_stable_contract():

    text = " What!!?? "

    result = preprocess_input(text)

    assert isinstance(result, ProcessingResult)
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None
    assert result.original_input == text
    assert result.processed_text == "What！？"
    assert result.is_valid is True
    assert result.errors == []
    assert any(ev.name == "symbol_cleaner" for ev in result.events)


def test_valid_input_freezes_exact_observable_contract():
    text = " What!!?? "

    result = preprocess_input(text)

    assert isinstance(result, ProcessingResult)
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None
    assert result.original_input == text
    assert result.processed_text == "What！？"
    assert result.is_valid is True
    assert result.errors == []
    assert [ev.name for ev in result.events] == [
        "strip_spaces",
        "trim_edges",
        "collapse_spaces",
        "symbol_cleaner",
    ]
    assert [ev.severity for ev in result.events] == [
        "info",
        "info",
        "info",
        "info",
    ]
    assert [ev.changed for ev in result.events] == [
        True,
        False,
        False,
        True,
    ]


def test_blank_input_freezes_exact_fallback_contract():
    text = "   "

    result = preprocess_input(text)

    assert isinstance(result, ProcessingResult)
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None
    assert result.original_input == text
    assert result.processed_text == "…"
    assert result.is_valid is False
    assert len(result.errors) == 1

    err = result.errors[0]
    assert err.code == "EMPTY_INPUT"
    assert err.step == "fallback_if_empty"
    assert err.severity == "warn"

    assert [ev.name for ev in result.events] == [
        "strip_spaces",
        "trim_edges",
        "collapse_spaces",
        "fallback_if_empty",
    ]
    assert "symbol_cleaner" not in [ev.name for ev in result.events]
    assert [ev.severity for ev in result.events] == [
        "info",
        "info",
        "info",
        "warn",
    ]
    assert [ev.changed for ev in result.events] == [
        True,
        False,
        False,
        True,
    ]


def test_non_string_input_freezes_exact_type_guard_contract():
    raw_input = 123

    result = preprocess_input(raw_input)

    assert isinstance(result, ProcessingResult)
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None
    assert result.original_input == raw_input
    assert result.processed_text == "…"
    assert result.is_valid is False
    assert len(result.errors) == 1

    err = result.errors[0]
    assert err.code == "UNEXPECTED_TYPE"
    assert err.step == "type_guard"
    assert err.severity == "warn"

    assert [ev.name for ev in result.events] == ["type_guard"]
    assert [ev.severity for ev in result.events] == ["warn"]
    assert [ev.changed for ev in result.events] == [True]
    assert "strip_spaces" not in [ev.name for ev in result.events]
    assert "trim_edges" not in [ev.name for ev in result.events]
    assert "collapse_spaces" not in [ev.name for ev in result.events]
    assert "symbol_cleaner" not in [ev.name for ev in result.events]


@pytest.mark.parametrize(
    "raw_input",
    [
        None,
        [1, 2, 3],
        {"x": 1},
        True,
    ],
)
def test_non_string_inputs_freeze_exact_type_guard_contract(raw_input):
    result = preprocess_input(raw_input)

    assert isinstance(result, ProcessingResult)
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None
    assert result.original_input == raw_input
    assert result.processed_text == "…"
    assert result.is_valid is False
    assert len(result.errors) == 1

    err = result.errors[0]
    assert err.code == "UNEXPECTED_TYPE"
    assert err.step == "type_guard"
    assert err.severity == "warn"

    event_names = [ev.name for ev in result.events]
    assert event_names == ["type_guard"]
    assert [ev.severity for ev in result.events] == ["warn"]
    assert [ev.changed for ev in result.events] == [True]
    assert "strip_spaces" not in event_names
    assert "trim_edges" not in event_names
    assert "collapse_spaces" not in event_names
    assert "fallback_if_empty" not in event_names
    assert "symbol_cleaner" not in event_names
    
