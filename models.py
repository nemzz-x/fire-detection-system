"""Data models for Fire Detection System."""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
from datetime import datetime


class SensorData(BaseModel):
    """Sensor data model with validation."""
    
    status: Literal["danger", "normal"] = Field(
        ...,
        description="Current fire detection status"
    )
    temperature: float = Field(
        ...,
        ge=-50,
        le=150,
        description="Temperature in Celsius (-50 to 150°C)"
    )
    gas: int = Field(
        ...,
        ge=0,
        le=10000,
        description="Gas concentration in ppm (0-10000)"
    )
    timestamp: Optional[str] = Field(
        default=None,
        description="Timestamp of the reading (auto-generated if not provided)"
    )
    
    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """Validate temperature is within reasonable range."""
        if v < -50 or v > 150:
            raise ValueError("Temperature must be between -50°C and 150°C")
        return round(v, 2)
    
    @field_validator('gas')
    @classmethod
    def validate_gas(cls, v: int) -> int:
        """Validate gas concentration is non-negative."""
        if v < 0:
            raise ValueError("Gas concentration cannot be negative")
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "danger",
                    "temperature": 45.5,
                    "gas": 4500
                },
                {
                    "status": "normal",
                    "temperature": 22.0,
                    "gas": 3800
                }
            ]
        }
    }


class StatusResponse(BaseModel):
    """Response model for status updates."""
    
    message: str = Field(..., description="Response message")
    timestamp: str = Field(..., description="Server timestamp")
    data: Optional[SensorData] = Field(None, description="Submitted sensor data")


class DashboardStats(BaseModel):
    """Dashboard statistics model."""
    
    current_status: SensorData
    danger_count: int = Field(ge=0, description="Total danger alerts")
    normal_count: int = Field(ge=0, description="Total normal readings")
    total_logs: int = Field(ge=0, description="Total log entries")
    recent_logs: list[SensorData] = Field(
        default_factory=list,
        description="Recent sensor readings"
    )


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Service health status")
    timestamp: str = Field(..., description="Current server time")
    version: str = Field(..., description="Application version")
    uptime_seconds: Optional[float] = Field(None, description="Service uptime in seconds")
