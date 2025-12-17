"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from main import app
from storage import InMemoryStorage


@pytest.fixture
def client():
    """Create a test client for the FastAPI application.
    
    Yields:
        TestClient instance
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def storage():
    """Create a fresh storage instance for testing.
    
    Returns:
        InMemoryStorage instance
    """
    return InMemoryStorage(max_logs=50)


@pytest.fixture
def sample_sensor_data():
    """Provide sample sensor data for testing.
    
    Returns:
        Dictionary with valid sensor data
    """
    return {
        "status": "normal",
        "temperature": 25.5,
        "gas": 3800
    }


@pytest.fixture
def danger_sensor_data():
    """Provide danger condition sensor data for testing.
    
    Returns:
        Dictionary with danger sensor data
    """
    return {
        "status": "danger",
        "temperature": 45.0,
        "gas": 4500
    }
