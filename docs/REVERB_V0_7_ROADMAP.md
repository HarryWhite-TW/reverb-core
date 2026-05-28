# Reverb Core v0.7 Roadmap

This document defines the next development direction after Reverb Core v0.6.

It is intentionally a planning document. It does not implement architecture changes, does not rename packages, and does not claim production readiness.

## 1. Current State

Reverb Core v0.6 is a deterministic input guardrail layer.

Its purpose is to accept untrusted input, run it through a predictable preprocessing pipeline, and always return a stable structured result. It is not a chatbot, not an application, and not a model inference system.

Current strengths:

* `ProcessingResult` provides a stable output envelope.
* `StepEvent` records step-level observability.
* `ErrorItem` provides structured error reporting.
* The pipeline follows a deterministic execution order.
* Invalid inputs return structured fallback results.
* CLI execution is available.
* Docker execution is available.
* Pytest layers exist for unit, integration, contract, and e2e validation.

Current status:

* v0.6 is demo-ready.
* v0.6 is suitable for portfolio explanation and engineering demonstration.
* v0.6 is not yet production-ready.
* v0.6 is not yet reusable-package-ready.

## 2. Gap Assessment

Approximate current readiness:

* Ideal usable: 65%
* Modularization: 45%
* Reusable in other products: 40%

### Ideal usability gap

The project can already demonstrate its core behavior, but it still needs better stabilization, clearer documentation, stronger CI/release discipline, and more explicit usage boundaries before it can be considered broadly usable.

### Modularization gap

The current implementation has a stable contract and useful test layers, but the internal responsibilities are still too concentrated. v0.7 should separate pipeline orchestration, step execution, and individual step logic without changing behavior.

### Reuse-in-other-products gap

The project is not yet ready to be consumed as a clean reusable package. It still needs public API stabilization, package metadata, CI, integration examples, and clearer output schema documentation.

## 3. v0.7 Goal: Thin Modularization

The v0.7 goal is thin modularization.

This means:

* Split responsibilities without overengineering.
* Preserve existing behavior.
* Preserve current contracts.
* Preserve current CLI behavior unless explicitly approved.
* Avoid plugin systems, framework-like abstractions, or premature package rename.
* Make the codebase easier to test, review, and extend.

v0.7 should focus on reorganizing existing responsibilities, not expanding product scope.

Target responsibility separation:

* `preprocess.py`: public entry point and compatibility surface.
* `pipeline.py`: deterministic pipeline orchestration.
* `runner.py`: reusable step execution and `StepEvent` creation.
* `steps/`: individual deterministic preprocessing steps.

The main design rule for v0.7:

> Same input should produce the same observable result before and after modularization.

## 4. v0.8 Goal: Reusable Package Readiness

The v0.8 goal is reusable package readiness.

This phase should only start after v0.7 has stabilized internal module boundaries.

Expected v0.8 planning areas:

* Public API export.
* `pyproject.toml`.
* GitHub Actions CI.
* Package usage documentation.
* Integration examples.
* Improved CLI JSON schema.
* Versioning and release notes.
* Clear install instructions.

v0.8 may prepare Reverb Core for external package-style consumption, but production readiness must still be validated separately.

## 5. Non-goals

The following are explicitly out of scope for v0.7:

* No model inference.
* No LLM prompt orchestration.
* No multi-agent orchestration.
* No OpenClaw integration.
* No Local AI Workbench integration yet.
* No package rename.
* No production-ready claim.
* No plugin system.
* No large framework abstraction.
* No broad product expansion.

The current package path `elysia_core` must remain unchanged during v0.7.

Any future rename to `reverb_core` must be handled as a separate approved migration.

## 6. Target Structure

Proposed future directory structure, not yet implemented:

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
          type_guard.py
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
```

The exact file names may still be reviewed during implementation, but v0.7 should preserve the current package path `elysia_core`.

A rename from `elysia_core` to `reverb_core` is not part of v0.7. If needed, it must be handled as a separate approved migration after modularization is stable.

## 7. Verification Strategy

Before modularization, existing behavior should be frozen through tests.

Required verification commands:

```powershell
pytest -q
python -m elysia_core.cli --json "What!!??"
python -m elysia_core.cli --json "   "
```

Docker verification should remain part of the final validation path:

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

## 8. AI-assisted Workflow Rules

Codex may assist with:

* File moves.
* Test scaffolds.
* Repeated refactors.
* README drafts.
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

## 9. Milestone Plan

### M0: Add roadmap document

Goal:

* Add this roadmap as a docs-only planning artifact.

Expected result:

* `docs/REVERB_V0_7_ROADMAP.md` exists.
* No source code changes.
* No test changes.
* No package changes.

### M1: Freeze current behavior with tests

Goal:

* Strengthen tests before refactoring.

Expected result:

* Current behavior is protected before modularization.
* Contract, fallback, type guard, symbol normalization, and CLI JSON behavior are covered.

### M2: Extract runner and steps

Goal:

* Move `run_step()` and individual step functions into clearer modules.

Expected result:

* Step execution logic is separated.
* Individual preprocessing steps are easier to review and test.
* Public behavior remains unchanged.

### M3: Extract pipeline orchestration

Goal:

* Separate deterministic pipeline orchestration from the public entry point.

Expected result:

* `preprocess_input()` remains the stable entry point.
* Pipeline flow becomes easier to understand.
* Existing tests continue passing.

### M4: Update CLI imports if needed

Goal:

* Keep CLI behavior stable after internal module changes.

Expected result:

* `python -m elysia_core.cli --json "What!!??"` still works.
* CLI JSON behavior remains representative and testable.

### M5: Update documentation

Goal:

* Update README and docs only after verified behavior changes.

Expected result:

* Documentation matches actual behavior.
* No unverified claims are introduced.

### M6: Prepare package-readiness checklist

Goal:

* Prepare for v0.8 without starting package migration prematurely.

Expected result:

* Public API, package metadata, CI, and integration-example needs are listed for v0.8.

## 10. Definition of Done

This roadmap task is complete when:

* `docs/REVERB_V0_7_ROADMAP.md` exists.
* Only the roadmap document is changed.
* No source code is changed.
* No tests are changed.
* No README, Dockerfile, setup.py, pyproject.toml, or CI files are changed.
* The document clearly separates v0.7 and v0.8.
* The document preserves `elysia_core` as the v0.7 package path.
* The document does not imply package rename during v0.7.
* The document does not introduce OpenClaw integration.
* The document does not introduce Local AI Workbench integration.
* The document does not claim production readiness.
