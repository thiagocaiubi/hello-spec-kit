# hello-spec-kit Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-16

## Active Technologies

- Python 3.13 (Dockerfile) / ≥3.10 (pyproject.toml)
- FastAPI 0.115.11
- Uvicorn ≥ 0.34.0
- pytest (testing)
- ruff (linting)

## Project Structure

```text
/
├── main.py              # FastAPI application entry point
├── tests/
│   └── unit/           # Unit tests
├── pyproject.toml      # Project dependencies
├── Dockerfile          # Container configuration
└── docker-compose.yaml # Orchestration
```

## Commands

```bash
# Run tests
python -m pytest tests/unit/ -v

# Run linter
ruff check .

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run with Docker
docker-compose up --build
```

## Code Style

- **Python**: PEP 8 compliant, enforced by ruff
- **Type Hints**: Required for all function signatures
- **Docstrings**: Required for all public functions (Google style)
- **Testing**: Unit tests required per constitution
- **Imports**: Standard library → Third-party → Local

## Constitution Principles

1. **Clean Code & Simplicity**: Single responsibility, DRY, YAGNI
2. **Minimal Dependencies**: Core dependencies only, no unnecessary packages
3. **Unit Tests Only**: FastAPI TestClient, no external test frameworks
4. **Type Safety**: Complete type hints throughout

## Recent Changes

- 001-health-endpoint: Added `/health` endpoint for Kubernetes probes
  - Returns `{"status": "ok"}` with HTTP 200
  - Performance: <100ms response time
  - 5 comprehensive unit tests

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
