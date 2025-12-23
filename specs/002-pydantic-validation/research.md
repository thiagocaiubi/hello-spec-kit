# Research: Pydantic Data Validation

**Feature**: 002-pydantic-validation  
**Date**: 2025-12-19  
**Phase**: 0 - Research & Design Decisions

## Overview

This document captures research findings and design decisions for integrating Pydantic data validation into the FastAPI application.

## Research Questions & Findings

### 1. Pydantic Version and FastAPI Compatibility

**Question**: What version of Pydantic comes with FastAPI 0.115.11 and what are its capabilities?

**Findings**:
- FastAPI 0.115.11 includes Pydantic V2 (2.x) as a dependency
- Pydantic V2 is a complete rewrite with significant performance improvements (5-50x faster than V1)
- Native support for strict mode validation (ConfigDict with `extra='forbid'`)
- Built-in JSON schema generation for OpenAPI documentation
- Improved type coercion with clear rules for basic types

**Decision**: Use Pydantic V2 features with strict validation mode
- **Rationale**: Already included with FastAPI, no version conflicts, performance optimized
- **Alternatives considered**: Pydantic V1 compatibility mode - rejected as V2 is current standard

### 2. Model Configuration for Strict Validation

**Question**: How to configure Pydantic models to reject extra fields as specified?

**Findings**:
- Pydantic V2 uses `model_config = ConfigDict(extra='forbid')` for strict validation
- Three modes available: 'allow', 'ignore', 'forbid'
- 'forbid' mode raises ValidationError for any extra fields
- Error messages automatically include field names and validation rules

**Decision**: Use `ConfigDict(extra='forbid')` on all models
- **Rationale**: Matches specification requirement for strict validation
- **Alternatives considered**: Global config - rejected to maintain explicit per-model control

### 3. Response Model Integration with FastAPI

**Question**: How to integrate Pydantic models with FastAPI endpoints for automatic validation?

**Findings**:
- FastAPI automatically validates request bodies against Pydantic models (function parameters)
- Response models set via decorator: `@app.get("/path", response_model=ModelClass)`
- FastAPI auto-generates OpenAPI schema from Pydantic models
- Validation errors automatically return HTTP 422 with detailed error structure

**Decision**: Use response_model parameter for all endpoints
- **Rationale**: Clean separation of routing and validation, automatic OpenAPI docs
- **Alternatives considered**: Manual dict returns - rejected as loses type safety and docs

### 4. Health Endpoint Migration Strategy

**Question**: How to migrate existing health endpoint to use Pydantic without breaking changes?

**Findings**:
- Current health endpoint returns `{"status": "ok"}` as plain dict
- Pydantic model with same structure is transparent to API consumers
- No breaking changes - response format identical
- Added benefit: schema validation and OpenAPI documentation

**Decision**: Create HealthResponse model, update endpoint with response_model
- **Rationale**: Zero breaking changes, immediate documentation benefits
- **Alternatives considered**: Leave as dict - rejected as misses validation and docs opportunities

### 5. Error Response Format

**Question**: What error format does Pydantic/FastAPI use for validation errors?

**Findings**:
- FastAPI returns HTTP 422 Unprocessable Entity for validation errors
- Error body structure:
  ```json
  {
    "detail": [
      {
        "type": "string_type",
        "loc": ["body", "field_name"],
        "msg": "Input should be a valid string",
        "input": 123
      }
    ]
  }
  ```
- Multiple errors returned simultaneously for multiple invalid fields
- Nested field paths shown with dot notation in `loc` array

**Decision**: Use FastAPI/Pydantic default error format
- **Rationale**: Industry standard, clear field paths, detailed error information
- **Alternatives considered**: Custom error handler - rejected as unnecessary complexity

### 6. Type Coercion Rules

**Question**: What types does Pydantic automatically coerce and when does it fail?

**Findings**:
- String to int: "123" → 123 (succeeds), "abc" → ValidationError
- String to float: "123.45" → 123.45 (succeeds)
- String to bool: "true"/"false"/"1"/"0" → True/False (case-insensitive)
- Int to float: 123 → 123.0 (succeeds)
- Strict types (StrictInt, StrictStr) disable coercion
- List/Dict structures validated recursively

