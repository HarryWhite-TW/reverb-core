import json

import streamlit as st

from elysia_core.input.preprocess import preprocess_input


st.set_page_config(
    page_title="Reverb Input Inspector",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="collapsed",
)


TEXT = {
    "zh": {
        "language_zh": "\u4e2d\u6587",
        "language_en": "English",
        "title": "Reverb \u8f38\u5165\u6aa2\u67e5\u5668",
        "description": "\u9019\u662f Reverb Core \u7684\u793a\u7bc4 UI\uff0c\u7528\u4f86\u5c55\u793a\u8f38\u5165\u5982\u4f55\u88ab\u6aa2\u67e5\u3001\u6e05\u7406\u6216\u963b\u64cb\u3002\u5b83\u4e0d\u662f production-ready\u3001\u4e0d\u662f\u5b8c\u6574 SDK\u3001\u4e0d\u662f Local AI Workbench integration\uff0c\u4e5f\u4e0d\u662f Task Packet Guardrail implementation\u3002",
        "input": "\u8f38\u5165",
        "preset": "\u793a\u7bc4\u6848\u4f8b",
        "current_input": "\u76ee\u524d\u8f38\u5165",
        "analyze": "\u5206\u6790\u76ee\u524d\u8f38\u5165",
        "pending": "\u8f38\u5165\u5df2\u8b8a\u66f4\u3002\u8acb\u6309\u300c\u5206\u6790\u76ee\u524d\u8f38\u5165\u300d\u4ee5\u91cd\u65b0\u6574\u7406\u7d50\u679c\u3002",
        "none_note": "\u9019\u500b\u6848\u4f8b\u6703\u76f4\u63a5\u547c\u53eb preprocess_input(None)\u3002\u756b\u9762\u4e0a\u7684 None \u53ea\u662f\u6a19\u7c64\uff0c\u4e0d\u662f\u6587\u5b57\u8f38\u5165\u81ea\u7136\u9001\u51fa\u7684\u503c\u3002",
        "overview": "\u6982\u89bd",
        "process": "\u8655\u7406\u6d41\u7a0b",
        "technical": "\u6280\u8853\u7d30\u7bc0",
        "result_summary": "\u7d50\u679c\u6458\u8981",
        "initial": "\u9078\u64c7\u6848\u4f8b\u6216\u8f38\u5165\u6587\u5b57\uff0c\u7136\u5f8c\u6309\u4e0b\u5206\u6790\u6309\u9215\u3002",
        "analyzed_input": "\u5df2\u5206\u6790\u8f38\u5165",
        "safe": "\u53ef\u4ee5\u7e7c\u7e8c",
        "blocked": "\u5df2\u963b\u64cb",
        "processed_text": "\u8655\u7406\u5f8c\u6587\u5b57",
        "error_codes": "Error codes",
        "trace_id": "\u8ffd\u8e64 ID",
        "valid_explanation": "Reverb \u5df2\u6b63\u898f\u5316\u8f38\u5165\uff0c\u53ef\u4ee5\u7e7c\u7e8c\u9032\u5165\u4e0b\u4e00\u500b\u5de5\u4f5c\u6b65\u9a5f\u3002",
        "blocked_explanation": "Reverb \u5075\u6e2c\u5230\u4e0d\u53ef\u7528\u7684\u8f38\u5165\uff0c\u4e26\u56de\u50b3\u5b89\u5168 fallback \u8207\u932f\u8aa4\u8cc7\u8a0a\u3002",
        "changed_explanation": "\u90e8\u5206\u5167\u5bb9\u5df2\u88ab\u6e05\u7406\u6216\u6b63\u898f\u5316\u3002",
        "unchanged_explanation": "\u8f38\u5165\u6c92\u6709\u9700\u8981\u6e05\u7406\u7684\u5167\u5bb9\u3002",
        "step_inspector": "Step Inspector",
        "step_helper": "\u9019\u88e1\u986f\u793a Reverb \u5be6\u969b\u57f7\u884c\u7684\u6b65\u9a5f\u3002\u5b83\u4e0d\u662f\u53ef\u8a2d\u5b9a\u7684 pipeline \u958b\u95dc\u3002",
        "changed_only": "\u53ea\u986f\u793a\u6703\u6539\u8b8a\u8f38\u5165\u7684\u6b65\u9a5f",
        "changed": "changed",
        "unchanged": "unchanged",
        "before_after": "\u67e5\u770b\u8655\u7406\u524d / \u8655\u7406\u5f8c",
        "before": "\u8655\u7406\u524d",
        "after": "\u8655\u7406\u5f8c",
        "before_escape": "before_escape",
        "after_escape": "after_escape",
        "processed_text_escape": "processed_text_escape",
        "is_valid": "is_valid",
        "errors": "errors",
        "events": "events",
        "correlation_id": "correlation_id",
        "correlation_id_length": "correlation_id_length",
        "raw_summary": "Raw JSON-like summary",
    },
    "en": {
        "language_zh": "\u4e2d\u6587",
        "language_en": "English",
        "title": "Reverb Input Inspector",
        "description": "This is a demo UI for Reverb Core. It shows how input is checked, cleaned, or blocked. It is not production-ready, not SDK-complete, not Local AI Workbench integration, and not Task Packet Guardrail implementation.",
        "input": "Input",
        "preset": "Demo case",
        "current_input": "Current input",
        "analyze": "Analyze current input",
        "pending": 'Input changed. Press "Analyze current input" to refresh the result.',
        "none_note": "This case calls preprocess_input(None) directly. The visible None is only a label, not a value naturally submitted by text input.",
        "overview": "Overview",
        "process": "Process",
        "technical": "Technical Details",
        "result_summary": "Result Summary",
        "initial": "Choose a case or enter text, then press Analyze current input.",
        "analyzed_input": "Analyzed input",
        "safe": "Safe to continue",
        "blocked": "Blocked",
        "processed_text": "Processed text",
        "error_codes": "Error codes",
        "trace_id": "Trace ID",
        "valid_explanation": "Reverb normalized the input and it can continue to the next workflow step.",
        "blocked_explanation": "Reverb detected an unusable input and returned a safe fallback with error information.",
        "changed_explanation": "Some content was cleaned or normalized.",
        "unchanged_explanation": "No cleanup was needed for this input.",
        "step_inspector": "Step Inspector",
        "step_helper": "This shows the steps Reverb executed. It is not a configurable pipeline switch.",
        "changed_only": "Show only steps that changed the input",
        "changed": "changed",
        "unchanged": "unchanged",
        "before_after": "View before / after",
        "before": "Before",
        "after": "After",
        "before_escape": "before_escape",
        "after_escape": "after_escape",
        "processed_text_escape": "processed_text_escape",
        "is_valid": "is_valid",
        "errors": "errors",
        "events": "events",
        "correlation_id": "correlation_id",
        "correlation_id_length": "correlation_id_length",
        "raw_summary": "Raw JSON-like summary",
    },
}


