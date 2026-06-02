# Reverb v0.8 Package Data Implementation Plan

## 1. Purpose

This document plans future package-data handling for `src/elysia_core/config/default.json`.

It is a planning document only. It does not modify package configuration, source code, tests, or claim package readiness.

## 2. Current Behavior

`load_default_config()` loads `default.json` from the same directory as `config_loader.py`.

This works in the source tree because `default.json` exists beside the module.

The preprocessing pipeline and CLI do not currently appear to depend on `load_default_config()` directly.

## 3. Current Risk

`default.json` is non-Python package data.

Current `setup.py` does not declare `package_data`, `include_package_data`, `data_files`, `MANIFEST.in`, or `pyproject.toml` package-data configuration.

Future installed builds may omit `default.json`.

Public API and CLI smoke checks may still pass even if `load_default_config()` breaks.

## 4. Expected Failure Mode

If `default.json` is omitted after install, `load_default_config()` may raise `FileNotFoundError` for `elysia_core/config/default.json`.

## 5. Implementation Options

| Option | Benefit | Risk / Tradeoff |
| --- | --- | --- |
| Add `package_data` in `setup.py` later | Smallest change while `setup.py` remains active | Keeps packaging behavior in legacy configuration |
| Add package-data configuration in `pyproject.toml` later | Aligns with future modern package configuration | Should wait until minimal `pyproject.toml` scope is separately approved |
| Use `importlib.resources` later | More robust resource loading if config loading becomes a formal public contract | Requires a source-code change and separate approval |
| Defer package-data handling | Avoids implementation if `load_default_config()` is not supported after install | Leaves a known installed-package risk if the function remains supported |

## 6. Recommended Future Approach

- Treat `default.json` as package data if `load_default_config()` remains supported after install.
- Handle package-data support before or together with minimal `pyproject.toml`.
- Keep module path as `elysia_core`.
- Do not rename package.
- Add install verification that calls `load_default_config()` after installation.
- Consider `importlib.resources` in a later source-code task only if approved.

## 7. Future Verification Commands

Future install verification commands:

```powershell
python -m pip install .
python -c "from elysia_core.config.config_loader import load_default_config; print(type(load_default_config()).__name__)"
python -c "from elysia_core.input.preprocess import preprocess_input; result = preprocess_input('What!!??'); print(result.processed_text)"
python -m elysia_core.cli --json "What!!??"
python -m elysia_core.cli --json "   "
```

Expected output wording:

- `load_default_config()` should return a `dict`.
- processed_text should equal `What\uFF01\uFF1F`
- fallback processed_text should equal `\u2026`

## 8. Test Coverage Gap

Current tests cover source-tree config loading.

Current tests do not verify installed package context or wheel install context.

Future install verification should run before any package-readiness claim.

## 9. Proposed Future Implementation Scope

A future separately approved implementation task may allow changes to:

- `setup.py` or `pyproject.toml`
- possibly `MANIFEST.in` if chosen
- possibly tests or docs for install verification

This current document does not approve that implementation.

## 10. Non-goals

- no `setup.py` change
- no `pyproject.toml` creation
- no source changes
- no test changes
- no package rename
- no production-ready claim
- no SDK-complete claim
- no Local AI Workbench integration
- no OpenClaw integration

## 11. Suggested Next Step

Recommended next step: create a future human-approved minimal package-data/package-config implementation task.

Implementation should be blocked until package metadata decisions and the install verification plan are reviewed.
