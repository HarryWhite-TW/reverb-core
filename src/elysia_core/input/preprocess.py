from typing import Any
from elysia_core.contracts import ProcessingResult
from elysia_core.input.pipeline import run_preprocess_pipeline
from elysia_core.input.steps.collapse_spaces import collapse_spaces
from elysia_core.input.steps.fallback import fallback_if_empty
from elysia_core.input.steps.strip import strip_spaces
from elysia_core.input.steps.symbol_cleaner import symbol_cleaner
from elysia_core.input.steps.trim_edges import trim_edges


def preprocess_input(text: Any) -> ProcessingResult:
    """
    完整的輸入前處理流程：
    1. 去除前後空白
    2. 去除句外符號（trim_edges）
    3. 壓縮句中空白
    4. fallback_if_empty → 處理 None / 空字串
    5. 清理/壓縮符號（symbol_cleaner）
    6. 回傳 text + errors + reasons（處理紀錄）
    """

    return run_preprocess_pipeline(text)



