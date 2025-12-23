# Pydantic Validation Error Responses

This document describes the validation error format and behavior for the Pydantic-validated health endpoint.

## Overview

When Pydantic validation fails, FastAPI automatically returns an HTTP 422 Unprocessable Entity response with a standardized error structure defined by Pydantic V2.

## Error Response Structure

All validation errors follow this structure:

```json
{
  "detail": [
    {
      "type": "string",
      "loc": ["array", "of", "strings/integers"],
      "msg": "string",
      "input": "any",
      "url": "string (optional)"
    }
  ]
}
```

### Fields

- **type** (string, required): Pydantic error type identifier (e.g., `string_type`, `extra_forbidden`, `missing`)
- **loc** (array, required): Location path to the invalid field (e.g., `["body", "status"]`)
- **msg** (string, required): Human-readable error message
- **input** (any, required): The value that failed validation
- **url** (string, optional): Link to Pydantic error documentation at `https://errors.pydantic.dev/2/v/{error_type}`

## Health Endpoint Validation Scenarios

### Scenario 1: Extra Fields Not Allowed (Strict Mode)

**Configuration**: `ConfigDict(extra='forbid')`

**Request**:
```http
GET /health?unknown_param=value
```

**Response**: HTTP 422
```json
{
  "detail": [
    {
      "type": "extra_forbidden",
      "loc": ["query", "unknown_param"],
      "msg": "Extra inputs are not permitted",
      "input": "value",
      "url": "https://errors.pydantic.dev/2/v/extra_forbidden"
    }
  ]
}
```

### Scenario 2: Invalid Field Type (If request body accepted)

**Request**:
```http
POST /health
Content-Type: application/json

{
  "status": 123
}
```

**Response**: HTTP 422
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

### Scenario 3: Invalid Enum Value

**Request**:
```http
POST /health
Content-Type: application/json

{
  "status": "unhealthy"
}
```

**Response**: HTTP 422
```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["body", "status"],
      "msg": "Input should be 'ok'",
      "input": "unhealthy",
      "ctx": {
        "expected": "'ok'"
      },
      "url": "https://errors.pydantic.dev/2/v/enum"
    }
  ]
}
```

### Scenario 4: Missing Required Field

**Request**:
```http
POST /health
Content-Type: application/json

{}
```

**Response**: HTTP 422
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "status"],
      "msg": "Field required",
      "input": {},
      "url": "https://errors.pydantic.dev/2/v/missing"
    }
  ]
}
```

## Type Coercion Behavior

Per clarification #3, Pydantic's default type coercion is enabled.

### Examples of Automatic Coercion

**String to Integer**:
- Input: `"123"` → Coerced to: `123`

**Integer to String**:
- Input: `123` → Coerced to: `"123"`

**String to Boolean**:
- Input: `"true"`, `"1"`, `"yes"` → Coerced to: `True`
- Input: `"false"`, `"0"`, `"no"` → Coerced to: `False`

### Coercion Limits

Some coercions will fail and trigger validation errors:
- Invalid format strings (e.g., `"abc"` → int fails)
- Object/array to scalar types
- Incompatible complex types

## Error Handling Best Practices

### For Kubernetes Probes

Health endpoints should **not** return 422 errors during normal operation:
- Kubernetes expects 2xx for healthy, 4xx/5xx for unhealthy
- Validation errors indicate misconfiguration, not health status
- Configure probes to use simple GET requests without parameters

### For API Clients

When consuming endpoints with Pydantic validation:
1. Read OpenAPI schema at `/docs` or `/redoc`
2. Use generated TypeScript/Python clients for type safety
3. Handle 422 responses as client-side validation failures
4. Parse `detail` array to show user-friendly error messages
5. Check `url` field for detailed Pydantic documentation

## Testing Validation Errors

Unit tests should verify:
- ✅ Valid requests return 200
- ✅ Invalid types return 422 with correct error structure
- ✅ Extra fields return 422 when strict mode enabled
- ✅ Type coercion works for supported conversions
- ✅ Error messages are descriptive

Example test structure:
```python
def test_health_rejects_extra_fields():
    response = client.get("/health?unknown=value")
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "extra_forbidden"
    assert "unknown" in error["loc"]
```

## References

- [Pydantic V2 Errors Documentation](https://docs.pydantic.dev/latest/errors/errors/)
- [FastAPI Validation Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/#requestvalidationerror-vs-validationerror)
- [HTTP 422 Unprocessable Entity](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422)
- [OpenAPI 3.1.0 Specification](https://spec.openapis.org/oas/v3.1.0)

