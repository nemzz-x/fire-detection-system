"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data
    assert "uptime_seconds" in data
    assert data["uptime_seconds"] >= 0


def test_dashboard_loads(client: TestClient):
    """Test that the dashboard page loads successfully."""
    response = client.get("/")
    
    assert response.status_code == 200
    assert "Fire Detection" in response.text
    assert "dashboard" in response.text.lower()


def test_post_status_valid_data(client: TestClient, sample_sensor_data: dict):
    """Test posting valid sensor data."""
    response = client.post("/status", json=sample_sensor_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["message"] == "Status updated successfully"
    assert "timestamp" in data
    assert data["data"]["status"] == sample_sensor_data["status"]
    assert data["data"]["temperature"] == sample_sensor_data["temperature"]
    assert data["data"]["gas"] == sample_sensor_data["gas"]


def test_post_status_danger_data(client: TestClient, danger_sensor_data: dict):
    """Test posting danger condition sensor data."""
    response = client.post("/status", json=danger_sensor_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["data"]["status"] == "danger"
    assert data["data"]["temperature"] == danger_sensor_data["temperature"]


def test_post_status_invalid_status(client: TestClient):
    """Test posting invalid status value."""
    invalid_data = {
        "status": "invalid_status",
        "temperature": 25.0,
        "gas": 3800
    }
    
    response = client.post("/status", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_post_status_negative_temperature(client: TestClient):
    """Test posting with negative temperature (should be allowed but validated)."""
    data = {
        "status": "normal",
        "temperature": -10.0,
        "gas": 3800
    }
    
    response = client.post("/status", json=data)
    # Should succeed as -10°C is within -50 to 150 range
    assert response.status_code == 200


def test_post_status_extreme_temperature(client: TestClient):
    """Test posting with extreme temperature."""
    data = {
        "status": "danger",
        "temperature": 200.0,  # Beyond validation range
        "gas": 3800
    }
    
    response = client.post("/status", json=data)
    assert response.status_code == 422  # Validation error


def test_post_status_negative_gas(client: TestClient):
    """Test posting with negative gas value."""
    data = {
        "status": "normal",
        "temperature": 25.0,
        "gas": -100
    }
    
    response = client.post("/status", json=data)
    assert response.status_code == 422  # Validation error


def test_get_stats(client: TestClient, sample_sensor_data: dict):
    """Test getting statistics."""
    # First post some data
    client.post("/status", json=sample_sensor_data)
    
    # Then get stats
    response = client.get("/api/stats")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "danger_count" in data
    assert "normal_count" in data
    assert "total_logs" in data
    assert "current_status" in data
    assert data["total_logs"] >= 1


def test_clear_logs(client: TestClient, sample_sensor_data: dict):
    """Test clearing all logs."""
    # Post some data
    client.post("/status", json=sample_sensor_data)
    
    # Clear logs
    response = client.delete("/api/logs")
    
    assert response.status_code == 200
    data = response.json()
    assert "cleared" in data["message"].lower()
    
    # Verify logs are cleared
    stats_response = client.get("/api/stats")
    stats = stats_response.json()
    assert stats["total_logs"] == 0


def test_multiple_status_updates(client: TestClient):
    """Test multiple status updates and verify counting."""
    # Post multiple normal readings
    for _ in range(3):
        client.post("/status", json={
            "status": "normal",
            "temperature": 22.0,
            "gas": 3500
        })
    
    # Post multiple danger readings
    for _ in range(2):
        client.post("/status", json={
            "status": "danger",
            "temperature": 50.0,
            "gas": 5000
        })
    
    # Check stats
    response = client.get("/api/stats")
    stats = response.json()
    
    assert stats["normal_count"] == 3
    assert stats["danger_count"] == 2
    assert stats["total_logs"] == 5


def test_api_documentation_available(client: TestClient):
    """Test that API documentation is accessible."""
    # Test Swagger UI
    response = client.get("/docs")
    assert response.status_code == 200
    
    # Test ReDoc
    response = client.get("/redoc")
    assert response.status_code == 200
