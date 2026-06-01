# Reverb v0.8 Package Readiness Checklist

## 1. Purpose

This checklist prepares future v0.8 package-readiness planning for Reverb Core.

It records the packaging, SDK, CLI, Docker, and future guardrail gaps that should be reviewed before Reverb moves toward reusable package or SDK readiness. It does not implement packaging, does not create package configuration, and does not claim SDK completion.

## 2. Current v0.7 Foundation

Reverb v0.7 provides a stable foundation for future package-readiness work:

- Behavior is frozen with tests.
- Thin modularization is complete.
- Stable public entry point: `elysia_core.input.preprocess.preprocess_input`.
- Stable contracts: `ProcessingResult`, `StepEvent`, `ErrorItem`.
- CLI JSON demo is available.
- Docker demo is verified as reproducible demo support.
- README and roadmap are aligned with v0.7.

## 3. Package-Readiness Gaps

Current package-readiness gaps:

- `pyproject.toml` is missing.
- `setup.py` is minimal.
- Package metadata gaps remain.
- Python version bounds are not documented.
- Dependency declaration strategy is missing.
- Build backend is not defined.
- Package install verification is missing.
- Release/version policy is missing.
- CI workflow is missing.

## 4. SDK-Readiness Gaps

Current SDK-readiness gaps:

- Public API is not formally documented as an SDK API.
- No top-level convenience export exists yet.
- No compatibility policy exists for contracts.
- No error catalog exists.
- No output schema reference document exists.
- No embedding examples exist for backend or agent workflow usage.
- No task/request abstraction exists beyond raw text preprocessing.

## 5. CLI Role

The CLI is currently a demo and validation adapter.

It is useful for local checks, README examples, Docker demos, and JSON output verification. It is not the main SDK interface yet.

A formal console script entry point can be considered later during package-readiness work.

## 6. Docker Role

Docker is currently reproducible demo support.

It should not be positioned as production deployment packaging. Future Docker improvements may include CI build checks, image tagging policy, runtime expectations, and a hardening review.

## 7. Task Packet Guardrail Future Gaps

Future task packet guardrail planning areas include:

- `TaskPacket` schema
- allowed actions
- forbidden operations
- risk-level taxonomy
- approval requirement model
- `correlation_id` linkage
- audit trace format
- task validation result contract
- tests for valid, invalid, risky, and approval-required task packets

These are future planning areas. Personal Local AI Workbench may become a future consumer or control-plane use case, but it is not part of Reverb v0.7.

## 8. Recommended v0.8 Checklist

- [ ] Define package metadata requirements.
- [ ] Decide `setup.py` / `pyproject.toml` migration path.
- [ ] Document public API and contract stability expectations.
- [ ] Add output schema docs.
- [ ] Add library usage examples.
- [ ] Add install/build verification plan.
- [ ] Add CI plan.
- [ ] Decide console script entry point.
- [ ] Define versioning/release-note policy.
- [ ] Keep `elysia_core` unless separate rename migration is approved.

## 9. Deferred Items

The following items are deferred:

- package rename
- production-ready claim
- completed SDK claim
- OpenClaw integration
- completed Local AI Workbench integration
- task packet validation implementation
- service/deployment packaging
- broad plugin/framework abstraction

## 10. Suggested Next Step

Perform a future read-only review of `setup.py` / `pyproject.toml` migration options before implementation.

Do not begin source, config, package metadata, CI, or SDK implementation from this checklist alone.
