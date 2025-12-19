"""Pydantic models for request/response validation.

This module exports Pydantic BaseModel schemas used for API validation.
All models use strict validation mode (ConfigDict with extra='forbid') to reject
requests containing extra fields not defined in the schema.

Strict Validation Mode:
    All models in this package are configured with ConfigDict(extra='forbid').
    This means:
    - Extra fields in requests will trigger HTTP 422 ValidationError
    - Only fields defined in the model schema are accepted
    - Type coercion follows Pydantic V2 rules (string→number ✓, number→string ✗)

Example:
    from models import HealthResponse
    
    # Valid usage
    response = HealthResponse(status="ok")
    
    # Invalid: extra field
    response = HealthResponse(status="ok", extra="field")  # ValidationError
"""

from models.schemas import HealthResponse

__all__ = ["HealthResponse"]
