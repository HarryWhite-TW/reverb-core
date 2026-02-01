def validate_persona_name(value: str, errors: list) -> str: #人名
    #驗證persona_name是否合法
    #如果不合法就加入errors並回傳安全值
    if not isinstance(value, str):
       errors.append("persona_name must be a non-empty string(persona_name不是字串)")
       return "Unknown"
    
    if value == "":
       errors.append("persona_name cannot be empty(persona_name不能是空值)")
       return "Unknown"
    
    return value

def validate_max_response_length(value, errors: list) -> int: #最大響應長度
    #驗證max_response_length是否合法
    #如果不合法就加入errors並回傳安全值
    if not isinstance(value, int):
       errors.append("max_response_length cannot be a type other than int(max_response_length不可為str)")
       fallback = 50
       value = fallback
    
    if value < 1:
       errors.append("max_response_length must not be less than 1(max_response_length不可小於1)")
       fallback = 50
       value = fallback
    
    return value

def validate_config(config: dict) -> dict:
    #驗證整份config
    errors = []
    
    value = config.get("persona_name")   #取值
    value = validate_persona_name(value, errors)   #帶入函式，修正值為value，錯誤則傳errors
    config["persona_name"] = value   #放回修正結果

    value = config.get("max_response_length")
    value = validate_max_response_length(value, errors)
    config["max_response_length"] = value

    return {"config": config, "errors": errors}
