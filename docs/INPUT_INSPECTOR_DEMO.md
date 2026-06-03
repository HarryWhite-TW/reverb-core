# Reverb Input Inspector Demo

## What It Is

The Input Inspector Demo is a lightweight Streamlit wrapper around Reverb Core.

It uses Streamlit native components only. There are no custom HTML cards, external CSS files, images, or frontend frameworks.

The demo helps viewers understand deterministic input guardrail behavior without reading CLI JSON first. It is a UI wrapper only and does not change Reverb core behavior.

## Boundaries

This demo is:

- not production-ready
- not SDK-complete
- not a full web app
- not Local AI Workbench integration
- not Task Packet Guardrail implementation

## Relationship To Reverb Core

The demo calls the existing public Python entry point:

```python
from elysia_core.input.preprocess import preprocess_input
```

The Python `None` object case calls `preprocess_input(None)` directly. It is a non-string object demo, not normal text input.

## Tab Layout

The UI has three tabs:

- Overview: a non-technical summary for teachers, companies, vendors, GitHub visitors, and other viewers who need the result without reading raw JSON.
- Process: a compact read-only table of the steps Reverb executed, followed by optional before / after expanders when there is meaningful step data.
- Technical Details: full raw contract-style output for engineering review.

The Overview tab answers the public-facing questions first: what kind of input is being demonstrated, what Reverb decided, what Reverb output, whether errors were returned, and why the result matters.

Each preset includes a short scenario explanation and a What happened summary. These are presentation copy only; they do not change Reverb core behavior.

The Overview tab avoids raw JSON, full event lists, debug-like step details, and full `correlation_id` emphasis. It shows only a short trace ID summary. The full `correlation_id` is available in Technical Details.

## Process Tab

The Process tab shows a compact Step Inspector table first. It is read-only because Reverb uses a deterministic fixed pipeline.

The changed-only filter only changes which executed steps are displayed. It does not disable, enable, reorder, or configure pipeline behavior.

The table shows:

- raw step name
- human-readable description
- severity from Reverb core
- changed state

Before / after details are hidden by default inside per-step expanders. Expanders appear only for steps with meaningful before / after data. Human-readable values are shown first, and escaped values appear only when they add useful visibility.

## Technical Details Tab

The Technical Details tab shows:

- `processed_text_escape`
- `is_valid`
- `errors`
- `events`
- `correlation_id`
- `correlation_id_length`
- raw JSON-like summary

Raw technical keys stay in English.

This tab is intentionally separate from Overview so engineering reviewers can inspect the complete raw contract-style shape without making the first screen feel like a debug page.

## Language Modes

The UI supports Traditional Chinese and English display modes. Browser auto-translation is not required.

## Optional Dependency

Streamlit is an optional demo dependency. It is not a Reverb core dependency.

Install the demo dependency from the repository root:

```powershell
python -m pip install -r requirements-demo.txt
```

## Run The Demo

Run from the repository root:

```powershell
$env:PYTHONPATH = "src"
python -m streamlit run .\examples\input_inspector_streamlit.py
```

For the broader public demo flow, see the [Demo Guide](DEMO_GUIDE.md).

## What To Try

- `What!!??`
- whitespace input, such as `   `
- `***Hello world!!!***`
- `Hello world`
- Python `None` object / Type Guard demo

## What To Observe

- human-readable processed text
- `processed_text_escape`
- safe / blocked status
- error codes
- read-only Step Inspector
- changed-only view
- `correlation_id`
- Technical Details
