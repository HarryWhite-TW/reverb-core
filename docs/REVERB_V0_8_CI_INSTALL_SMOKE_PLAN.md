# Reverb v0.8 CI Install Smoke Plan

## 1. Purpose

This plan records how Reverb should eventually add CI install smoke checks after isolated source snapshot install verification and isolated wheel build/install verification have passed.

This is a planning document, not CI implementation. It does not add GitHub Actions workflow files, does not change package configuration, and does not expand Reverb's readiness claims.

## 2. Current Context

Current verified evidence:

- source snapshot install verification passed
- wheel build and wheel install verification passed
- public API import passed through `elysia_core.input.preprocess.preprocess_input`
- contract imports passed for `ProcessingResult`, `StepEvent`, and `ErrorItem`
- CLI valid and fallback checks passed after install
- `load_default_config()` package data loading passed after install
- `default.json` was available in installed package contexts
- Streamlit remains a demo-only dependency and was not installed as a core dependency
- package readiness closeout exists

Reverb is currently an installable deterministic preprocessing core with verified representative package behavior. It is not yet backed by CI install smoke checks.

## 3. CI Goals

Future CI should verify:

- source-tree tests
- CLI smoke checks
- source install smoke
- wheel build and wheel install smoke
- package data loading
- Streamlit is not a core dependency

The goal is to catch regressions in core behavior, installability, and package boundary without turning CI into a release pipeline.

## 4. Recommended CI Job Structure

### Core Test Job

Purpose:

- verify source-tree behavior and existing test coverage

Suggested checks:

- install test dependencies
- run `pytest`
- run CLI valid smoke from source context
- run CLI fallback smoke from source context

Representative CLI cases:

- `python -m elysia_core.cli --json "What!!\u003F\u003F"`
- `python -m elysia_core.cli --json "   "`

### Source Install Smoke Job

Purpose:

- verify that the package can be installed from repository source and used outside source-tree import assumptions

Suggested checks:

- create a clean virtual environment
- install package from repo source
- verify public API import
- verify contract imports
- verify CLI valid case
- verify CLI fallback case
- verify `load_default_config()`

Expected boundaries:

- package name remains `elysia_core`
- public entry point remains `elysia_core.input.preprocess.preprocess_input`
- fallback input returns `EMPTY_INPUT`
- default config loads as installed package data

### Wheel Install Smoke Job

Purpose:

- verify that a built wheel contains the expected package modules and package data

Suggested checks:

- build wheel
- create a clean virtual environment
- install wheel into that clean environment
- verify public API import
- verify contract imports
- verify CLI valid case
- verify CLI fallback case
- verify `load_default_config()`
- verify Streamlit is not installed as a core dependency

Expected boundaries:

- installed import resolves from the clean environment, not the source checkout
- wheel includes `elysia_core/config/default.json`
- core install does not pull in Streamlit

## 5. What Not To Put In Core CI Yet

Core CI should not yet:

- run the Streamlit UI demo
- require Docker if Docker is not stable in the CI environment
- publish a package
- upload artifacts as release assets
- add package metadata decisions
- claim package-release readiness
- make the CLI a console script
- implement Task Packet Guardrail
- implement Local AI Workbench integration

Streamlit and Docker can be considered later as separate demo or environment checks if human-approved.

## 6. Risk Notes

Risks to account for during future CI implementation:

- CI can create false confidence if it only tests source-tree behavior.
- Build artifacts or cache files can pollute the repository if cleanup is not explicit.
- Streamlit could accidentally become a core dependency if dependency boundaries are not checked.
- A wheel can pass import checks while still missing package data unless `load_default_config()` is tested.
- CI existence can lead to overclaiming SDK completeness or package-release readiness.
- Windows and Linux may differ in path handling, shell quoting, encoding, or package build behavior.

## 7. Human Decisions Required Before CI Implementation

Before implementing CI, humans should decide:

- whether CI should run on `push`, `pull_request`, or both
- which Python versions to test
- whether to include Windows, Linux, or both
- whether pytest dependency installation should use a requirements file or direct install
- whether wheel build should be required on every push
- whether install smoke should block merges
- whether the Streamlit demo should get a separate non-blocking check later

These decisions should be made before adding workflow files or expanding package claims.

## 8. Recommended Immediate Next Implementation

Recommended first implementation:

- add a minimal GitHub Actions workflow for core `pytest` plus CLI valid/fallback smoke checks

Then, in a separate commit, add source install and wheel install smoke checks.

This sequence is recommended because it keeps the first CI change small, makes failures easier to debug, and avoids putting all CI complexity into one change.

## 9. Boundaries

This plan does not mean:

- CI has been implemented
- Reverb is production-ready
- Reverb is SDK-complete
- Reverb is package-release ready
- public metadata is complete

It also does not approve package rename, package publishing, console script implementation, Task Packet Guardrail implementation, Local AI Workbench integration, or Streamlit as a core dependency.
