# Reverb Product Direction Review

## Purpose

This document records Reverb's product direction after reaching demo-ready guardrail core status.

It is a product direction record, not an implementation prompt. It is intended to keep future milestones aligned with Reverb's current positioning, likely users, strategic roadmap, anti-goals, and human decisions that must be made before package or SDK claims are expanded.

## Current Positioning

Reverb is currently a deterministic input guardrail and contract-first preprocessing core.

It is best understood as an embeddable Python-oriented component that can sit before APIs, AI workflows, NLP systems, backend services, or agent workflows. Its current value is deterministic preprocessing, structured results, explicit errors, step-level observability, and traceable `correlation_id` output.

Current implemented surfaces include:

- Python library usage through `elysia_core.input.preprocess.preprocess_input`
- structured in-memory contracts: `ProcessingResult`, `StepEvent`, and `ErrorItem`
- CLI demo and JSON verification route
- basic Python usage example
- public API and output schema documentation
- Streamlit Input Inspector demo for public-facing explanation

Reverb is CLI-demoable and UI-demoable, but the CLI and Streamlit UI are demo and validation surfaces. They are not the core product.

Reverb is not currently:

- production-ready
- SDK-complete
- package-release ready
- Local AI Workbench integration
- Task Packet Guardrail implementation

## Likely Users

Likely users and viewers include:

- AI application developers who need deterministic preprocessing before model or workflow calls
- workflow and agent tool builders who need structured preflight checks
- QA and engineering reviewers who need contract, error, event, and traceability evidence
- non-technical demo viewers who need to understand guardrail behavior without reading raw JSON
- future Local AI Workbench as a possible consumer or control plane, after package and API maturity

## Ideal Product Direction

The ideal direction is to make Reverb an embeddable Python guardrail package with a stable public contract first, then expand toward profiles, task packet validation, and future consumer integrations.

Ranked direction:

1. Package and API maturity
2. Versioned output schema and compatibility policy
3. Embedding examples for AI workflows
4. Named guardrail profiles
5. Task Packet Guardrail
6. Local AI Workbench consumer or control plane

### 1. Package and API Maturity

This is the highest-value next direction because Reverb already has a stable public entry point, structured contracts, examples, CLI verification, and public documentation.

This serves AI application developers and engineering reviewers who need to install, import, and trust Reverb outside the source tree.

Risks and scope traps:

- claiming package-release readiness before install verification is complete
- claiming SDK completion before compatibility policy exists
- inventing package metadata, license, maintainer, or Python version support without human approval
- allowing package rename work to distract from core reliability

Do not overclaim production readiness, SDK completeness, or package-release readiness.

### 2. Versioned Output Schema and Compatibility Policy

This direction fits Reverb because its core value is structured, observable output.

This serves backend teams, QA reviewers, and integrators who need predictable fields, error codes, events, and trace identifiers.

Risks and scope traps:

- freezing behavior that is not protected by tests
- documenting compatibility promises too broadly
- letting CLI JSON and in-memory Python contracts drift without clear explanation

Do not claim a stable long-term schema until tests and compatibility policy support it.

### 3. Embedding Examples for AI Workflows

This direction fits Reverb's README positioning as a component that sits before APIs, NLP systems, AI workflows, or backend services.

This serves AI application developers and workflow builders who need practical examples of how to use `processed_text`, `is_valid`, `errors`, `events`, and `correlation_id`.

Risks and scope traps:

- building framework integrations too early
- turning examples into broad SDK abstractions
- implying production deployment readiness

Do not turn embedding examples into full platform integrations.

### 4. Named Guardrail Profiles

Named profiles may become useful once the public API and schema are stable. Profiles could describe different guardrail policies without making individual pipeline steps look freely toggleable.

This serves teams that need consistent policy names for different workflow contexts.

Risks and scope traps:

- undermining deterministic pipeline behavior
- making the UI look like a pipeline switchboard
- creating profile semantics before core contracts are stable

Do not make pipeline steps freely toggleable.

### 5. Task Packet Guardrail

