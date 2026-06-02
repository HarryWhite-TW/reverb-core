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

## 3. Three-Minute Demo Flow

1. Show valid input `"What!!??"`.
2. Show fallback input `"   "`.
3. Show unexpected type input such as `None` through the Python example.
4. Explain `processed_text`, `is_valid`, `errors`, `events`, and `correlation_id`.

The main point is that Reverb returns a structured processing result, not just modified text.

## 4. What To Observe

- `processed_text`: the normalized or fallback text.
- `is_valid`: whether the input passed the current guardrail checks.
- `errors`: machine-readable error codes for invalid cases.
- `events`: the deterministic preprocessing steps that ran.
- `correlation_id`: a per-call trace identifier.

## 5. Run The Python Example

PowerShell source-tree usage:

```powershell
$env:PYTHONPATH = "src"
python .\examples\basic_usage.py
```

After package installation, the example should be adaptable without `PYTHONPATH`.

## 6. Run CLI Demo

PowerShell source-tree usage:

```powershell
$env:PYTHONPATH = "src"
python -m elysia_core.cli --json "What!!??"
python -m elysia_core.cli --json "   "
```

Expected output descriptions:

- valid processed_text should equal `What\uFF01\uFF1F`
- fallback processed_text should equal `\u2026`

## 7. Plain-Language Summary

Reverb sits before an AI workflow.

It checks and normalizes input before the text or task enters later AI steps.

It returns not only text, but also whether the input is valid, what changed, what errors occurred, and how to trace the processing.

## 8. Current Boundaries

- Not production-ready
- Not SDK-complete
- Not a full UI app
- Not Local AI Workbench integration
- Not Task Packet Guardrail implementation yet
- Current demo focuses on text preprocessing guardrail behavior

## 9. Next Demo Improvements

- output schema docs
- API reference
- more example cases
- small input inspector UI later
- Task Packet Guardrail demo later
