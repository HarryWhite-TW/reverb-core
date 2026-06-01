# Reverb v0.8 Package Configuration Migration Plan

## 1. Purpose

This document records the safest future path for package configuration migration in Reverb v0.8 planning.

It is a planning document only. It does not implement package configuration changes, does not create `pyproject.toml`, and does not claim that Reverb is package-ready.

## 2. Current Packaging State

Current `setup.py` is minimal:

- `name="elysia_core"`
- `version="0.1"`
- `packages=find_packages(where="src")`
- `package_dir={"": "src"}`

`pyproject.toml` does not currently exist.

`elysia_core` remains the current Python package and module path.

## 3. Current Gaps

Current package configuration gaps:

- missing `pyproject.toml`
- minimal package metadata
- missing Python version bounds
- missing build backend declaration
- missing dependency declaration strategy
- missing package data policy
- missing install verification
- missing CI workflow
- no console script entry point
- no formal public API docs or output schema docs

## 4. Migration Options

### Keep `setup.py` For Now And Document Gaps

This is the lowest-risk option. It preserves the current behavior and avoids premature packaging changes while v0.8 requirements are clarified.

The tradeoff is that package-readiness gaps remain open.

### Add Minimal `pyproject.toml` Later While Keeping `setup.py`

This is the recommended next configuration step after this plan is reviewed. It can introduce a modern build-system declaration while preserving the current `setup.py` package discovery behavior.

The tradeoff is that the repository temporarily keeps both configuration files.

### Fully Migrate To `pyproject.toml` Later

This is a cleaner long-term option, but it should wait until metadata, versioning, package data, install verification, and CLI entry point expectations are settled.

The tradeoff is higher migration risk if done before those decisions are made.

## 5. Recommended Path

Use a staged migration path:

1. First document metadata and install verification expectations.
2. Then add a minimal `pyproject.toml` later while keeping `setup.py`.
3. Then add install and build verification.
4. Then consider a console script entry point, package data policy, versioning policy, and fuller `pyproject.toml` migration.

This path keeps v0.8 focused on package-readiness planning before package-release claims.

## 6. Metadata Questions To Decide Later

Questions to decide before package configuration changes:

- project display name
- package/module name
- version policy
- author/maintainer fields
- license
- description
- README long description
- Python version support
- classifiers
- project URLs
- keywords

## 7. Package Data Questions

`src/elysia_core/config/default.json` may require package-data handling if installed builds must support `load_default_config()`.

Do not implement package-data configuration as part of this planning document.

## 8. Install Verification Plan

Future install verification commands to consider:

```bash
python -m pip install .
python -c "from elysia_core.input.preprocess import preprocess_input; print(preprocess_input('What!!??').processed_text)"
python -m elysia_core.cli --json "What!!??"
```

Wheel build and wheel install checks should be considered later.

## 9. CLI Packaging Direction

The CLI remains a demo and validation adapter for now.

A formal console script entry point can be considered later during package-readiness work.

Do not make the CLI the main SDK interface.

## 10. Non-goals

- no package rename
- no production-ready claim
- no SDK-complete claim
- no `pyproject.toml` implementation in this task
- no `setup.py` modification in this task
- no CI implementation
- no source/test changes
- no Local AI Workbench integration
- no OpenClaw integration

## 11. Suggested Next Step

After this plan is reviewed, a future separately approved implementation task may add a minimal `pyproject.toml` while keeping `setup.py`.

That future task should be explicitly scoped and approved before any package configuration files are changed.
