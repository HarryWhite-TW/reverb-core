# Reverb Core - Deterministic Input Guardrail Layer (v0.7)

> A contract-first, deterministic input preprocessing layer designed to make system behavior observable, traceable, and safe.

## Overview

**Reverb Core** is a backend-oriented engineering project focused on deterministic, contract-first input preprocessing.

`Reverb` / `Reverb Core` is the public project name. `elysia_core` remains the current Python package and module path.

It is not an application and does not perform model inference. It is a foundational guardrail component designed to sit before APIs, NLP systems, or backend services to ensure:

- All inputs return a structured `ProcessingResult`
- Every normal processing step emits a traceable `StepEvent`
- Errors are explicit and machine-readable
- Invalid inputs use structured early returns
- Pipeline execution order is deterministic

## Current Status

Reverb v0.7 has completed two stabilization milestones:

- **M1: Behavior freeze with tests**
  Current observable behavior was frozen with unit, integration, contract, public API, and CLI/e2e tests.
- **M2: Thin modularization**
  The previous preprocessing implementation was split into runner, pipeline, and individual step modules while preserving behavior.

This project is demo-ready as a deterministic input guardrail layer. It does not claim production readiness, reusable package readiness, or a package rename.

## Future Direction

Reverb is intended to evolve toward an embeddable guardrail SDK/package for AI applications, agents, local workbenches, and backend workflows. Beyond raw text preprocessing, the longer-term direction includes validating structured AI task packets before they enter AI-assisted or agent workflows, including task schema, allowed actions, forbidden operations, risk level, approval requirements, `correlation_id` linkage, and audit traceability. Personal Local AI Workbench may become a future consumer or control-plane use case, but it is not part of Reverb v0.7; v0.7 is currently a modular, test-protected preprocessing core, not a finished SDK, completed Workbench integration, or production-ready system.

Planning notes:

- [Reverb v0.7 roadmap](docs/REVERB_V0_7_ROADMAP.md)
- [M1 test freeze summary](docs/REVERB_V0_7_M1_TEST_FREEZE_SUMMARY.md)
- [M2 thin modularization summary](docs/REVERB_V0_7_M2_THIN_MODULARIZATION_SUMMARY.md)

## Demo, API, And Output Documentation

Reverb is currently a modular, test-protected deterministic preprocessing core with a small demo layer and usage documentation.

- [Demo Guide](docs/DEMO_GUIDE.md): how to present Reverb in a short demo.
- [Basic Usage Example](examples/basic_usage.py): runnable Python example for valid input, fallback input, and type guard behavior.
- [API Reference](docs/API_REFERENCE.md): how to call `preprocess_input()` and understand in-memory objects.
- [Output Schema](docs/OUTPUT_SCHEMA.md): how to interpret `ProcessingResult` and CLI JSON output.

These docs do not claim production readiness, SDK completion, package-release readiness, completed Local AI Workbench integration, or completed Task Packet Guardrail implementation. Future SDK and task packet direction remains future work.

## Core Guarantees

Reverb enforces the following invariants:

- Deterministic execution order
- Contract-stable output shape
- Structured early termination
- Explicit error modeling
- Step-level observability

