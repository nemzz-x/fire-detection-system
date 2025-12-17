"""Tests for data models."""

import pytest
from pydantic import ValidationError
from models import SensorData, StatusResponse, HealthResponse


def test_sensor_data_valid():
    """Test creating valid sensor data."""
    data = SensorData(
        status="normal",
        temperature=25.5,
        gas=3800
    )
    
    assert data.status == "normal"
    assert data.temperature == 25.5
    assert data.gas == 3800


def test_sensor_data_danger():
    """Test creating danger sensor data."""
    data = SensorData(
        status="danger",
        temperature=50.0,
        gas=5000
    )
    
    assert data.status == "danger"
    assert data.temperature == 50.0
    assert data.gas == 5000


def test_sensor_data_invalid_status():
    """Test that invalid status raises validation error."""
    with pytest.raises(ValidationError):
        SensorData(
            status="invalid",
            temperature=25.0,
            gas=3800
        )


def test_sensor_data_temperature_rounding():
    """Test that temperature is rounded to 2 decimal places."""
    data = SensorData(
        status="normal",
        temperature=25.555555,
        gas=3800
    )
    
    assert data.temperature == 25.56


def test_sensor_data_extreme_temperature():
    """Test that extreme temperatures are rejected."""
    with pytest.raises(ValidationError):
        SensorData(
            status="danger",
            temperature=200.0,  # Beyond -50 to 150 range
            gas=3800
        )


def test_sensor_data_negative_gas():
    """Test that negative gas values are rejected."""
    with pytest.raises(ValidationError):
        SensorData(
            status="normal",
            temperature=25.0,
            gas=-100
        )


def test_sensor_data_with_timestamp():
    """Test sensor data with explicit timestamp."""
    timestamp = "2025-12-17 16:00:00"
    data = SensorData(
        status="normal",
        temperature=25.0,
        gas=3800,
        timestamp=timestamp
    )
    
    assert data.timestamp == timestamp


def test_sensor_data_without_timestamp():
    """Test sensor data without timestamp (should be None)."""
    data = SensorData(
        status="normal",
        temperature=25.0,
        gas=3800
    )
    
    assert data.timestamp is None


def test_status_response():
    """Test status response model."""
    sensor_data = SensorData(
        status="normal",
        temperature=25.0,
        gas=3800
    )
    
    response = StatusResponse(
        message="Test message",
        timestamp="2025-12-17 16:00:00",
        data=sensor_data
    )
    
    assert response.message == "Test message"
    assert response.data.status == "normal"


def test_health_response():
    """Test health response model."""
    response = HealthResponse(
        status="healthy",
        timestamp="2025-12-17 16:00:00",
        version="1.0.0",
        uptime_seconds=123.45
    )
    
    assert response.status == "healthy"
    assert response.version == "1.0.0"
    assert response.uptime_seconds == 123.45


def test_sensor_data_boundary_values():
    """Test sensor data with boundary values."""
    # Minimum values
    data_min = SensorData(
        status="normal",
        temperature=0,
        gas=0
    )
    assert data_min.temperature == 0
    assert data_min.gas == 0
    
    # Maximum values
    data_max = SensorData(
        status="danger",
        temperature=100,
        gas=10000
    )
    assert data_max.temperature == 100
    assert data_max.gas == 10000
