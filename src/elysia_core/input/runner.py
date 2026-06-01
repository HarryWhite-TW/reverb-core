from collections.abc import Callable

from elysia_core.contracts import StepEvent


def run_step(name: str, func: Callable[[str], str], before: str) -> tuple[str, StepEvent]:
    after = func(before)
    changed = before != after

    event = StepEvent(
        name=name,
        severity="info",
        changed=changed,
        note="",
        before=before,
        after=after,
    )
    return after, event
