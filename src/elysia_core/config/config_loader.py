import json
from pathlib import Path

def load_config(config_path: Path) -> dict:
    #讀取JSON設定檔
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_default_config() -> dict:
    #讀取預設的default.json
    base_path = Path(__file__).resolve().parents[0]
    default_path = base_path / "default.json"
    return load_config(default_path)