Task Packet Guardrail is a natural future direction because Reverb already emphasizes structured validation, traceability, explicit errors, and deterministic behavior.

This serves agent and workflow systems that need task schema validation, allowed actions, forbidden operations, risk levels, approval requirements, correlation linkage, and audit traceability.

Risks and scope traps:

- implementing task packet validation before text guardrail contracts are stable
- overbuilding agent infrastructure
- claiming Task Packet Guardrail implementation before it exists

Do not begin this before package/API/schema maturity is established.

### 6. Local AI Workbench Consumer or Control Plane

Local AI Workbench may become a future consumer or control plane for Reverb.

This direction should come after Reverb is mature as an installable, documented, embeddable guardrail core.

Risks and scope traps:

- turning Reverb into an application too early
- tying Reverb's core direction to one consumer
- claiming Local AI Workbench integration before implementation exists

Do not jump into full Local AI Workbench before package and API maturity.

## Recommended Next Three Milestones

## M1: Package and Install Readiness

Goal:

Make Reverb reliably installable and usable outside the source checkout.

Expected outcome:

- clean environment install is verified
- public API import works after install
- contract imports work after install
- CLI module execution works after install
- package data behavior is verified or explicitly scoped
- no package rename is introduced

Possible affected areas:

- package configuration
- install verification documentation or scripts
- package metadata planning
- package-data handling for config files if required

Non-goals:

- production-ready claim
- SDK-complete claim
- package rename
- Local AI Workbench integration
- Task Packet Guardrail implementation
- broad framework adapters

Validation evidence:

- isolated install verification succeeds
- `preprocess_input("What!!??")` works after install
- CLI valid and fallback JSON cases work after install
- contract imports succeed after install
- package data behavior is verified if supported

## M2: Public API and Schema Stabilization

Goal:

Define what Reverb promises to embedders and reviewers.

Expected outcome:

- public API expectations are documented
- in-memory contract expectations are documented
- CLI JSON shape is documented separately from in-memory objects
- error codes and event names are documented with current boundaries
- compatibility policy is explicit and test-backed

Possible affected areas:

- API reference
- output schema documentation
- contract tests
- CLI JSON tests
- examples and demo documentation

Non-goals:

- broad new feature surface
- configurable pipeline profiles
- Task Packet Guardrail implementation
- package rename
- production readiness claim

Validation evidence:

- tests protect documented contract shape
- representative examples match documented behavior
- docs clearly distinguish in-memory Python objects from CLI JSON
- compatibility expectations avoid unsupported promises

## M3: Embedding Story Before Expansion

Goal:

Show how Reverb fits into AI and backend workflows without becoming an app or platform.

Expected outcome:

- clear examples for backend or AI workflow preflight usage
- examples show how to handle valid, fallback, and type guard cases
- examples show how to pass along or log `correlation_id`
- examples show how to interpret errors and events without overclaiming production readiness

Possible affected areas:

- examples
- demo guide
- API documentation
- output schema documentation

Non-goals:

- full framework plugins
- chatbot behavior
- production deployment guidance
- Local AI Workbench implementation
- Task Packet Guardrail implementation

Validation evidence:

- embedding examples run successfully
- examples preserve current core behavior
- docs keep CLI and Streamlit as demo surfaces
- no production, SDK-complete, or platform-integration claims are introduced

## Anti-Goals / Scope Traps

Avoid or delay:

- overbuilding the Streamlit UI
- turning Reverb into a chatbot
- making pipeline steps freely toggleable
- claiming production readiness too early
- jumping into full Local AI Workbench too early
- implementing Task Packet Guardrail before text guardrail contracts are stable
- inventing license, maintainer, version support, or package metadata without human approval
- letting outdated planning docs contradict current packaging reality

## Human Decisions Required

The following require human approval before implementation or public claims:

- license
- public maintainer identity
- version policy
- Python version support
- package metadata wording
- whether `elysia_core` remains indefinitely
- whether CLI becomes a formal console script
- when Task Packet Guardrail becomes an approved implementation milestone
