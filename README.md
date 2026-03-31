````md
# Reverb Core — Deterministic Input Guardrail Layer (v0.6)

> A contract-first, deterministic input preprocessing layer designed to make system behavior observable, traceable, and safe.

---

## Overview

**Reverb Core** is a backend-oriented engineering project focused on building a deterministic and contract-first input preprocessing pipeline.

It is not an application.

It is a foundational guardrail component designed to sit before APIs, NLP systems, or backend services to ensure:

- All inputs return a structured `ProcessingResult`
- Every processing step emits a traceable `StepEvent`
- Errors are explicit and machine-readable
- No uncaught exceptions escape the system
- The pipeline execution order is deterministic

---

## Core Guarantees (v0.6)

Reverb enforces the following invariants:

- Deterministic execution order
- Contract-stable output shape
- Structured early termination
- Explicit error modeling
- Step-level observability

Same input → Same output.

---

## Deterministic Pipeline

Execution order:

1. Type validation (`type_guard`)
2. Strip leading/trailing whitespace
3. Trim edge noise
4. Collapse internal spaces
5. Fallback if empty (early return)
6. Symbol normalization
7. Final `ProcessingResult`

```text
Input
↓
strip_spaces
↓
trim_edges
↓
collapse_spaces
↓
fallback_if_empty ──┐ (early return if triggered)
↓                  │
symbol_cleaner     │
↓                  │
ProcessingResult ◀─┘
````

---

## Quick Start

### Run locally

```bash
python -m elysia_core.cli "Hello   world!!"
```

### Run in JSON mode

```bash
python -m elysia_core.cli --json "Hello   world!!"
```

### Run with Docker

```bash
docker build -t reverb .
docker run --rm reverb --json "Hello   world!!"
```

---

## Representative CLI Demo Cases

### Valid processing with whitespace collapse + symbol normalization

```bash
python -m elysia_core.cli "Hello   world!!"
```

Expected behavior:

* `collapse_spaces` changes internal spacing
* `symbol_cleaner` normalizes repeated punctuation
* output remains valid

### Mixed punctuation normalization in JSON mode

```bash
python -m elysia_core.cli --json "What!!??"
```

Expected behavior:

* `symbol_cleaner` normalizes mixed punctuation
* output becomes `What！？`
* result remains valid with no errors

### Empty / whitespace-only fallback in JSON mode

```bash
python -m elysia_core.cli --json "   "
```

Expected behavior:

* `fallback_if_empty` is triggered
* output becomes `…`
* result is invalid with warning-level fallback behavior

---

## Example Output (JSON)

```json
{
  "processed_text": "Hello world！",
  "is_valid": true,
  "errors": [],
  "events": [
    {
      "name": "strip_spaces",
      "changed": false,
      "severity": "info"
    },
    {
      "name": "trim_edges",
      "changed": false,
      "severity": "info"
    },
    {
      "name": "collapse_spaces",
      "changed": false,
      "severity": "info"
    },
    {
      "name": "symbol_cleaner",
      "changed": true,
      "severity": "info"
    }
  ],
  "correlation_id": "..."
}
```

---

## Edge Cases

| Case | Input                    | Processed_text | is_valid | Errors            | Notes                             |
| ---- | ------------------------ | -------------- | -------- | ----------------- | --------------------------------- |
| 01   | `""`                     | `…`            | False    | `EMPTY_INPUT`     | Empty string triggers fallback    |
| 02   | `None`                   | `…`            | False    | `UNEXPECTED_TYPE` | Intercepted by type_guard         |
| 03   | `"   "`                  | `…`            | False    | `EMPTY_INPUT`     | Whitespace-only triggers fallback |
| 04   | `"Hello world"`          | `Hello world`  | True     | None              | No modification                   |
| 05   | `" Hello world "`        | `Hello world`  | True     | None              | Strip applied                     |
| 06   | `"***Hello world!!!***"` | `Hello world！` | True     | None              | Trim + symbol normalization       |
| 07   | `"Hello... world"`       | `Hello… world` | True     | None              | Ellipsis normalization            |
| 08   | `"What!!??"`             | `What！？`       | True     | None              | Mixed punctuation normalized      |
| 09   | `123`                    | `…`            | False    | `UNEXPECTED_TYPE` | Non-string input handled safely   |

---

## Architecture

### Contracts

* `ProcessingResult`
* `StepEvent`
* `ErrorItem`

All outputs conform strictly to the defined contract schema.

### Step Runner

Each processing function is wrapped by `run_step`, which:

* Executes transformation
* Detects state changes
* Emits structured `StepEvent`

---

## Testing

```bash
pytest -q
```

Testing focuses on:

* Contract shape validation
* Early return behavior
* Deterministic step ordering
* Edge case regression safety

### Regression / Boundary Notes

A permanent regression test was added for early-return behavior:
when `fallback_if_empty` is triggered, the pipeline must stop before `symbol_cleaner`.

CLI boundary was also confirmed:
`python -m elysia_core.cli --json 123` does not test non-string handling,
because CLI argv input is passed as string. Non-string `type_guard` behavior
must be validated at the `preprocess_input()` / pytest level instead.

---

## Scope (v0.6)

This version focuses strictly on:

* Input preprocessing
* Deterministic guardrail logic
* Contract-first architecture
* Observability & traceability

Out of scope:

* Model inference
* API layer integration
* Performance optimization

---

## Project Structure

```text
src/
  elysia_core/
    contracts.py
    cli.py
    input/preprocess.py

tests/
Dockerfile
README.md
```

---

**Author:** 駿弘
**Status:** v0.6 — Deterministic Guardrail Layer (Complete Demo Ready)
