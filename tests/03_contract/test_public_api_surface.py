import re

from elysia_core.contracts import ErrorItem, ProcessingResult, StepEvent
from elysia_core.input.preprocess import preprocess_input


def test_preprocess_input_returns_stable_processing_result_surface_for_valid_input():
    result = preprocess_input("What!!??")

    assert isinstance(result, ProcessingResult)
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None
    assert result.original_input == "What!!??"
    assert isinstance(result.processed_text, str)
    assert isinstance(result.is_valid, bool)
    assert isinstance(result.events, list)
    assert isinstance(result.errors, list)

    assert result.processed_text == "What！？"
    assert result.is_valid is True
    assert result.errors == []
    assert all(isinstance(ev, StepEvent) for ev in result.events)
    assert any(ev.name == "symbol_cleaner" for ev in result.events)


def test_preprocess_input_returns_stable_processing_result_surface_for_empty_input():
    result = preprocess_input("   ")

    assert isinstance(result, ProcessingResult)
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None
    assert result.original_input == "   "
    assert isinstance(result.processed_text, str)
    assert isinstance(result.is_valid, bool)
    assert isinstance(result.events, list)
    assert isinstance(result.errors, list)

    assert result.processed_text == "…"
    assert result.is_valid is False
    assert all(isinstance(ev, StepEvent) for ev in result.events)
    assert all(isinstance(err, ErrorItem) for err in result.errors)
    assert any(err.code == "EMPTY_INPUT" for err in result.errors)
    assert any(ev.name == "fallback_if_empty" for ev in result.events)


def test_preprocess_input_returns_stable_processing_result_surface_for_non_string_input():
    raw_input = 123
    result = preprocess_input(raw_input)

    assert isinstance(result, ProcessingResult)
    assert re.fullmatch(r"[0-9a-f]{32}", result.correlation_id) is not None
    assert result.original_input == raw_input
    assert isinstance(result.processed_text, str)
    assert isinstance(result.is_valid, bool)
    assert isinstance(result.events, list)
    assert isinstance(result.errors, list)

    assert result.processed_text == "…"
    assert result.is_valid is False
    assert all(isinstance(ev, StepEvent) for ev in result.events)
    assert all(isinstance(err, ErrorItem) for err in result.errors)
    assert any(err.code == "UNEXPECTED_TYPE" for err in result.errors)
    assert any(ev.name == "type_guard" for ev in result.events)

def test_processing_result_exposes_minimum_public_fields():
    result = preprocess_input("Hello")

    assert hasattr(result, "correlation_id")
    assert hasattr(result, "original_input")
    assert hasattr(result, "processed_text")
    assert hasattr(result, "is_valid")
    assert hasattr(result, "events")
    assert hasattr(result, "errors")

    assert isinstance(result.processed_text, str)
    assert isinstance(result.is_valid, bool)
    assert isinstance(result.events, list)
    assert isinstance(result.errors, list)
    assert isinstance(result.correlation_id, str)

    assert result.original_input == "Hello"

    assert all(isinstance(ev, StepEvent) for ev in result.events)
