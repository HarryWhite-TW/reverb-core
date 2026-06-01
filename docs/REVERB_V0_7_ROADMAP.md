# Reverb Core v0.7 Roadmap

This document tracks the v0.7 direction after Reverb Core v0.6 and records the current post-M1/M2/M3-B state.

It is intentionally a planning document. It does not rename packages, does not claim production readiness, and does not describe completed SDK or Workbench integration.

## 1. Current State

Reverb Core v0.7 is a deterministic input guardrail and preprocessing core.

Its purpose is to accept untrusted input, run it through a predictable preprocessing pipeline, and always return a stable structured result. It is not a chatbot, not an application, and not a model inference system.

Current strengths:

* `ProcessingResult` provides a stable output envelope.
* `StepEvent` records step-level observability.
* `ErrorItem` provides structured error reporting.
* The pipeline follows a deterministic execution order.
* Invalid inputs return structured fallback results.
* CLI execution is available.
* Docker execution is available.
* Pytest layers exist for unit, integration, contract, public API, and e2e validation.
* M1 froze observable behavior with tests.
* M2 completed thin modularization of runner, steps, and pipeline orchestration.
* M3-B aligned the README with the current v0.7 state.

Current status:

* v0.7 is demo-ready as a deterministic guardrail layer.
* v0.7 is suitable for engineering review, CLI demonstration, and future SDK/package-readiness planning.
* v0.7 is modular and test-protected.
* v0.7 is not production-ready.
* v0.7 is not reusable-package-ready.
* v0.7 is not a completed SDK.

## 2. Gap Assessment

Approximate current readiness after M1/M2/M3-B:

* Demo / engineering usability: high for the current v0.7 scope.
* Modularization: largely complete for thin modularization.
* Reuse in other products: structurally prepared, but not package-ready or SDK-complete yet.

### Ideal usability gap

The project can demonstrate its core behavior and internal boundaries clearly. Remaining v0.7 work should focus on documentation alignment, demo verification, and package-readiness planning without expanding scope.

### Modularization gap

The main v0.7 thin modularization goal is complete. `preprocess.py`, `pipeline.py`, `runner.py`, and `steps/` now have clearer responsibilities. Optional future cleanup may review whether type guard logic should remain in `pipeline.py` or move into a dedicated module, but that is deferred and not required for v0.7 completion.

### Reuse-in-other-products gap

The project is not yet ready to be consumed as a clean reusable package. It still needs package metadata review, public API documentation, CI planning, integration examples, and clearer versioning/release guidance before v0.8 package-readiness work begins.

## 3. v0.7 Goal: Thin Modularization And Documentation Alignment

The v0.7 goal is thin modularization plus alignment of the public docs with the completed internal structure.

This means:

* Split responsibilities without overengineering.
* Preserve existing behavior.
* Preserve current contracts.
* Preserve current CLI behavior unless explicitly approved.
* Avoid plugin systems, framework-like abstractions, or premature package rename.
* Make the codebase easier to test, review, and extend.
* Keep README and roadmap wording aligned with actual implementation.

v0.7 focuses on reorganizing existing responsibilities and explaining the result, not expanding product scope.

Current responsibility separation:

* `preprocess.py`: public entry point and compatibility surface.
* `pipeline.py`: deterministic pipeline orchestration, early returns, `correlation_id` creation, event/error collection, and `ProcessingResult` construction.
* `runner.py`: reusable step execution and normal info-level `StepEvent` creation.
* `steps/`: individual deterministic preprocessing steps.

The main design rule for v0.7 remains:

> Same input follows the same deterministic processing path and produces the same normalized output, errors, and event sequence, while `correlation_id` is generated per call.

## 4. Longer-Term Direction

Reverb may evolve toward an embeddable guardrail SDK/package for AI applications, agents, local workbenches, or backend workflows.

Future directions may include validating structured AI task packets before they enter AI-assisted or agent workflows. Potential task validation areas include task schema, allowed actions, forbidden operations, risk level, approval requirements, `correlation_id` linkage, and audit traceability.

Personal Local AI Workbench may become a future consumer or control-plane use case for Reverb. It is not part of Reverb v0.7, and no Workbench integration is complete in the current project.

## 5. v0.8 Goal: Reusable Package Readiness

The v0.8 goal is reusable package readiness.

This phase should only start after v0.7 documentation and demo readiness are stable.

Expected v0.8 planning areas:

* Public API export.
* `pyproject.toml`.
* GitHub Actions CI.
* Package usage documentation.
* Integration examples.
* Improved CLI JSON schema documentation.
* Versioning and release notes.
* Clear install instructions.

v0.8 may prepare Reverb Core for external package-style consumption, but production readiness must still be validated separately.

## 6. Non-goals

The following are explicitly out of scope for v0.7:

* No model inference.
* No LLM prompt orchestration.
* No multi-agent orchestration.
* No OpenClaw integration.
* No completed Local AI Workbench integration.
* No package rename.
* No production-ready claim.
* No completed SDK claim.
* No package-ready claim.
* No plugin system.
* No large framework abstraction.
* No broad product expansion.