PRESETS = [
    {
        "key": "valid_symbols",
        "label_en": "Valid symbol normalization",
        "label_zh": "\u6709\u6548\u7b26\u865f\u6b63\u898f\u5316",
        "visible": "What!!??",
    },
    {
        "key": "whitespace",
        "label_en": "Whitespace fallback",
        "label_zh": "\u7a7a\u767d fallback",
        "visible": "   ",
    },
    {
        "key": "mixed_symbols",
        "label_en": "Mixed symbols",
        "label_zh": "\u6df7\u5408\u7b26\u865f",
        "visible": "***Hello world!!!***",
    },
    {
        "key": "normal_sentence",
        "label_en": "Normal sentence",
        "label_zh": "\u4e00\u822c\u53e5\u5b50",
        "visible": "Hello world",
    },
    {
        "key": "python_none",
        "label_en": "Python None object",
        "label_zh": "Python None \u7269\u4ef6",
        "visible": "None",
    },
]


STEP_DESCRIPTIONS = {
    "zh": {
        "type_guard": "\u6aa2\u67e5\u8f38\u5165\u662f\u5426\u70ba\u5b57\u4e32\u3002",
        "strip_spaces": "\u79fb\u9664\u958b\u982d\u8207\u7d50\u5c3e\u7684\u7a7a\u767d\u3002",
        "trim_edges": "\u4fee\u526a\u908a\u754c\u4e0a\u7684\u4e0d\u652f\u63f4\u7b26\u865f\u3002",
        "collapse_spaces": "\u6b63\u898f\u5316\u91cd\u8907\u7a7a\u767d\u3002",
        "symbol_cleaner": "\u6b63\u898f\u5316\u91cd\u8907\u6a19\u9ede\u7b26\u865f\u3002",
        "fallback_if_empty": "\u8f38\u5165\u70ba\u7a7a\u6642\u4f7f\u7528\u5b89\u5168 fallback\u3002",
    },
    "en": {
        "type_guard": "Checks whether the input is a string.",
        "strip_spaces": "Removes leading and trailing whitespace.",
        "trim_edges": "Trims unsupported edge symbols.",
        "collapse_spaces": "Normalizes repeated spaces.",
        "symbol_cleaner": "Normalizes repeated punctuation.",
        "fallback_if_empty": "Uses a safe fallback for empty input.",
    },
}


