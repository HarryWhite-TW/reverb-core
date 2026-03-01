#FILE:test_config_contract.py
from elysia_core.config.config_loader import load_default_config


def test_load_default_config_returns_dict_with_expected_keys():
    #Arrange/Act
    config = load_default_config()

    #Assert
    assert isinstance(config, dict) #測試是否成功回傳dict

      #以下應該存在於設定(config)中
    assert "persona_name" in config
    assert "max_response_length" in config
    assert "enable_safety" in config


def test_default_persona_name_is_elysia():
    #Arrange/Act
    config = load_default_config()

    #Assert
    assert config.get("persona_name") == "Elysia"


def test_default_max_response_length_is_positive():
    #Arrange/Act
    config = load_default_config()

    #Assert
    #最大回應長度應大於0
    assert config.get("max_response_length", -1) > 0