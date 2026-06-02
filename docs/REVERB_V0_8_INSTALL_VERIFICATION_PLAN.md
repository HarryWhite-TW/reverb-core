# Reverb v0.8 Install Verification Plan

## 1. Purpose

This document defines future install verification before package configuration changes.

It is a planning document only. It does not implement package configuration, does not create `pyproject.toml`, and does not claim package readiness.

## 2. Current Context

Reverb v0.7 is closed as a modular, test-protected deterministic preprocessing core.

Reverb v0.8 is package-readiness planning.

The current module path remains `elysia_core`.

The current stable public API is `elysia_core.input.preprocess.preprocess_input`.

Current contracts are `ProcessingResult`, `StepEvent`, and `ErrorItem`.

The CLI currently works through `python -m elysia_core.cli`.

Docker is reproducible demo support, not production deployment.

Reverb may move toward a future embeddable guardrail SDK / task packet validation layer, but that direction remains future work.

## 3. Verification Goals

- Verify package can be installed in a clean environment.
- Verify public API import works after install.
- Verify `preprocess_input()` behavior after install.
- Verify CLI module execution after install.
- Verify `config/default.json` or default config loading if package data is required.
- Verify tests or representative smoke checks can run after install.
- Verify no package rename is introduced.

## 4. Suggested Clean Environment Strategy

Future install verification can use a temporary clean environment:

```powershell
python -m venv .venv-install-check
.\.venv-install-check\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install .
```

The temporary environment should be removed after verification and should not be committed.

## 5. Public API Import Check

Future command:

```powershell
python -c "from elysia_core.input.preprocess import preprocess_input; result = preprocess_input('What!!??'); print(result.processed_text)"
```

Expected output:

- processed_text equals `What\uFF01\uFF1F`

## 6. Contract Import Check

Future command:

```powershell
python -c "from elysia_core.contracts import ProcessingResult, StepEvent, ErrorItem; print(ProcessingResult.__name__, StepEvent.__name__, ErrorItem.__name__)"
```

Expected:

- imports succeed without error

## 7. CLI Module Check

Future commands:

```powershell
python -m elysia_core.cli --json "What!!??"
python -m elysia_core.cli --json "   "
```

Expected:

- valid case returns processed_text `What\uFF01\uFF1F`, `is_valid=true`, no errors, and `symbol_cleaner` event
- fallback case returns processed_text `\u2026`, `is_valid=false`, `EMPTY_INPUT`, and no `symbol_cleaner` event

## 8. Package Data / Default Config Check

`src/elysia_core/config/default.json` may require package-data handling.

Future install verification should check whether `load_default_config()` works after install.

Do not implement package-data configuration in this task.

Future command, if installed package support for this function is required:

```powershell
python -c "from elysia_core.config.config_loader import load_default_config; print(type(load_default_config()).__name__)"
```

Expected:

- default config loads successfully, if installed package support for this function is required

## 9. Build / Wheel Verification Later

Future checks after package configuration exists:

- build sdist/wheel after package config exists
- install from wheel into a clean environment
- repeat public API, CLI, and package-data checks from wheel install

Wheel verification is not required before package configuration is implemented.

## 10. Success Criteria

- clean environment install succeeds
- public API import succeeds
- contract imports succeed
- representative `preprocess_input()` result matches current behavior
- CLI module works after install
- fallback behavior remains intact
- `config/default.json` behavior is either verified or explicitly documented as not required
- no package rename
- no production-ready or SDK-complete claim

## 11. Failure Criteria

- install fails
- imports only work from source checkout but not installed package
- CLI fails after install
- package data missing breaks default config loading
- package rename or path drift occurs
- test/demo behavior changes after install

## 12. Non-goals

- no source changes
- no test changes
- no `setup.py` modification
- no `pyproject.toml` creation
- no CI implementation
- no package rename
- no production-ready claim
- no completed SDK claim
- no Local AI Workbench integration
- no OpenClaw integration

## 13. Suggested Next Step

Recommended next step: perform a future read-only package data audit before implementing package configuration.

Any install verification implementation or package configuration change must be separately approved.
