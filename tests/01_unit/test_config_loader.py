import json
from pathlib import Path

import pytest

from elysia_core.config.config_loader import load_config, load_default_config


def test_load_config_reads_valid_json_file(tmp_path):
    config_file = tmp_path / "test_config.json"
    config_file.write_text(
        json.dumps({"persona_name": "Echo", "max_response_length": 50}),
        encoding="utf-8",
    )

    result = load_config(config_file)

    assert result["persona_name"] == "Echo"
    assert result["max_response_length"] == 50


def test_load_config_raises_file_not_found_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_config(missing_file)


def test_load_default_config_returns_dict():
    result = load_default_config()

    assert isinstance(result, dict)