# Reverb v0.8 Package Metadata Decisions

## 1. Purpose

This document records package metadata decisions before future package configuration implementation.

It is a planning record only. It does not implement package metadata, does not create `pyproject.toml`, and does not claim package readiness.

## 2. Current Context

Reverb v0.7 is closed as a modular, test-protected deterministic preprocessing core.

Reverb v0.8 is package-readiness planning.

The current module path remains `elysia_core`.

The current `setup.py` is minimal and still exists.

`pyproject.toml` does not exist yet.

## 3. Decision Table

| Field | Current Decision | Status | Notes |
| --- | --- | --- | --- |
| Project display name | Reverb Core | accepted | public project name used in README/docs |
| Python package/module path | elysia_core | accepted for v0.8 planning | no package rename in this milestone |
| Package rename to reverb_core | deferred | deferred | must be a separate approved migration if ever needed |
| Version | keep current setup.py version unchanged for now | undecided | decide version policy before changing package metadata |
| License | undecided | undecided | do not invent a license |
| Author / maintainer | undecided | undecided | decide what public identity/email should appear before implementation |
| Python version support | audit before declaring | undecided | avoid unsupported version claims |
| Dependencies | no external runtime dependencies confirmed yet | needs verification | verify before package config changes |
| Console script entry point | deferred | deferred | CLI remains demo/validation adapter for now |
| README long description | likely use README.md later | planned | verify packaging format before implementation |
| Package data | needs review for config/default.json | needs verification | ensure installed package can load default config if required |
| Classifiers / keywords / URLs | undecided | undecided | fill only after project metadata wording is finalized |

## 4. Accepted Decisions For v0.8 Planning

- Keep `elysia_core` as module path.
- Do not rename package in v0.8-B.
- Keep CLI as demo/validation adapter for now.
- Treat `pyproject.toml` as future implementation, not this task.
- Keep Reverb positioned as a deterministic input guardrail / preprocessing core moving toward future embeddable guardrail SDK direction.

## 5. Deferred Decisions

- package rename
- console script entry point
- full pyproject migration
- production-ready claim
- SDK-complete claim
- Task Packet Guardrail implementation
- Local AI Workbench integration
- OpenClaw integration

## 6. Undecided Fields Requiring Human Approval

- license
- public author/maintainer information
- version policy
- Python version support
- final package metadata wording
- classifiers
- project URLs
- package data policy

## 7. Risks If Implemented Too Early

- inaccurate version or license metadata
- accidental package rename
- broken install due package data omission
- CLI entry point becoming main SDK interface too early
- claiming SDK/package readiness before install verification exists

## 8. Recommended Next Step

Recommended next step: create a future read-only install verification plan before package configuration implementation, or implement a narrowly scoped minimal `pyproject.toml` only after human approval.

Any implementation must be separately approved.

## 9. Non-goals

- no source changes
- no test changes
- no `setup.py` modification
- no `pyproject.toml` creation
- no CI implementation
- no package rename
- no production-ready claim
- no completed SDK claim
