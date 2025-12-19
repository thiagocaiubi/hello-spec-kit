# Pydantic Validation Feature - Quick Start Guide

## Overview

This guide helps developers quickly test and verify the Pydantic validation feature for the health endpoint.

## Prerequisites

- Python ≥3.10 installed
- Make utility available
- Docker and docker-compose (optional, for containerized testing)

## Setup

### 1. Clone and Install

```bash
# Navigate to project root
cd /path/to/hello-spec-kit

# Install dependencies with development tools
make install

# Verify installation
make test
```

### 2. Start Development Server

```bash
# Option A: Local Python server
make dev

# Option B: Docker container
make docker-up
```

The API will be available at `http://localhost:8000`

## Testing Pydantic Validation

### A. Interactive API Documentation

FastAPI automatically generates interactive docs:

1. **OpenAPI UI (Swagger)**: http://localhost:8000/docs
   - Click "GET /health" endpoint
   - Click "Try it out"
   - Execute to see Pydantic-validated response

2. **ReDoc**: http://localhost:8000/redoc
   - View `HealthResponse` schema definition
   - See validation error examples

### B. Command-Line Testing

#### Valid Request (200 OK)

```bash
curl -i http://localhost:8000/health
```

Expected response:
```http
HTTP/1.1 200 OK
content-type: application/json

{"status":"ok"}
```

#### Invalid Method (405 Method Not Allowed)

```bash
curl -i -X POST http://localhost:8000/health
```

Expected response:
```http
HTTP/1.1 405 Method Not Allowed
content-type: application/json

{"detail":"Method Not Allowed"}
```

#### Extra Fields Validation (422 if strict mode enabled)

```bash
curl -i "http://localhost:8000/health?unknown_param=value"
```

Expected behavior:
- **With strict mode**: HTTP 422 with Pydantic error
- **Without strict mode**: HTTP 200 (extra params ignored)

### C. Python Testing

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test valid request
response = client.get("/health")
assert response.status_code == 200
assert response.json() == {"status": "ok"}

# Test response model validation
data = response.json()
assert isinstance(data["status"], str)
assert data["status"] == "ok"

# Test strict validation (if enabled)
response = client.get("/health?unknown=value")
if response.status_code == 422:
    error = response.json()["detail"][0]
    assert error["type"] == "extra_forbidden"
```

## Running Unit Tests

```bash
# Run all tests
make test

# Run tests with coverage
make coverage

# Run specific test file
pytest tests/unit/test_health.py -v

# Run specific test function
pytest tests/unit/test_health.py::test_health_endpoint_returns_200 -v
```

Expected output:
```
tests/unit/test_health.py::test_health_endpoint_returns_200 PASSED
tests/unit/test_health.py::test_health_endpoint_returns_json PASSED
tests/unit/test_health.py::test_health_endpoint_correct_content_type PASSED
tests/unit/test_health.py::test_health_endpoint_ignores_query_params PASSED
tests/unit/test_health.py::test_health_endpoint_rejects_post PASSED
```

## Verifying Pydantic Integration

### 1. Check Response Model

The health endpoint should use `response_model`:

```python
from models.schemas import HealthResponse

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "ok"}
```

### 2. Verify Strict Validation

Check `models/schemas.py` for `ConfigDict`:

```python
from pydantic import BaseModel, ConfigDict

class HealthResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')
    status: str = "ok"
```

### 3. Test Type Coercion

Pydantic should automatically coerce compatible types:

```python
# Integer to string coercion
response = HealthResponse(status=123)  # Coerced to "123"

# Invalid type (should fail)
try:
    response = HealthResponse(status={"invalid": "object"})
except ValidationError as e:
    print(e.errors())  # Shows Pydantic error details
```

## Validation Error Inspection

When validation fails, inspect the error structure:

```bash
curl -i -X POST http://localhost:8000/health \
  -H "Content-Type: application/json" \
  -d '{"status": 123}'
```

Response structure:
```json
{
  "detail": [
    {
      "type": "string_type",
      "loc": ["body", "status"],
      "msg": "Input should be a valid string",
      "input": 123,
      "url": "https://errors.pydantic.dev/2/v/string_type"
    }
  ]
}
```

Visit the `url` field for detailed Pydantic error documentation.

## Performance Validation

Verify response times meet requirements:

```bash
# Single request timing
time curl -s http://localhost:8000/health

# Load testing (requires ab/apache-bench)
ab -n 1000 -c 10 http://localhost:8000/health

# Expected: <100ms per request (typically <10ms)
```

## Code Quality Checks

```bash
# Type checking with mypy
make type-check

# Linting with ruff
make lint

# Format code
make format

# Run all checks
make lint test type-check
```

## Docker Testing

```bash
# Build image
make docker-build

# Start container
make docker-up

# View logs
make docker-logs

# Test health endpoint
curl http://localhost:8000/health

# Stop container
make docker-down
```

## Troubleshooting

### Pydantic Not Found

```bash
# Verify FastAPI includes Pydantic
python -c "from pydantic import BaseModel; print('OK')"

# Reinstall if needed
make install
```

### Validation Not Working

1. Check `response_model` is set on endpoint
2. Verify `HealthResponse` model exists in `models/schemas.py`
3. Confirm strict mode: `model_config = ConfigDict(extra='forbid')`
4. Review test failures for validation behavior

### Type Errors

```bash
# Run mypy to catch type issues
make type-check

# Check Pydantic V2 syntax (not V1)
# V1: class Config: extra = 'forbid'
# V2: model_config = ConfigDict(extra='forbid')
```

## Next Steps

1. Review implementation plan: `specs/002-pydantic-validation/plan.md`
2. Check data models: `specs/002-pydantic-validation/data-model.md`
3. Read API contracts: `specs/002-pydantic-validation/contracts/`
4. Review research findings: `specs/002-pydantic-validation/research.md`
5. Execute tasks: Run `/speckit.tasks` to generate task breakdown

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [Project Makefile](../../Makefile) - All available commands
- [Feature Specification](spec.md) - Detailed requirements

