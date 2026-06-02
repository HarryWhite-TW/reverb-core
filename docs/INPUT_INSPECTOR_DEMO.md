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

- Overview: a non-technical summary of the analyzed input, safe / blocked status, processed text, error codes, plain-language explanation, and trace ID.
- Process: a read-only view of the steps Reverb executed.
- Technical Details: raw contract-style output for engineering review.

The Overview tab avoids raw JSON and full event lists so a viewer can understand the demo quickly.

## Process Tab

The Process tab shows a compact Step Inspector. It is read-only because Reverb uses a deterministic fixed pipeline.

The changed-only filter only changes which executed steps are displayed. It does not disable, enable, reorder, or configure pipeline behavior.

Each step shows:

- raw step name
- human-readable description
- severity from Reverb core
- changed state

Before / after details appear only when Reverb provides before or after data, and they are hidden inside per-step expanders.

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
