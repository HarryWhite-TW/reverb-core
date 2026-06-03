# Reverb v0.8 Compatibility Policy Draft

## 1. Purpose

This document is a draft compatibility policy for Reverb v0.8 after CI-backed core smoke checks, source install smoke checks, and wheel install smoke checks.

It records which public API, output schema, CLI JSON fields, error codes, event names, and package boundaries should be protected now, documented but not fully frozen yet, kept internal, or left for human decision.

This is a draft policy only. It is not a v1.0 stability guarantee, not an SDK-complete claim, not a package-release-ready claim, and not a production-ready claim.

## 2. Current Public API Candidates

Current public API candidates:

- current package/module path: `elysia_core`
- main entry point: `elysia_core.input.preprocess.preprocess_input`
- return type: `ProcessingResult`
- contract classes: `ProcessingResult`, `StepEvent`, `ErrorItem`

`elysia_core` is the current package path and should not be renamed without explicit human approval.

## 3. Protected Now

The following items should not change casually.

Python API:

- `preprocess_input()` import path
- `preprocess_input(text: Any) -> ProcessingResult`
- `ProcessingResult` core fields:
  - `correlation_id`
  - `original_input`
  - `processed_text`
  - `is_valid`
  - `events`
  - `errors`
- `StepEvent` minimum fields:
  - `name`
  - `severity`
  - `changed`
- `ErrorItem` minimum fields:
  - `code`
  - `message`
  - `step`
  - `severity`

CLI JSON:

- top-level fields:
  - `processed_text`
  - `is_valid`
  - `errors`
  - `events`
  - `correlation_id`
- `errors` as a reduced list of error code strings
- `events` as reduced objects with:
  - `name`
  - `changed`
  - `severity`

Behavior:

- whitespace-only input returns fallback output and `EMPTY_INPUT`
- non-string input returns fallback output and `UNEXPECTED_TYPE`
- valid representative punctuation case `What!!\u003F\u003F` remains covered by tests and CI
- `correlation_id` remains present and should remain traceable
- Streamlit remains demo-only and not a core dependency

## 4. Documented But Not Fully Frozen Yet

The following areas are compatibility-sensitive and should be documented carefully, but should not be treated as fully frozen without further human approval:

- exact event ordering
- full event catalog
- `StepEvent.before`
- `StepEvent.after`
- `StepEvent.note`
- exact human-readable error messages
- exact punctuation normalization beyond representative cases
- exact internal pipeline step implementation
- fallback text permanence, if not yet human-approved as long-term stable
- severity assignment details, except allowed severity values

## 5. Internal Implementation Details

The following should remain internal implementation details unless separately approved:

- pipeline runner internals
- individual step helper implementations
- module layout under `src/elysia_core/input/steps/`
- Streamlit UI layout, labels, cards, tabs, or summaries
- demo-specific presentation fields
- test file layout
- CI job implementation details, except that CI validates core/package smoke behavior

Internal refactors should remain allowed when protected public behavior and schema stay stable.

## 6. Compatibility-Sensitive Error Codes And Events

Current known error codes:

- `EMPTY_INPUT`
- `UNEXPECTED_TYPE`

Current known event names:

- `type_guard`
- `strip_spaces`
- `trim_edges`
- `collapse_spaces`
- `fallback_if_empty`
- `symbol_cleaner`

Current severity values:

- `info`
- `warn`
- `error`

Error codes are more compatibility-sensitive than human-readable error messages.

## 7. Human Decisions Required

The following require human decision before becoming official policy:

- whether `elysia_core` becomes the permanent package path
- versioning policy
- Python version support
- license
- maintainer identity
- package metadata wording
- console script policy
- how strongly to freeze event names
- how strongly to freeze fallback text
- when this draft becomes an official compatibility policy

## 8. Change Policy Guidance

- Protected-now fields should only change with a deliberate compatibility decision.
- Breaking changes should be documented.
- CLI JSON should not be confused with the full dataclass schema.
- Internal refactors are allowed if public behavior and schema remain stable.
- Streamlit UI should not define core API.
- Package rename work should not start unless explicitly approved as a separate migration.

## 9. Recommended Next Step

Recommended next step: review this draft manually and decide whether to convert it into an official compatibility policy.

A small compatibility contract test may be added later only after human approval. Do not implement tests as part of this draft.