def preset_by_key(key):
    return next(preset for preset in PRESETS if preset["key"] == key)


def preset_label(key, lang):
    preset = preset_by_key(key)
    return preset["label_zh"] if lang == "zh" else preset["label_en"]


def update_visible_input_from_preset():
    st.session_state.visible_input = preset_by_key(st.session_state.preset_key)["visible"]


def escape_text(value):
    if isinstance(value, str):
        return value.encode("unicode_escape").decode()
    return repr(value)


def event_to_dict(event):
    return {
        "name": event.name,
        "severity": event.severity,
        "changed": event.changed,
        "note": event.note,
        "before": event.before,
        "after": event.after,
    }


def error_to_dict(error):
    return {
        "code": error.code,
        "message": error.message,
        "step": error.step,
        "severity": error.severity,
    }


def result_summary(result):
    return {
        "original_input_repr": repr(result.original_input),
        "processed_text": result.processed_text,
        "processed_text_escape": escape_text(result.processed_text),
        "is_valid": result.is_valid,
        "errors": [error_to_dict(error) for error in result.errors],
        "events": [event_to_dict(event) for event in result.events],
        "correlation_id": result.correlation_id,
        "correlation_id_length": len(result.correlation_id),
    }


def has_changed_events(result):
    return any(event.changed for event in result.events)


def display_value(value):
    return repr(value) if not isinstance(value, str) else value


def render_before_after(event, t):
    if event.before is None and event.after is None:
        return

    with st.expander(t["before_after"]):
        before_col, after_col = st.columns(2)
        with before_col:
            st.caption(t["before"])
            st.code("" if event.before is None else display_value(event.before))
            before_escape = escape_text(event.before)
            if event.before is not None and before_escape != str(event.before):
                st.caption(t["before_escape"])
                st.code(before_escape)
        with after_col:
            st.caption(t["after"])
            st.code("" if event.after is None else display_value(event.after))
            after_escape = escape_text(event.after)
            if event.after is not None and after_escape != str(event.after):
                st.caption(t["after_escape"])
                st.code(after_escape)


if "preset_key" not in st.session_state:
    st.session_state.preset_key = PRESETS[0]["key"]
if "visible_input" not in st.session_state:
    st.session_state.visible_input = PRESETS[0]["visible"]
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_visible_input" not in st.session_state:
    st.session_state.last_visible_input = None

