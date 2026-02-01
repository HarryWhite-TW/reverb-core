from pathlib import Path
from elysia_core.config.config_loader import load_default_config

def test_load_default_config_returns_dict():
    #測試是否成功回傳dict
    config = load_default_config()
    assert isinstance(config, dict)

def test_load_default_config_persona_name():
    #persona_name應該是Elysia
    config = load_default_config()
    assert config.get("persona_name") == "Elysia"

def test_load_default_config_no_error():
    #測試函式是否能正常運行不報錯
    try:
        load_default_config()
    except Exception as e:
        assert False, f"load_default_config raised an error: {e}"

def test_max_response_length_positive():
    #最大回應長度應大於0
    config = load_default_config()
    assert config.get("max_response_length", -1) > 0

def test_enable_safety_exists():
    #enable_safety應該存在於設定中
    config = load_default_config()
    assert "enable_safety" in config
