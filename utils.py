"""Utility functions for Fire Detection System."""

import logging
import sys
from datetime import datetime
from config import settings


def setup_logging() -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured at {settings.log_level} level")


def get_current_timestamp() -> str:
    """Get current timestamp in standard format.
    
    Returns:
        Formatted timestamp string (YYYY-MM-DD HH:MM:SS)
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_temperature(temp: float) -> str:
    """Format temperature with unit.
    
    Args:
        temp: Temperature value in Celsius
        
    Returns:
        Formatted temperature string (e.g., "25.5°C")
    """
    return f"{temp:.1f}°C"


def format_gas_level(gas: int) -> str:
    """Format gas level with unit.
    
    Args:
        gas: Gas concentration in ppm
        
    Returns:
        Formatted gas level string (e.g., "4500 ppm")
    """
    return f"{gas} ppm"


def is_danger_condition(temperature: float, gas: int) -> bool:
    """Determine if sensor readings indicate danger.
    
    Args:
        temperature: Temperature in Celsius
        gas: Gas concentration in ppm
        
    Returns:
        True if conditions indicate danger, False otherwise
    """
    # Example thresholds (can be made configurable)
    TEMP_THRESHOLD = 40.0  # °C
    GAS_THRESHOLD = 4000   # ppm
    
    return temperature > TEMP_THRESHOLD or gas > GAS_THRESHOLD