The current package path `elysia_core` must remain unchanged during v0.7.

Any future rename to `reverb_core` must be handled as a separate approved migration and is not proposed for v0.7.

## 7. Current Module Structure

Implemented v0.7 structure:

```text
reverb-core/
  src/
    elysia_core/
      __init__.py
      contracts.py
      cli.py
      input/
        __init__.py
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
```

`type_guard` currently remains inside `pipeline.py` because it is orchestration-level early-return behavior. Extracting it into a dedicated `type_guard.py` step module is deferred and optional.

## 8. Verification Strategy

M1 froze behavior before modularization. M2 and M3-B preserved that behavior while improving structure and docs.

Core validation commands:

```powershell
python -m pytest -q --basetemp=.\.pytest_tmp -p no:cacheprovider
$env:PYTHONPATH = "src"
python -m elysia_core.cli --json "What!!??"
python -m elysia_core.cli --json "   "
```

Docker verification remains useful for final demo refresh:

```powershell
docker build -t reverb .
docker run --rm reverb --json "What!!??"
docker run --rm reverb --json "   "
```

Behavior that must remain stable:

* `ProcessingResult` structure.
* `correlation_id` format.
* `original_input` preservation.
* `processed_text` output for representative inputs.
* `is_valid` behavior.
* `StepEvent` names, severity, and changed status.
* `ErrorItem` code, step, and severity.
* `type_guard` early return behavior.
* `fallback_if_empty` early return behavior.
* `symbol_cleaner` representative normalization cases.
* CLI JSON output for representative cases.

## 9. AI-assisted Workflow Rules

Codex may assist with:

* File moves.
* Test scaffolds.
* Repeated refactors.
* README drafts.
* Roadmap alignment.
* Mechanical import updates.
* Candidate diffs.

The human owner must approve:

* Architecture boundaries.
* Contract changes.
* Public API changes.
* Package rename decisions.
* Merge readiness.
* Any production-readiness claim.

Required rules for AI-assisted changes:

* Verify repository identity before any file modification.
* Restrict allowed files for each task.
* Preserve forbidden-file boundaries.
* Do not stage, commit, or push unless explicitly instructed.
* Keep each Codex task scoped to one repository.
* Do not use one VS Code workspace for simultaneous multi-repo Codex edits.
* Any Codex-generated change must be explainable by the owner before entering the main branch.

For Reverb tasks, the expected remote is:

```text
https://github.com/HarryWhite-TW/reverb-core.git
```

The local folder name may differ between environments. Repository identity should be verified primarily by Git remote URL, not by local folder name.

## 10. Milestone Plan

### M0: Add roadmap document

Status: Complete.

Result:

* `docs/REVERB_V0_7_ROADMAP.md` exists.
* No source code changes were introduced by M0.

### M1: Freeze current behavior with tests

Status: Complete.

Result:

* Current behavior is protected before modularization.
* Contract, fallback, type guard, symbol normalization, public API surface, and CLI JSON behavior are covered.
* Summary: `docs/REVERB_V0_7_M1_TEST_FREEZE_SUMMARY.md`.

### M2: Thin modularization

Status: Complete.

Result:

* `runner.py` owns `run_step`.
* Individual deterministic steps live under `steps/`.
* `pipeline.py` owns deterministic preprocessing orchestration.
* `preprocess_input()` remains the stable public entry point.
* Existing tests continued passing after each extraction.
* Summary: `docs/REVERB_V0_7_M2_THIN_MODULARIZATION_SUMMARY.md`.

### M3: Documentation alignment and demo readiness

Status: In progress.

Completed:

* README aligned with v0.7 current state and modular architecture.

In progress:

* Roadmap alignment with completed M1/M2/M3-B state.

Remaining possible M3 work:

* Demo verification refresh.
* Docker verification refresh.
* Package-readiness checklist planning.
* Final v0.7 closeout summary if useful.

### M4: Package-readiness planning

Status: Future planning.

Goal:

* Prepare for v0.8 without starting package migration prematurely.

Expected result:

* Public API, package metadata, CI, versioning, and integration-example needs are listed for v0.8.

## 11. Definition of Done For Current Roadmap Alignment

This roadmap alignment task is complete when:

* `docs/REVERB_V0_7_ROADMAP.md` reflects completed M1 and M2 work.
* README v0.7 alignment is reflected as completed.
* Current module responsibilities match the implemented code.
* `type_guard` is documented as currently inside `pipeline.py`.
* Future direction is preserved without overclaiming.
* No source code is changed.
* No tests are changed.
* No README, Dockerfile, setup.py, pyproject.toml, or CI files are changed.
* The document preserves `elysia_core` as the v0.7 package path.
* The document does not propose package rename during v0.7.
* The document does not claim production readiness.
* The document does not claim completed SDK or Workbench integration.
