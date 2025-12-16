# Research: Kubernetes Health Probe Endpoint

**Feature**: 001-health-endpoint  
**Date**: 2025-12-16  
**Phase**: 0 - Research & Design Decisions

## Overview

This document captures research findings and design decisions for implementing a Kubernetes health probe endpoint in a FastAPI application.

## Research Questions & Findings

### 1. FastAPI Health Endpoint Best Practices

**Question**: What is the standard approach for implementing health endpoints in FastAPI?

**Findings**:
- FastAPI uses standard route decorators (`@app.get()`) for endpoint definition
- Health endpoints typically return simple JSON responses with status indicators
- No special FastAPI middleware or extensions needed for basic health checks
- FastAPI automatically sets `Content-Type: application/json` for dict responses

**Decision**: Use FastAPI's native route decorator with direct dictionary return
- **Rationale**: Simplest approach, no additional abstractions needed
- **Alternatives considered**: Pydantic response models rejected as over-engineering for fixed response

### 2. Response Format for Kubernetes Probes

**Question**: What response format do Kubernetes probes expect?

**Findings**:
- Kubernetes probes primarily check HTTP status code (200 = healthy)
- Response body is optional but useful for debugging
- Common patterns: `{"status": "ok"}`, `{"status": "healthy"}`, or `{"alive": true}`
- Content-Type should be `application/json` for structured responses

**Decision**: Return `{"status": "ok"}` as specified in requirements
- **Rationale**: Matches user specification exactly, simple and clear
- **Alternatives considered**: More verbose formats rejected per YAGNI principle

### 3. Endpoint Path Convention

**Question**: What is the conventional path for health endpoints?

**Findings**:
- Common conventions: `/health`, `/healthz`, `/health/live`, `/health/ready`
- `/health` is most widely used across ecosystems
- Kubernetes documentation examples typically use `/healthz`
- Some applications separate liveness (`/health/live`) and readiness (`/health/ready`)

**Decision**: Use `/health` path
- **Rationale**: Specified in requirements, most universal convention
- **Alternatives considered**: Separate endpoints for liveness/readiness rejected as premature complexity

### 4. Performance Considerations

**Question**: How to ensure the health endpoint meets performance requirements (<100ms p95)?

**Findings**:
- Simple FastAPI route handlers execute in microseconds (typically <1ms)
- No I/O operations needed for basic health checks
- FastAPI's async handlers are extremely efficient for lightweight operations
- Uvicorn's ASGI implementation adds minimal overhead

**Decision**: Implement as synchronous function returning dict
- **Rationale**: No async operations needed, simpler code, meets performance targets by orders of magnitude
- **Alternatives considered**: Async function unnecessary - adds complexity without benefit

### 5. Error Handling

**Question**: What error handling is needed for the health endpoint?

**Findings**:
- If the endpoint handler executes, the server is healthy by definition
- Catastrophic failures (server down) result in connection refused, not 500 errors
- FastAPI automatically handles uncaught exceptions with 500 status
- Health endpoints should not intentionally throw exceptions

**Decision**: No explicit error handling in health endpoint
- **Rationale**: If handler executes, server is healthy. If server is unhealthy, connection fails before handler runs
- **Alternatives considered**: Try-catch blocks rejected as unnecessary - no operations can fail

### 6. Testing Strategy

**Question**: How to test the health endpoint per constitution requirements?

**Findings**:
- FastAPI provides `TestClient` for testing without running actual server
- `TestClient` wraps application with requests-like interface
- Tests can verify status code, headers, and response body
- No external dependencies needed - fully in-memory testing

**Decision**: Use FastAPI TestClient with standard assertions
- **Rationale**: Meets constitution unit testing requirements, fast, no dependencies
- **Alternatives considered**: pytest fixtures rejected as unnecessary abstraction

### 7. HTTP Method Handling

**Question**: Should the endpoint explicitly reject non-GET methods?

**Findings**:
- FastAPI automatically returns 405 Method Not Allowed for non-matching methods
- No explicit handler needed for POST, PUT, DELETE, etc.
- Decorator `@app.get()` restricts endpoint to GET method only

**Decision**: Rely on FastAPI's automatic 405 responses
- **Rationale**: Built-in behavior, no code needed, meets edge case requirements
- **Alternatives considered**: Explicit method checking rejected as duplicate logic

## Technology Decisions

### Implementation Approach

**Chosen**: Direct route handler in main.py

```python
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

**Justification**:
- Simplest possible implementation
- No new dependencies
- Meets all functional and non-functional requirements
- Aligns with Clean Code principle (Single Responsibility)
- Aligns with YAGNI principle (no premature abstraction)

### Testing Approach

**Chosen**: FastAPI TestClient with direct assertions

```python
from fastapi.testclient import TestClient
from main import app

def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

**Justification**:
- Zero external dependencies
- Fast execution (< 1ms per test)
- Meets constitution unit testing requirements
- Verifies all acceptance criteria

## Dependencies

**New Dependencies**: None

**Existing Dependencies Used**:
- FastAPI 0.115.11 (already in pyproject.toml)
- Uvicorn ≥ 0.34.0 (already in pyproject.toml)

**Test Dependencies**: None (FastAPI TestClient included with FastAPI)

## Performance Analysis

**Expected Performance**:
- Handler execution: <1ms (no I/O, simple dict return)
- Serialization: <1ms (2-field JSON object)
- Network overhead: 1-5ms (TCP/HTTP protocol)
- **Total p95 latency**: <10ms (well under 100ms requirement)

**Throughput Capacity**:
- FastAPI + Uvicorn can handle 10,000+ req/s for simple endpoints
- Requirement: 100 req/s
- **Headroom**: 100x over requirement

## Security Considerations

**Authentication**: None required
- **Rationale**: Health endpoints must be accessible to Kubernetes control plane without authentication
- **Risk**: Information disclosure (server is running) - acceptable for operational necessity

**Rate Limiting**: Not implemented
- **Rationale**: Kubernetes probes are predictable, low-frequency traffic
- **Mitigation**: Application-level rate limiting can be added later if needed

## Migration Path

**Current State**: No health endpoint exists

**Implementation Path**:
1. Add route handler to main.py
2. Add unit test to tests/unit/test_health.py
3. Verify test passes
4. Manual verification via curl/browser
5. Deploy and configure Kubernetes probes

**Rollback**: Simple - remove 3 lines of code

## Open Questions

None - all research complete, no ambiguities remaining.

## References

- [FastAPI Documentation - First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Kubernetes - Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
