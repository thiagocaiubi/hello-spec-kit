# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A minimal FastAPI microservice template designed for Kubernetes deployment. Python 3.10+, managed with UV.

## Common Commands

```bash
make setup             # Full setup: install dev dependencies + verify + check
make test              # Run all unit tests (pytest -v)
make test-cov          # Tests with coverage report
make lint              # Ruff linter
make format            # Ruff auto-format
make typecheck         # MyPy strict type checking
make check             # All checks: test + lint + typecheck
make run               # Dev server with auto-reload (port 8000)
make run-prod          # Production server (4 workers)
make docker-up         # Start containers
make docker-down       # Stop containers
make ci                # CI pipeline: clean + install + test + lint
```

To run a single test file: `uv run pytest tests/unit/test_health.py -v`
To run a single test: `uv run pytest tests/unit/test_health.py::test_health_returns_ok -v`

## Architecture

Single FastAPI app (`main.py`) with two routes: `GET /` (welcome) and `GET /health` (Kubernetes probe). Pydantic models live in `models/schemas.py` with strict validation (`extra='forbid'`). Models are re-exported from `models/__init__.py`.

Tests are in `tests/unit/` using FastAPI's `TestClient` — no external services or integration tests. Tests must run fast (<5 seconds total).

Feature specifications live in `specs/` following a spec-driven development workflow. Each feature has its own directory with spec, plan, tasks, and contract documents.

## Code Conventions

- All functions require type hints (parameters and return types)
- Google-style docstrings
- Pydantic models use `ConfigDict(extra='forbid')` to reject unknown fields
- MyPy strict mode is enabled (see `pyproject.toml` for full config)
- Ruff handles both linting and formatting (PEP 8)
- Production dependencies only: FastAPI, Uvicorn, UV — keep minimal
