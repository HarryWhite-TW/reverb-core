import uuid
from typing import Any

from elysia_core.contracts import ErrorItem, ProcessingResult, StepEvent
from elysia_core.input.runner import run_step
from elysia_core.input.steps.collapse_spaces import collapse_spaces
from elysia_core.input.steps.fallback import fallback_if_empty
from elysia_core.input.steps.strip import strip_spaces
from elysia_core.input.steps.symbol_cleaner import symbol_cleaner
from elysia_core.input.steps.trim_edges import trim_edges


def make_correlation_id() -> str:
    return uuid.uuid4().hex


def run_preprocess_pipeline(text: Any) -> ProcessingResult:
    correlation_id = make_correlation_id()

    result = {
        "text": text,
    }

    events: list[StepEvent] = []
    errors: list[ErrorItem] = []

    if not isinstance(text, str):
        errors.append(
            ErrorItem(
                code="UNEXPECTED_TYPE",
                message="\u8f38\u5165\u985e\u578b\u975e\u5b57\u4e32\uff0c\u5df2\u4f7f\u7528 fallback",
                step="type_guard",
                severity="warn",
            )
        )
        events.append(
            StepEvent(
                name="type_guard",
                severity="warn",
                changed=True,
                note="\u975e\u5b57\u4e32\u8f38\u5165\uff0c\u4f7f\u7528 fallback \u4e26\u63d0\u524d\u7d42\u6b62",
                before=text,
                after="\u2026",
            )
        )
        return ProcessingResult(
            correlation_id=correlation_id,
            original_input=text,
            processed_text="\u2026",
            is_valid=False,
            events=events,
            errors=errors,
        )

    before = result["text"]

    after, event = run_step(
        name="strip_spaces",
        func=strip_spaces,
        before=before,
    )

    result["text"] = after
    events.append(event)

    before = result["text"]

    after, event = run_step(
        name="trim_edges",
        func=trim_edges,
        before=before,
    )

    result["text"] = after
    events.append(event)

    before = result["text"]

    after, event = run_step(
        name="collapse_spaces",
        func=collapse_spaces,
        before=before,
    )

    result["text"] = after
    events.append(event)

    fb = fallback_if_empty(result["text"])

    result["text"] = fb["text"]

    if fb["reason"] == "fallback":
        errors.append(
            ErrorItem(
                code="EMPTY_INPUT",
                message="\u8f38\u5165\u70ba\u7a7a\u6216\u975e\u6709\u6548\u5b57\u4e32\uff0c\u5df2\u4f7f\u7528 fallback",
                step="fallback_if_empty",
                severity="warn",
            )
        )

        events.append(
            StepEvent(
                name="fallback_if_empty",
                severity="warn",
                changed=True,
                note="\u8f38\u5165\u70ba\u7a7a\uff0c\u63d0\u524d\u7d42\u6b62 pipeline",
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
