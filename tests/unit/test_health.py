"""Unit tests for health endpoint.

Tests verify that the /health endpoint meets all functional requirements
for Kubernetes readiness and liveness probes.
"""
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_health_endpoint_returns_200():
    """Test that health endpoint returns HTTP 200 status code.
    
    Requirement: FR-001 - Health endpoint must return HTTP 200
    """
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_returns_correct_json():
    """Test that health endpoint returns correct JSON payload.
    
    Requirement: FR-002 - Response body must be {"status": "ok"}
    """
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_endpoint_has_json_content_type():
    """Test that health endpoint returns JSON content type.
    
    Requirement: FR-003 - Content-Type must be application/json
    """
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"


def test_health_endpoint_ignores_query_params():
    """Test that health endpoint ignores query parameters.
    
    Requirement: Edge case - Query parameters should not affect response
    """
    response = client.get("/health?foo=bar&baz=qux")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint_rejects_post_method():
    """Test that health endpoint rejects POST requests.
    
    Requirement: Edge case - Only GET method should be allowed
    """
    response = client.post("/health")
    assert response.status_code == 405
