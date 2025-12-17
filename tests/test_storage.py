"""Tests for storage layer."""

import pytest
from storage import InMemoryStorage
from models import SensorData


def test_storage_initialization(storage: InMemoryStorage):
    """Test storage initialization."""
    assert storage.max_logs == 50
    assert len(storage.logs) == 0


def test_add_log(storage: InMemoryStorage):
    """Test adding a log entry."""
    data = SensorData(
        status="normal",
        temperature=25.0,
        gas=3800,
        timestamp="2025-12-17 16:00:00"
    )
    
    storage.add_log(data)
    
    assert len(storage.logs) == 1
    assert storage.logs[0] == data


def test_get_current_status_empty(storage: InMemoryStorage):
    """Test getting current status when storage is empty."""
    current = storage.get_current_status()
    assert current is None


def test_get_current_status(storage: InMemoryStorage):
    """Test getting current status."""
    data1 = SensorData(status="normal", temperature=25.0, gas=3800)
    data2 = SensorData(status="danger", temperature=50.0, gas=5000)
    
    storage.add_log(data1)
    storage.add_log(data2)
    
    current = storage.get_current_status()
    assert current == data2  # Should return the most recent


def test_get_recent_logs(storage: InMemoryStorage):
    """Test getting recent logs."""
    # Add 5 logs
    for i in range(5):
        data = SensorData(
            status="normal",
            temperature=20.0 + i,
            gas=3800 + i * 100
        )
        storage.add_log(data)
    
    recent = storage.get_recent_logs(limit=3)
    
    assert len(recent) == 3
    # Should be in reverse order (newest first)
    assert recent[0].temperature == 24.0
    assert recent[1].temperature == 23.0
    assert recent[2].temperature == 22.0


def test_get_all_logs(storage: InMemoryStorage):
    """Test getting all logs."""
    for i in range(3):
        data = SensorData(
            status="normal",
            temperature=20.0 + i,
            gas=3800
        )
        storage.add_log(data)
    
    all_logs = storage.get_all_logs()
    
    assert len(all_logs) == 3
    assert all_logs[0].temperature == 20.0
    assert all_logs[2].temperature == 22.0


def test_get_stats_empty(storage: InMemoryStorage):
    """Test getting stats when storage is empty."""
    stats = storage.get_stats()
    
    assert stats["danger_count"] == 0
    assert stats["normal_count"] == 0
    assert stats["total_logs"] == 0


def test_get_stats(storage: InMemoryStorage):
    """Test getting statistics."""
    # Add normal readings
    for _ in range(3):
        storage.add_log(SensorData(status="normal", temperature=25.0, gas=3800))
    
    # Add danger readings
    for _ in range(2):
        storage.add_log(SensorData(status="danger", temperature=50.0, gas=5000))
    
    stats = storage.get_stats()
    
    assert stats["normal_count"] == 3
    assert stats["danger_count"] == 2
    assert stats["total_logs"] == 5


def test_clear(storage: InMemoryStorage):
    """Test clearing storage."""
    # Add some data
    for i in range(5):
        storage.add_log(SensorData(status="normal", temperature=25.0, gas=3800))
    
    assert len(storage.logs) == 5
    
    # Clear
    storage.clear()
    
    assert len(storage.logs) == 0
    stats = storage.get_stats()
    assert stats["total_logs"] == 0


def test_max_logs_limit():
    """Test that storage respects max_logs limit."""
    storage = InMemoryStorage(max_logs=5)
    
    # Add 10 logs
    for i in range(10):
        storage.add_log(SensorData(
            status="normal",
            temperature=20.0 + i,
            gas=3800
        ))
    
    # Should only keep the last 5
    assert len(storage.logs) == 5
    assert storage.logs[0].temperature == 25.0  # First of the last 5
    assert storage.logs[4].temperature == 29.0  # Last one


def test_storage_copy_independence(storage: InMemoryStorage):
    """Test that get_all_logs returns a copy."""
    storage.add_log(SensorData(status="normal", temperature=25.0, gas=3800))
    
    logs_copy = storage.get_all_logs()
    logs_copy.clear()
    
    # Original storage should still have the log
    assert len(storage.logs) == 1
