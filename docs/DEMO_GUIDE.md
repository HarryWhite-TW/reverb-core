# Reverb Demo Guide

## 1. Purpose

This guide helps demonstrate Reverb as a deterministic input guardrail / preprocessing core.

Reverb is a core / library-style project, so this guide provides a demo wrapper for humans who need to understand the behavior quickly.

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

## 4. Run The Python Example

PowerShell source-tree usage:

```powershell
$env:PYTHONPATH = "src"
python .\examples\basic_usage.py
```

After package installation, the example should be adaptable without `PYTHONPATH`.

## 5. Run CLI Demo

PowerShell source-tree usage:

```powershell
$env:PYTHONPATH = "src"
python -m elysia_core.cli --json "What!!??"
python -m elysia_core.cli --json "   "
```

Expected output descriptions:

- valid processed_text should equal `What\uff01\uff1f`
- fallback processed_text should equal `\u2026`

## 6. How To Explain This To Non-Specialists

Reverb sits before an AI workflow.

It checks and normalizes input before the text or task enters later AI steps.

It returns not only text, but also whether the input is valid, what changed, what errors occurred, and how to trace the processing.

## 7. Current Boundaries

- Not production-ready
- Not SDK-complete
- Not a full UI app
- Not Local AI Workbench integration
- Not Task Packet Guardrail implementation yet
- Current demo focuses on text preprocessing guardrail behavior

## 8. Suggested Presenter Script

"Reverb is a deterministic preprocessing guardrail. I can give it normal text, messy text, empty input, or even the wrong input type, and it always returns the same structured result shape. That result tells us the processed text, whether the input is valid, which errors occurred, which steps ran, and a correlation ID for traceability. This is not the full future SDK yet, but it shows the core guardrail behavior clearly."

## 9. Next Demo Improvements

- output schema docs
- API reference
- more example cases
- small input inspector UI later
- Task Packet Guardrail demo later