Same input follows the same deterministic processing path and produces the same normalized output, errors, and event sequence, while correlation_id is generated per call.

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
|
strip_spaces
|
trim_edges
|
collapse_spaces
|
fallback_if_empty -- early return if triggered
|
symbol_cleaner
|
ProcessingResult
```

## Quick Start

The CLI is currently invoked through the `elysia_core` module path.

### Run Locally

```bash
python -m elysia_core.cli "Hello   world!!"
```

### Run In JSON Mode

```bash
python -m elysia_core.cli --json "Hello   world!!"
```

### Run With Docker

```bash
docker build -t reverb .
docker run --rm reverb --json "Hello   world!!"
```

## Representative CLI Demo Cases

### Valid Processing With Whitespace Collapse And Symbol Normalization

```bash
python -m elysia_core.cli "Hello   world!!"
```

Expected behavior:

- `collapse_spaces` changes internal spacing
- `symbol_cleaner` normalizes repeated punctuation
- output remains valid

### Mixed Punctuation Normalization In JSON Mode

```bash
python -m elysia_core.cli --json "What!!??"
```

Expected behavior:

- `symbol_cleaner` normalizes mixed punctuation
- output becomes `What！？`
- result remains valid with no errors

### Empty / Whitespace-Only Fallback In JSON Mode

```bash
python -m elysia_core.cli --json "   "
```

Expected behavior:

- `fallback_if_empty` is triggered
- output becomes `…`
- result is invalid with warning-level fallback behavior
- `symbol_cleaner` does not run after fallback

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
      "changed": true,
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

## Edge Cases

| Case | Input                    | Processed text | is_valid | Errors            | Notes                             |
| ---- | ------------------------ | -------------- | -------- | ----------------- | --------------------------------- |
| 01   | `""`                     | `…`            | False    | `EMPTY_INPUT`     | Empty string triggers fallback    |
| 02   | `None`                   | `…`            | False    | `UNEXPECTED_TYPE` | Intercepted by type guard         |
| 03   | `"   "`                  | `…`            | False    | `EMPTY_INPUT`     | Whitespace-only triggers fallback |
| 04   | `"Hello world"`          | `Hello world`  | True     | None              | No modification                   |
| 05   | `" Hello world "`        | `Hello world`  | True     | None              | Strip applied                     |
| 06   | `"***Hello world!!!***"` | `Hello world！` | True     | None              | Trim + symbol normalization       |
| 07   | `"Hello... world"`       | `Hello… world` | True     | None              | Ellipsis normalization            |
| 08   | `"What!!??"`             | `What！？`       | True     | None              | Mixed punctuation normalized      |
| 09   | `123`                    | `…`            | False    | `UNEXPECTED_TYPE` | Non-string input handled safely   |

## Architecture

### Public Entry Point

`src/elysia_core/input/preprocess.py` provides the stable public entry point:

```python
from elysia_core.input.preprocess import preprocess_input
```

It also keeps compatibility imports for the individual step functions used by existing tests and examples.

### Pipeline

`src/elysia_core/input/pipeline.py` owns deterministic orchestration:

- `correlation_id` creation
- event and error collection
- type guard early return
- fallback early return
- `ProcessingResult` construction
- step execution order

### Runner

`src/elysia_core/input/runner.py` owns `run_step`, which:

- Executes a deterministic step function
- Detects whether the step changed the text
- Creates normal info-level `StepEvent` records

### Steps

`src/elysia_core/input/steps/` contains deterministic individual preprocessing steps:

- `strip.py`
- `trim_edges.py`
- `collapse_spaces.py`
- `fallback.py`
- `symbol_cleaner.py`

### Contracts

Contract types are defined in `src/elysia_core/contracts.py`:

- `ProcessingResult`
- `StepEvent`
- `ErrorItem`

All public preprocessing results conform to this contract shape.

## Testing

```bash
pytest -q
```

Testing focuses on:

- Contract shape validation
- Early return behavior
- Deterministic step ordering
- Edge case regression safety
- CLI JSON parseability
- Public API surface stability

Current test layers:

- `01_unit`
- `02_integration`
- `03_contract`
- `04_e2e`

## Regression / Boundary Notes

A permanent regression test protects early-return behavior: when `fallback_if_empty` is triggered, the pipeline must stop before `symbol_cleaner`.

CLI boundary note: `python -m elysia_core.cli --json 123` does not test non-string handling because CLI argv input is passed as a string. Non-string `type_guard` behavior is validated at the `preprocess_input()` / pytest level.

## Docker Verification

The Docker image can be verified against representative JSON cases:

```bash
docker build --no-cache -t reverb .
docker run --rm reverb --json "What!!??"
docker run --rm reverb --json "   "
```

Expected behavior:

- Docker output matches local CLI behavior for symbol normalization
- Docker output matches local CLI behavior for empty-input fallback
- The container demo is reproducible for representative valid and invalid cases

## Scope

This version focuses strictly on:

- Input preprocessing
- Deterministic guardrail logic
- Contract-first architecture
- Observability and traceability
- Thin modularization of the preprocessing core

Out of scope:

- Production-ready claims
- Package rename
- Model inference
- API layer integration
- OpenClaw integration
- Local AI Workbench integration

## Project Structure

```text
src/
  elysia_core/
    contracts.py
    cli.py
    input/
      preprocess.py
      pipeline.py
      runner.py
      steps/
        __init__.py
        strip.py
        trim_edges.py
        collapse_spaces.py
        fallback.py
        symbol_cleaner.py
tests/
  01_unit/
  02_integration/
  03_contract/
  04_e2e/
docs/
  REVERB_V0_7_ROADMAP.md
  REVERB_V0_7_M1_TEST_FREEZE_SUMMARY.md
  REVERB_V0_7_M2_THIN_MODULARIZATION_SUMMARY.md
Dockerfile
README.md
```

---

**Author:** 駿弘  
**Status:** v0.7 - Behavior frozen with tests; thin modularization complete; demo-ready, not production-ready.
