"""Storage layer for Fire Detection System."""

from abc import ABC, abstractmethod
from typing import List, Optional
from models import SensorData
from config import settings
import logging

logger = logging.getLogger(__name__)


class StorageInterface(ABC):
    """Abstract interface for storage implementations."""
    
    @abstractmethod
    def add_log(self, data: SensorData) -> None:
        """Add a new sensor log entry."""
        pass
    
    @abstractmethod
    def get_current_status(self) -> Optional[SensorData]:
        """Get the most recent sensor reading."""
        pass
    
    @abstractmethod
    def get_recent_logs(self, limit: int = 20) -> List[SensorData]:
        """Get recent log entries."""
        pass
    
    @abstractmethod
    def get_all_logs(self) -> List[SensorData]:
        """Get all log entries."""
        pass
    
    @abstractmethod
    def get_stats(self) -> dict:
        """Get statistics about stored data."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all stored data."""
        pass


class InMemoryStorage(StorageInterface):
    """In-memory storage implementation using a list."""
    
    def __init__(self, max_logs: int = None):
        """Initialize in-memory storage.
        
        Args:
            max_logs: Maximum number of logs to keep. If None, uses settings.max_logs
        """
        self.logs: List[SensorData] = []
        self.max_logs = max_logs or settings.max_logs
        logger.info(f"Initialized in-memory storage with max_logs={self.max_logs}")
    
    def add_log(self, data: SensorData) -> None:
        """Add a new sensor log entry.
        
        Args:
            data: Sensor data to store
        """
        self.logs.append(data)
        
        # Trim logs if exceeding max_logs
        if len(self.logs) > self.max_logs:
            removed_count = len(self.logs) - self.max_logs
            self.logs = self.logs[-self.max_logs:]
            logger.debug(f"Trimmed {removed_count} old log entries")
        
        logger.debug(f"Added log entry: {data.status} at {data.timestamp}")
    
    def get_current_status(self) -> Optional[SensorData]:
        """Get the most recent sensor reading.
        
        Returns:
            Most recent SensorData or None if no logs exist
        """
        if not self.logs:
            return None
        return self.logs[-1]
    
    def get_recent_logs(self, limit: int = 20) -> List[SensorData]:
        """Get recent log entries.
        
        Args:
            limit: Maximum number of recent logs to return
            
        Returns:
            List of recent SensorData entries (newest first)
        """
        return list(reversed(self.logs[-limit:]))
    
    def get_all_logs(self) -> List[SensorData]:
        """Get all log entries.
        
        Returns:
            List of all SensorData entries
        """
        return self.logs.copy()
    
    def get_stats(self) -> dict:
        """Get statistics about stored data.
        
        Returns:
            Dictionary with danger_count, normal_count, and total_logs
        """
        danger_count = sum(1 for log in self.logs if log.status == "danger")
        normal_count = sum(1 for log in self.logs if log.status == "normal")
        
        return {
            "danger_count": danger_count,
            "normal_count": normal_count,
            "total_logs": len(self.logs)
        }
    
    def clear(self) -> None:
        """Clear all stored data."""
        count = len(self.logs)
        self.logs.clear()
        logger.info(f"Cleared {count} log entries from storage")


# Global storage instance
storage = InMemoryStorage()
