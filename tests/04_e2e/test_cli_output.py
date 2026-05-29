from subprocess import run
import json
import re
import sys


def run_cli_json(text):
    result = run(
        [sys.executable, "-m", "elysia_core.cli", "--json", text],
        capture_output=True,
        text=True,
        cwd="src",
    )

    assert result.returncode == 0
    return json.loads(result.stdout)


def test_cli_json_outputs_valid_symbol_normalization_result():
    payload = run_cli_json("What!!??")
    event_names = [event["name"] for event in payload["events"]]

    assert {
        "processed_text",
        "is_valid",
        "errors",
        "events",
        "correlation_id",
    }.issubset(payload.keys())
    assert payload["processed_text"] == "What！？"
    assert payload["is_valid"] is True
    assert payload["errors"] == []
    assert re.fullmatch(r"[0-9a-f]{32}", payload["correlation_id"]) is not None
    assert isinstance(payload["events"], list)
    assert all(
        {"name", "changed", "severity"}.issubset(event.keys())
        for event in payload["events"]
    )
    assert "symbol_cleaner" in event_names


def test_cli_json_outputs_fallback_for_empty_input():
    payload = run_cli_json("   ")
    event_names = [event["name"] for event in payload["events"]]

    assert payload["processed_text"] == "…"
    assert payload["is_valid"] is False
    assert payload["errors"] == ["EMPTY_INPUT"]
    assert re.fullmatch(r"[0-9a-f]{32}", payload["correlation_id"]) is not None
    assert "fallback_if_empty" in event_names
    assert "symbol_cleaner" not in event_names
