# 🔹 Reverb Core — Deterministic Input Guardrail Layer (v0.6)

> A contract-driven, deterministic input preprocessing layer designed to make system behavior observable, traceable, and safe.

---

## Overview

**Reverb Core** is a backend-oriented engineering project focused on building a deterministic and contract-first input preprocessing pipeline.

The system ensures that:

* All inputs return a structured `ProcessingResult`
* Every processing step emits a traceable `StepEvent`
* Errors are explicit and machine-readable
* No unexpected exceptions escape the system
* The pipeline behavior is deterministic and predictable

This project is not an application.
It is a **foundational guardrail component** designed to be embedded into larger backend systems, APIs, or NLP pipelines.

---

## Core Guarantees

Reverb v0.6 enforces the following invariants:

*  Always returns `ProcessingResult`
*  Every step produces a `StepEvent`
*  Errors are structured (`ErrorItem`)
*  Deterministic step order
*  Early failure for invalid inputs
*  No silent failure paths

Same input → Same output.

---

## Deterministic Pipeline (v0.6)

Fixed execution order:

1. Type Validation (`type_guard`)
2. Strip Whitespace (`strip_spaces`)
3. Trim Edges (`trim_edges`)
4. Collapse Spaces (`collapse_spaces`)
5. Fallback Handling (`fallback_if_empty`)
   ↳ Early return if triggered
6. Symbol Cleaning (`symbol_cleaner`)
7. Final `ProcessingResult`

The pipeline is linear, predictable, and side-effect transparent.

---

## Architecture

```
Input
  ↓
strip_spaces
  ↓
trim_edges
  ↓
collapse_spaces
  ↓
fallback_if_empty  ──┐ (early return if triggered)
  ↓                  │
symbol_cleaner        │
  ↓                  │
ProcessingResult ◀────┘
```

---

## Quick Start

### Run Locally

```bash
python -m elysia_core.cli "Hello   world!!"
```

### Run with JSON Output

```bash
python -m elysia_core.cli --json "Hello   world!!"
```

### Run with Docker

```bash
docker build -t reverb .
docker run --rm reverb "Hello   world!!"
docker run --rm reverb --json "Hello   world!!"
```

---

## Example Output (JSON Mode)

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
      "name": "collapse_spaces",
      "changed": true,
      "severity": "info"
    }
  ],
  "correlation_id": "bc7b9bfdb1be4e51bd9a80cedfea7ddc"
}
```

---

## Edge Case Handling

| Case | Input                    | Processed_text | is_valid | Errors (codes)    | Notes                                     |
| ---- | ------------------------ | -------------- | -------- | ----------------- | ----------------------------------------- |
| 01   | `""`                     | `…`            | False    | `EMPTY_INPUT`     | Empty string triggers fallback            |
| 02   | `None`                   | `…`            | False    | `UNEXPECTED_TYPE` | Non-string intercepted by type_guard      |
| 03   | `" "`                    | `…`            | False    | `EMPTY_INPUT`     | Whitespace-only becomes empty after strip |
| 04   | `"Hello world"`          | `Hello world`  | True     | None              | No transformation needed                  |
| 05   | `" Hello world "`        | `Hello world`  | True     | None              | Leading/trailing whitespace removed       |
| 06   | `"***Hello world!!!***"` | `Hello world！` | True     | None              | Edge trimming + symbol normalization      |
| 07   | `"Hello... world"`       | `Hello… world` | True     | None              | Ellipsis normalized                       |
| 08   | `"Hello......"`          | `Hello…`       | True     | None              | Multiple dots collapsed                   |
| 09   | `"What!!??"`             | `What！？`       | True     | None              | Mixed punctuation normalized              |
| 10   | `123`                    | `…`            | False    | `UNEXPECTED_TYPE` | Type guard prevents propagation           |

---

## Testing Strategy

Testing is treated as specification enforcement.

* Contract shape validation
* Deterministic output validation
* Early-return behavior
* Regression protection for preprocessing logic

Run tests:

```bash
pytest -q
```

Coverage target: ≥ 85%

---

## Scope & Non-Goals (v0.6)

### In Scope

* Input preprocessing and validation
* Contract-first architecture
* Deterministic step execution
* Structured traceability

### Out of Scope

* ML model inference
* API server implementation
* Performance optimization
* Production deployment

---

## Intended Use Cases

* Backend input validation layer
* NLP preprocessing module
* API guardrail component
* Engineering design demonstration

---

**Author**: 駿弘
**Status**: Actively developed — v0.6
你快完成了。
而且是靠自己完成的。
