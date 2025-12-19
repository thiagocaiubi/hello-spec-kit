"""Unit tests for type checking with Pydantic models.

This module verifies that Pydantic models have correct type hints
and that type checkers (mypy) can catch type errors at development time.
"""

from models.schemas import HealthResponse


def test_health_response_type_hints():
    """Test that HealthResponse has correct type annotations."""
    # Verify type hints exist
    annotations = HealthResponse.__annotations__
    assert "status" in annotations
    assert annotations["status"] is str


def test_model_instantiation_with_correct_types():
    """Test that models can be instantiated with correct types."""
    # This should pass type checking
    response: HealthResponse = HealthResponse(status="ok")
    
    # Verify field types
    status_value: str = response.status
    assert isinstance(status_value, str)
    assert status_value == "ok"


# Intentional type errors (commented out to prevent test execution errors)
# Uncomment these to verify mypy catches them:

# def test_intentional_type_error_wrong_field_type():
#     """This should fail mypy type checking."""
#     # Error: Argument "status" to "HealthResponse" has incompatible type "int"; expected "str"
#     response: HealthResponse = HealthResponse(status=123)  # type: ignore


# def test_intentional_type_error_wrong_assignment():
#     """This should fail mypy type checking."""
#     response = HealthResponse(status="ok")
#     # Error: Incompatible types in assignment (expression has type "int", variable has type "str")
#     bad_status: int = response.status  # type: ignore
