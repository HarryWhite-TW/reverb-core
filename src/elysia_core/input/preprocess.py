import re
import uuid
from elysia_core.contracts import ProcessingResult, StepEvent, ErrorItem


print("⚡ 我是最新 preprocess.py ⚡")

def make_correlation_id() -> str:
    return uuid.uuid4().hex
#1. uuid4()：產生一個「幾乎不會重複」的隨機 ID（UUID v4）
#2. .hex：把 UUID 轉成「只含 0-9 a-f 的 32 碼字串」，沒有破折號，方便 log、檔名、測試。
#每次呼叫會得到像這樣的值（示意）：f2a1c9b0c8d94a4db57b2c7d41a0e3d1（32 個十六進位字元）

def preprocess_input(text: str) -> ProcessingResult:
    """
    完整的輸入前處理流程：
    1. 去除前後空白
    2. 去除句外符號（trim_edges）
    3. 壓縮句中空白
    4. fallback_if_empty → 處理 None / 空字串
    5. 清理/壓縮符號（symbol_cleaner）
    6. 回傳 text + errors + reasons（處理紀錄）
    """

    correlation_id = make_correlation_id()  #註解:全路徑共用，同一次呼叫只生成一次

    result = {
        "text": text,
    }

    #註解:容器一定要在最前面就存在，避免後面 append 爆掉
    events: list[StepEvent] = []
    errors: list[ErrorItem] = []


    # ---------------------------------------------------------
    # PART 0：型別防禦（非字串 → fallback，但仍回 ProcessingResult）
    # ---------------------------------------------------------
    if not isinstance(text, str):
        errors.append(
            ErrorItem(
                code="UNEXPECTED_TYPE",
                message="輸入類型非字串，已使用 fallback",
                step="type_guard",
                severity="warn",
            )
        )
        events.append(
            StepEvent(
                name="type_guard",
                severity="warn",
                changed=True,
                note="非字串輸入，使用 fallback 並提前終止",
                before=text,
                after="…",
            )
        )
        return ProcessingResult(
            correlation_id=correlation_id,
            original_input=text,
            processed_text="…",
            is_valid=False,
            events=events,
            errors=errors,
        )

    # -----------------------------------------
    # PART 1：strip 前後空白（step 化）
    # -----------------------------------------
    before = result["text"]

    after, event = run_step(
        name="strip_spaces",
        func=strip_spaces,
        before=before,
    )

    result["text"] = after
    events.append(event)


    # -----------------------------------------
    # PART 2：trim_edges（句外符號清除）
    # -----------------------------------------
    before = result["text"]

    after, event = run_step(
        name="trim_edges",
        func=trim_edges,
        before=before
    ) 

    result["text"] = after
    events.append(event)

    # -----------------------------------------
    # PART 3：collapse_spaces 壓縮句中空白
    # -----------------------------------------
    before = result["text"]

    after, event = run_step(
        name="collapse_spaces",
        func=collapse_spaces,
        before=before
    )

    result["text"] = after
    events.append(event)

    # -----------------------------------------
    # PART 4：fallback_if_empty（空字串/None）
    # -----------------------------------------

    fb = fallback_if_empty(result["text"])

    result["text"] = fb["text"]

    #註解:先做最小事件紀錄：只記 fallback
    if fb["reason"] == "fallback":
       errors.append(
           ErrorItem(
               code="EMPTY_INPUT",
               message="輸入為空或非有效字串，已使用 fallback",
               step="fallback_if_empty",
               severity="warn",
           )
       )

       events.append(
           StepEvent(
               name="fallback_if_empty",
               severity="warn",
               changed=True,
               note="輸入為空，提前終止 pipeline",
               before=text,
               after=result["text"],
           )
       )

       return ProcessingResult(
           correlation_id=correlation_id,
           original_input=text,
           processed_text=result["text"],
           is_valid=False,
           events=events,
           errors=errors,
       )

    # -----------------------------------------
    # PART 5：symbol_cleaner（清理符號）
    # -----------------------------------------
    before = result["text"]
    
    after, event = run_step(
        name="symbol_cleaner",
        func=symbol_cleaner,
        before=before,
    )

    result["text"] = after
    events.append(event)

    return ProcessingResult(
        correlation_id=correlation_id,
        original_input=text,
        processed_text=result["text"],
        is_valid=True,
        events=events,
        errors=errors,
    )



# ---------------------------------------------------------
# run_step: 把「處理行為本身」變成一個可記錄、可回放、可驗證的東西。
# ---------------------------------------------------------
def run_step(name: str, func, before: str)-> tuple[str, StepEvent]:  
     #func像「插槽」，把不同的處理函式「插進去」collapse_spaces、trim_edges、symbol_cleaner
    after = func(before)
    changed = before != after  #「事件是否改變輸入，是由資料自己決定的」。

    event = StepEvent(  #把這一步「發生了什麼」封裝成標準格式，交回給 pipeline 去收集。
        name=name,
        severity="info",
        changed=changed,
        note="",
        before=before,
        after=after,
    )
    return after, event


# ---------------------------------------------------------
# strip_spaces: 輸入字串 → 回傳去除前後空白後的字串，沒有紀錄、沒有事件、沒有錯誤處理。
# ---------------------------------------------------------
def strip_spaces(text: str) -> str:
    return text.strip()


# ---------------------------------------------------------
# collapse_spaces: 將多個空白壓成「1 個空白」
# ---------------------------------------------------------
def collapse_spaces(text: str) -> str:
    return re.sub(" +", " ", text)


# ---------------------------------------------------------
# symbol_cleaner: 壓縮重複符號
# ---------------------------------------------------------
def symbol_cleaner(text: str) -> str:
    # 基礎收斂（句點、波浪等）
    text = re.sub(r"\.{2,}", "…", text)
    text = re.sub(r"。{2,}", "…", text)
    text = re.sub(r"\?{2,}", "？", text)
    text = re.sub(r"!{2,}", "！", text)
    text = re.sub(r"~{2,}", "～", text)

    # 混合 !? 區塊收斂
    def normalize(block: str) -> str:
        # 抓出不同種類的符號（依出現順序）
        unique = []
        for ch in block:
            if ch not in unique:
                unique.append(ch)
        # 替換成全形
        full = []
        for ch in unique[:2]:  # 最多取兩種
            if ch in ['!', '！']:
                full.append("！")
            elif ch in ['?', '？']:
                full.append("？")
        return "".join(full)

    text = re.sub(r"[!?！？]+", lambda m: normalize(m.group(0)), text)

    return text

# ---------------------------------------------------------
# fallback_if_empty: 處理 None 或空字串
# ---------------------------------------------------------
def fallback_if_empty(text: str) -> dict:
    if text is None or str(text).strip() == "":
        return {
            "text": "…",
            "errors": ["輸入為空，因此使用 fallback"],
            "reason": "fallback"
        }

    return {
        "text": text,
        "errors": [],
        "reason": "normal"
    }


# ---------------------------------------------------------
# trim_edges:去除頭尾標點符號
# ---------------------------------------------------------
def trim_edges(text: str) -> str:
    #註解:只做句首/句尾的非法字元剔除，不碰中間
    allowed_chars = r"A-Za-z0-9\u4e00-\u9fff\.\,\?\!\？\！\～\…"
    text = re.sub(rf"^[^{allowed_chars}]+", "", text)
    text = re.sub(rf"[^{allowed_chars}]+$", "", text)
    return text