**Decision**: Use default Pydantic coercion (not strict types)
- **Rationale**: Matches specification for "basic type coercion", more flexible for API clients
- **Alternatives considered**: Strict types - rejected as too restrictive for REST API

### 7. Performance Impact

**Question**: What is the performance overhead of Pydantic validation?

**Findings**:
- Pydantic V2 validation typically adds <1ms for simple models (1-10 fields)
- Nested models: ~0.1ms per nesting level
- JSON serialization included in validation cost
- Caching of schema compilation makes subsequent validations faster
- For HealthResponse (1 field): expected overhead <0.5ms

**Decision**: No performance optimizations needed
- **Rationale**: Overhead well under 50ms requirement (spec SC-001)
- **Alternatives considered**: Lazy validation - rejected as premature optimization

### 8. Testing Strategy

**Question**: How to test Pydantic validation using FastAPI TestClient?

**Findings**:
- FastAPI TestClient simulates HTTP requests in-memory
- Can test both valid and invalid payloads
- Validation errors accessible via response.json()["detail"]
- No external dependencies needed
- Tests run in milliseconds

**Decision**: Use FastAPI TestClient for all validation tests
- **Rationale**: Meets constitution requirement (unit tests only, no external deps)
- **Alternatives considered**: Direct Pydantic model testing - rejected as doesn't test FastAPI integration

## Technology Decisions

### Implementation Approach

**Chosen**: Pydantic BaseModel with ConfigDict for all schemas

```python
from pydantic import BaseModel, ConfigDict

class HealthResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')
    status: str
```

**Justification**:
- Declarative and readable
- Type-safe with IDE support
- Automatic validation and serialization
- Zero boilerplate code

### Project Organization

**Chosen**: Separate `models/schemas.py` module

```text
models/
├── __init__.py
└── schemas.py      # All Pydantic models
```

**Justification**:
- Separates data models from routing logic
- Easy to import: `from models.schemas import HealthResponse`
- Scalable as more models are added
- Follows common FastAPI project structure

### Testing Approach

**Chosen**: TestClient with comprehensive validation scenarios

```python
from fastapi.testclient import TestClient

def test_health_endpoint_validation():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

**Justification**:
- Tests full request/response cycle
- Validates FastAPI+Pydantic integration
- Fast execution (in-memory)
- No external dependencies

## Dependencies

**New Dependencies**: None

**Existing Dependencies Used**:
- FastAPI 0.115.11 (includes Pydantic V2)
- Uvicorn ≥ 0.34.0 (ASGI server)

**No changes to pyproject.toml required**

## Performance Analysis

**Expected Performance**:
- Model definition: Compiled once at startup (~1ms one-time cost)
- Validation per request: <1ms for simple models
- Health endpoint: <0.5ms validation overhead
- **Total p95 latency impact**: <1ms (well under 50ms requirement)

**Throughput Impact**: Negligible - Pydantic V2 handles 100k+ validations/second

## Security Considerations

**Input Validation**: Pydantic prevents injection attacks by enforcing type constraints
- Strings remain strings, numbers remain numbers
- No code execution from input data
- Extra fields rejected (prevents parameter pollution)

**Error Information**: Validation errors reveal schema structure
- **Assessment**: Acceptable - API docs already expose schema
- **Mitigation**: Errors don't include internal implementation details

## Migration Path

**Current State**: Health endpoint returns plain dict `{"status": "ok"}`

**Implementation Path**:
1. Create `models/` directory structure
2. Define HealthResponse Pydantic model
3. Update health endpoint to use `response_model=HealthResponse`
4. Add validation tests
5. Verify OpenAPI docs reflect new schema

**Rollback**: Remove `response_model` parameter (instant rollback)

## Open Questions

None - all research complete, no ambiguities remaining.

## References

- Pydantic V2 Documentation: https://docs.pydantic.dev/2.0/
- FastAPI Response Models: https://fastapi.tiangolo.com/tutorial/response-model/
- Pydantic Performance: https://docs.pydantic.dev/latest/concepts/performance/
