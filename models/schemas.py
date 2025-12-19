"""Pydantic schemas for API request and response validation.

This module contains Pydantic BaseModel classes that define the structure
and validation rules for API data. All models use strict validation mode
(ConfigDict with extra='forbid') to ensure data integrity.

Validation Error Structure:
    When validation fails, Pydantic returns HTTP 422 with this structure:
    {
        "detail": [
            {
                "type": "string_type",              # Error type identifier
                "loc": ["body", "field_name"],      # Field location path
                "msg": "Input should be a valid string",  # Human-readable message
                "input": 123,                       # The invalid input value
                "url": "https://errors.pydantic.dev/..."  # Documentation link
            }
        ]
    }

Type Coercion Examples:
    - String to int: "123" → 123 ✓
    - String to float: "123.45" → 123.45 ✓
    - String to bool: "true"/"false" → True/False ✓
    - Int to string: 123 → Validation Error ✗ (strict mode)
"""

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Health check response model.
    
    Represents the response from the /health endpoint for Kubernetes probes.
    Uses strict validation mode to reject any extra fields not defined in the schema.
    
    Validation Behavior:
        - Extra fields are rejected (ConfigDict with extra='forbid')
        - Missing 'status' field triggers validation error
        - Type coercion: string values accepted (e.g., status="ok")
    
    Attributes:
        status: Health status indicator (always "ok" for healthy state)
    
    Example:
        >>> response = HealthResponse(status="ok")
        >>> response.status
        'ok'
        
        >>> # Extra fields are rejected in strict mode
        >>> HealthResponse(status="ok", extra="field")  # doctest: +SKIP
        ValidationError: extra_forbidden
    """
    
    model_config = ConfigDict(extra='forbid')
    
    status: str
