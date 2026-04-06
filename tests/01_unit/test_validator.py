from elysia_core.validator import (
    validate_persona_name,
    validate_max_response_length,
    validate_config,
)


def test_validate_persona_name_returns_unknown_for_non_string():
    errors = []

    result = validate_persona_name(123, errors)

    assert result == "Unknown"
    assert len(errors) == 1
    assert "persona_name must be a non-empty string" in errors[0]


def test_validate_persona_name_returns_unknown_for_empty_string():
    errors = []

    result = validate_persona_name("", errors)

    assert result == "Unknown"
    assert len(errors) == 1
    assert "persona_name cannot be empty" in errors[0]


def test_validate_persona_name_returns_original_value_for_valid_string():
    errors = []

    result = validate_persona_name("Echo", errors)

    assert result == "Echo"
    assert errors == []


def test_validate_max_response_length_returns_fallback_for_non_int():
    errors = []

    result = validate_max_response_length("50", errors)

    assert result == 50
    assert len(errors) == 1
    assert "max_response_length cannot be a type other than int" in errors[0]


def test_validate_max_response_length_returns_fallback_for_value_less_than_one():
    errors = []

    result = validate_max_response_length(0, errors)

    assert result == 50
    assert len(errors) == 1
    assert "max_response_length must not be less than 1" in errors[0]


def test_validate_max_response_length_returns_original_value_for_valid_int():
    errors = []

    result = validate_max_response_length(100, errors)

    assert result == 100
    assert errors == []


def test_validate_config_returns_clean_config_for_valid_input():
    config = {
        "persona_name": "Echo",
        "max_response_length": 120,
    }

    result = validate_config(config)

    assert result["config"]["persona_name"] == "Echo"
    assert result["config"]["max_response_length"] == 120
    assert result["errors"] == []


def test_validate_config_returns_safe_values_and_errors_for_invalid_input():
    config = {
        "persona_name": "",
        "max_response_length": 0,
    }

    result = validate_config(config)

    assert result["config"]["persona_name"] == "Unknown"
    assert result["config"]["max_response_length"] == 50
    assert len(result["errors"]) == 2