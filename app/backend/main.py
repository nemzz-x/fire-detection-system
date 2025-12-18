"""Fire Detection System - Simplified Application."""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
import json
import os
import logging
import time

# ==================== Configuration ====================
APP_NAME = "Fire Detection System"
APP_VERSION = "1.0.0"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
MAX_LOGS = int(os.getenv("MAX_LOGS", 100))
DATA_FILE = "data.json"

# ==================== Logging Setup ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ==================== Data Models ====================
class SensorData(BaseModel):
    status: Literal["danger", "normal"]
    temperature: float = Field(ge=-50, le=150)
    gas: int = Field(ge=0, le=10000)
    timestamp: Optional[str] = None

class StatusResponse(BaseModel):
    message: str
    timestamp: str
    data: SensorData

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    uptime_seconds: float

# ==================== Storage Functions ====================
def load_logs():
    """Load logs from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return [SensorData(**item) for item in data]
    except Exception as e:
        logger.error(f"Error loading logs: {e}")
        return []

def save_logs(logs):
    """Save logs to JSON file."""
    try:
        data = [log.model_dump() for log in logs]
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving logs: {e}")

def add_log(sensor_data: SensorData):
    """Add a log entry."""
    logs = load_logs()
    
    # Add timestamp if not provided
    if not sensor_data.timestamp:
        sensor_data.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    logs.append(sensor_data)
    
    # Keep only last MAX_LOGS entries
    if len(logs) > MAX_LOGS:
        logs = logs[-MAX_LOGS:]
    
    save_logs(logs)
    logger.info(f"Status: {sensor_data.status} | Temp: {sensor_data.temperature}°C | Gas: {sensor_data.gas} ppm")

def get_current_status():
    """Get most recent log."""
    logs = load_logs()
    return logs[-1] if logs else None

def get_recent_logs(limit=20):
    """Get recent logs (newest first)."""
    logs = load_logs()
    return list(reversed(logs[-limit:]))

def get_stats():
    """Get statistics."""
    logs = load_logs()
    danger_count = sum(1 for log in logs if log.status == "danger")
    normal_count = sum(1 for log in logs if log.status == "normal")
    return {
        "danger_count": danger_count,
        "normal_count": normal_count,
        "total_logs": len(logs)
    }

def clear_logs():
    """Clear all logs."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    logger.info("All logs cleared")

# ==================== FastAPI Application ====================
start_time = time.time()

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Real-time fire detection monitoring system"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/frontend/templates")

# ==================== Routes ====================
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        version=APP_VERSION,
        uptime_seconds=round(time.time() - start_time, 2)
    )

@app.post("/status", response_model=StatusResponse)
async def update_status(data: SensorData):
    """Update system status with new sensor data."""
    try:
        add_log(data)
        return StatusResponse(
            message="Status updated successfully",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data=data
        )
    except Exception as e:
        logger.error(f"Error updating status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the main dashboard."""
    try:
        current = get_current_status()
        
        # Default values if no data
        if current is None:
            current_dict = {
                "status": "normal",
                "temperature": 0,
                "gas": 0,
                "timestamp": ""
            }
        else:
            current_dict = current.model_dump()
        
        stats = get_stats()
        recent_logs = get_recent_logs(limit=20)
        logs_dict = [log.model_dump() for log in recent_logs]
        
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "current": current_dict,
            "logs": logs_dict,
            "danger_count": stats["danger_count"],
            "normal_count": stats["normal_count"]
        })
    except Exception as e:
        logger.error(f"Error rendering dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def api_get_stats():
    """Get current statistics."""
    stats = get_stats()
    current = get_current_status()
    return {
        **stats,
        "current_status": current.model_dump() if current else None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.delete("/api/logs")
async def api_clear_logs():
    """Clear all stored logs."""
    clear_logs()
    return {
        "message": "All logs cleared successfully",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