language_choice = st.radio(
    "Display language",
    ["\u4e2d\u6587", "English"],
    horizontal=True,
    label_visibility="collapsed",
)
lang = "zh" if language_choice == "\u4e2d\u6587" else "en"
t = TEXT[lang]

st.title(t["title"])
st.caption(t["description"])
st.divider()

with st.container(border=True):
    st.write(f"### {t['input']}")
    st.selectbox(
        t["preset"],
        [preset["key"] for preset in PRESETS],
        format_func=lambda key: preset_label(key, lang),
        key="preset_key",
        on_change=update_visible_input_from_preset,
    )

    if st.session_state.preset_key == "python_none":
        st.info(t["none_note"])

    disabled_input = st.session_state.preset_key == "python_none"
    st.text_input(
        t["current_input"],
        key="visible_input",
        disabled=disabled_input,
    )

    with st.form("analyze_form"):
        submitted = st.form_submit_button(t["analyze"], type="primary")

if submitted:
    value = None if st.session_state.preset_key == "python_none" else st.session_state.visible_input
    st.session_state.last_result = preprocess_input(value)
    st.session_state.last_visible_input = st.session_state.visible_input

result = st.session_state.last_result
pending = result is not None and st.session_state.visible_input != st.session_state.last_visible_input

if pending:
    st.warning(t["pending"])

overview_tab, process_tab, technical_tab = st.tabs(
    [t["overview"], t["process"], t["technical"]]
)

with overview_tab:
    if result is None:
        st.info(t["initial"])
    else:
        summary = result_summary(result)
        error_codes = [error.code for error in result.errors]

        st.write(f"### {t['result_summary']}")
        if result.is_valid:
            st.success(t["safe"])
        else:
            st.error(t["blocked"])

        first_col, second_col = st.columns(2)
        with first_col:
            st.metric(t["analyzed_input"], repr(result.original_input))
        with second_col:
            st.metric(
                t["error_codes"],
                ", ".join(error_codes) if error_codes else "None",
            )

        st.caption(t["processed_text"])
        st.code(result.processed_text)

        explanation = t["valid_explanation"] if result.is_valid else t["blocked_explanation"]
        change_explanation = (
            t["changed_explanation"]
            if has_changed_events(result)
            else t["unchanged_explanation"]
        )
        st.info(f"{explanation}\n\n{change_explanation}")

        st.metric(t["trace_id"], summary["correlation_id"])

with process_tab:
    if result is None:
        st.info(t["initial"])
    else:
        st.write(f"### {t['step_inspector']}")
        st.caption(t["step_helper"])
        changed_only = st.checkbox(t["changed_only"])
        visible_events = [
            event for event in result.events if event.changed or not changed_only
        ]

        rows = [
            {
                "name": event.name,
                "description": STEP_DESCRIPTIONS[lang].get(event.name, event.name),
                "severity": event.severity,
                "state": t["changed"] if event.changed else t["unchanged"],
            }
            for event in visible_events
        ]
        st.table(rows)

        for event in visible_events:
            if event.note:
                st.caption(f"{event.name}: {event.note}")
            render_before_after(event, t)

with technical_tab:
    if result is None:
        st.info(t["initial"])
    else:
        summary = result_summary(result)
        metric_col_1, metric_col_2 = st.columns(2)
        with metric_col_1:
            st.metric(t["is_valid"], str(summary["is_valid"]))
            st.metric(t["correlation_id_length"], summary["correlation_id_length"])
        with metric_col_2:
            st.metric(t["correlation_id"], summary["correlation_id"])
            st.metric(t["processed_text_escape"], summary["processed_text_escape"])

        st.caption(t["errors"])
        st.code(json.dumps(summary["errors"], indent=2), language="json")
        st.caption(t["events"])
        st.code(json.dumps(summary["events"], indent=2), language="json")
        st.caption(t["raw_summary"])
        st.code(json.dumps(summary, indent=2), language="json")
