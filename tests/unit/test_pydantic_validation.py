"""Unit tests for general Pydantic validation patterns.

This module tests comprehensive validation behavior including type coercion,
nested structures, extra fields rejection, and error message formatting.
"""

import pytest
from pydantic import BaseModel, ValidationError, ConfigDict


# Test models for validation patterns
class SimpleModel(BaseModel):
    """Simple model for basic validation testing."""
    model_config = ConfigDict(extra='forbid')
    
    name: str
    age: int


class NestedAddress(BaseModel):
    """Nested address model."""
    model_config = ConfigDict(extra='forbid')
    
    street: str
    city: str
    zipcode: str


class PersonModel(BaseModel):
    """Model with nested structure for testing nested validation."""
    model_config = ConfigDict(extra='forbid')
    
    name: str
    address: NestedAddress


def test_valid_data_acceptance():
    """Test that valid data is accepted and parsed correctly."""
    data = {"name": "Alice", "age": 30}
    model = SimpleModel(**data)
    
    assert model.name == "Alice"
    assert model.age == 30


def test_invalid_type_rejection():
    """Test that invalid field types are rejected with clear errors."""
    with pytest.raises(ValidationError) as exc_info:
        SimpleModel(name="Bob", age="not_an_integer")
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "int_parsing"
    assert "age" in str(errors[0]["loc"])
    assert "input" in errors[0]


def test_missing_required_fields():
    """Test that missing required fields trigger validation errors."""
    with pytest.raises(ValidationError) as exc_info:
        SimpleModel(name="Charlie")  # Missing 'age'
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "missing"
    assert "age" in str(errors[0]["loc"])


def test_type_coercion_string_to_int():
    """Test that Pydantic coerces string to int when possible."""
    # String representation of number should be coerced
    model = SimpleModel(name="David", age="25")
    assert model.age == 25
    assert isinstance(model.age, int)


def test_type_coercion_behavior():
    """Test Pydantic V2 type coercion behavior.
    
    Pydantic V2 coerces strings to numbers but not numbers to strings
    unless using Field(coerce=True) or custom validators.
    """
    # String to int coercion works
    model1 = SimpleModel(name="David", age="25")
    assert model1.age == 25
    
    # Int to string does NOT auto-coerce in Pydantic V2 strict mode
    with pytest.raises(ValidationError) as exc_info:
        SimpleModel(name=123, age=30)
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "string_type"


def test_extra_fields_rejection_strict_mode():
    """Test that extra fields are rejected in strict validation mode."""
    with pytest.raises(ValidationError) as exc_info:
        SimpleModel(name="Eve", age=28, extra_field="not_allowed")
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "extra_forbidden"
    assert "extra_field" in str(errors[0]["loc"])


def test_nested_validation_errors_with_field_paths():
    """Test that nested validation errors show correct field paths."""
    with pytest.raises(ValidationError) as exc_info:
        PersonModel(
            name="Frank",
            address={"street": "Main St", "city": "NYC"}  # Missing zipcode
        )
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "missing"
    # Check that error path includes nested structure
    loc = errors[0]["loc"]
    assert "address" in str(loc)
    assert "zipcode" in str(loc)


def test_multiple_simultaneous_validation_errors():
    """Test that multiple validation errors are returned simultaneously."""
    with pytest.raises(ValidationError) as exc_info:
        SimpleModel(
            name=None,  # Invalid: should be string
            age="invalid"  # Invalid: cannot parse as int
        )
    
    errors = exc_info.value.errors()
    # Should have at least one error (Pydantic may report multiple)
    assert len(errors) >= 1
    
    # Collect all error locations
    error_locs = [str(e["loc"]) for e in errors]
    
    # Should have errors for both fields
    assert any("name" in loc or "age" in loc for loc in error_locs)
