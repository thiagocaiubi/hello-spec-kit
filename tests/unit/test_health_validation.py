"""Unit tests for Pydantic validation on the health endpoint.

This module tests the HealthResponse Pydantic model and its integration
with the /health endpoint, including strict validation mode.
"""

import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient

from main import app
from models.schemas import HealthResponse


client = TestClient(app)


def test_health_response_model_instantiation():
    """Test that HealthResponse model can be instantiated with valid data."""
    response = HealthResponse(status="ok")
    assert response.status == "ok"


def test_health_response_model_rejects_extra_fields():
    """Test that HealthResponse model rejects extra fields in strict mode."""
    with pytest.raises(ValidationError) as exc_info:
        HealthResponse(status="ok", extra_field="not_allowed")
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "extra_forbidden"
    assert "extra_field" in str(errors[0]["loc"])


def test_health_endpoint_response_validation():
    """Test that /health endpoint returns valid HealthResponse structure."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    
    # Verify response can be parsed by HealthResponse model
    health_response = HealthResponse(**data)
    assert health_response.status == "ok"
