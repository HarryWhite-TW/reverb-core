from dataclasses import dataclass, field
from typing import Any, List, Optional, Literal

Severity = Literal["info","warn","error"]  #決策意義：我在限制錯誤等級，防止亂塞字串


@dataclass
class ErrorItem:
    code: str
    message: str
    step: str
    severity: Severity = "error"



@dataclass  #決策意義：我要一個「資料結構」，不是行為物件
class StepEvent:   #StepEvent:「過程中發生了什麼」
    name: str  #叫什麼
    severity: Severity  #嚴重性(info / warn / error)
    changed: bool  #有沒有改動
    note: str  #補充說明
    before: Optional[Any] = None  #改動前
    after: Optional[Any] = None  #改動後



@dataclass
class ProcessingResult:
    correlation_id: str  #單次流水編號(讓log、trace、測試可以對應)
    original_input: Any  #原始輸入保留（為了追溯與證據鏈）
    processed_text: str  #處理後結果(真正交給後續模組用)
    is_valid: bool  #這次輸入判定是否可用
    events: List[StepEvent] = field(default_factory=list)  #field(default_factory=list)決策意義：避免共享同一個 list 造成跨請求污染。
    errors: List[ErrorItem] = field(default_factory=list)

