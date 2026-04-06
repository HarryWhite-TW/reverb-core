from subprocess import run
import sys


def test_cli_json_outputs_valid_symbol_normalization_result():
    result = run(
        [sys.executable, "-m", "elysia_core.cli", "--json", "What!!??"],
        capture_output=True,
        text=True,
        cwd="src",
    )

    assert result.returncode == 0
    assert '"processed_text": "What！？"' in result.stdout
    assert '"is_valid": true' in result.stdout
    assert '"name": "symbol_cleaner"' in result.stdout


def test_cli_json_outputs_fallback_for_empty_input():
    result = run(
        [sys.executable, "-m", "elysia_core.cli", "--json", "   "],
        capture_output=True,
        text=True,
        cwd="src",
    )

    assert result.returncode == 0
    assert '"processed_text": "…"' in result.stdout
    assert '"is_valid": false' in result.stdout
    assert '"EMPTY_INPUT"' in result.stdout
    assert '"name": "fallback_if_empty"' in result.stdout