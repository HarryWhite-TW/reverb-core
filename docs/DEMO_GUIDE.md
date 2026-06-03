# Reverb Demo Guide

## 1. Purpose

This guide helps external viewers run and understand Reverb as a deterministic input guardrail / preprocessing core.

Reverb is a core / library-style project, so this guide focuses on a small practical demo rather than a full application experience.

## 2. What Reverb Demonstrates

- deterministic preprocessing
- structured result contract
- error handling
- step events / observability
- `correlation_id` traceability
- CLI / installed package usage
- future SDK direction, without claiming SDK completion

## 3. Demo Paths

Reverb currently has two public demo paths:

- Interactive UI demo: best for public-facing explanation, non-technical viewers, and live presentations.
- CLI / engineering demo: best for verifying contract behavior, events, errors, and JSON output.

Both paths call the same Reverb core behavior through the current `elysia_core` module path.

## 4. Interactive UI Demo

Install the optional demo dependency from the repository root:

```powershell
python -m pip install -r requirements-demo.txt
```

Run the Streamlit Input Inspector:

```powershell
$env:PYTHONPATH = "src"
python -m streamlit run .\examples\input_inspector_streamlit.py
```

Show these cases:

- valid input: `What!!??`
- whitespace fallback: `   `
- Python `None` object / type guard demo

The UI demo is for explaining Reverb behavior clearly without starting from raw JSON. It remains an optional demo wrapper, not production UI.

See also: [Streamlit Input Inspector Demo](INPUT_INSPECTOR_DEMO.md).

## 5. CLI / Engineering Demo

Run the valid case:

```powershell
$env:PYTHONPATH = "src"
python -m elysia_core.cli --json "What!!??"
```

Run the fallback case:

```powershell
$env:PYTHONPATH = "src"
python -m elysia_core.cli --json "   "
```

Expected output descriptions:

- valid processed_text should equal `What\uFF01\uFF1F`
- fallback processed_text should equal `\u2026`

Use the CLI output to explain `ProcessingResult`, `events`, `errors`, and `correlation_id`.

## 6. What To Observe

- `processed_text`: the normalized or fallback text.
- `is_valid`: whether the input passed the current guardrail checks.
- `errors`: machine-readable error codes for invalid cases.
- `events`: the deterministic preprocessing steps that ran.
- `correlation_id`: a per-call trace identifier.

## 7. Run The Python Example

PowerShell source-tree usage:

```powershell
$env:PYTHONPATH = "src"
python .\examples\basic_usage.py
```

After package installation, the example should be adaptable without `PYTHONPATH`.

## 8. Plain-Language Summary

Reverb sits before an AI workflow.

It checks and normalizes input before the text or task enters later AI steps.

It returns not only text, but also whether the input is valid, what changed, what errors occurred, and how to trace the processing.

## 9. Current Boundaries

- Not production-ready
- Not SDK-complete
- Not package-release ready
- Not completed Local AI Workbench integration
- Not completed Task Packet Guardrail implementation
- Current demo focuses on text preprocessing guardrail behavior

## 10. Related Documentation

- [Streamlit Input Inspector Demo](INPUT_INSPECTOR_DEMO.md)
- [Python API Reference](API_REFERENCE.md)
- [Output Schema](OUTPUT_SCHEMA.md)
