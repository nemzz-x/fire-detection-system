"""Fire Detection System - Main Application.

A real-time fire detection monitoring system with temperature and gas level tracking.
Provides a web dashboard and REST API for sensor data collection and visualization.
"""

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import time

from config import settings
from models import SensorData, StatusResponse, HealthResponse
from storage import StorageInterface, storage
from utils import setup_logging, get_current_timestamp

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Track application start time for uptime calculation
start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Server running on {settings.host}:{settings.port}")
    yield
    logger.info("Shutting down application")


# Initialize FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Real-time fire detection monitoring system with temperature and gas level tracking",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Initialize templates
templates = Jinja2Templates(directory="templates")


def get_storage() -> StorageInterface:
    """Dependency injection for storage.
    
    Returns:
        Storage instance
    """
    return storage


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint.
    
    Returns:
        Health status information including uptime
    """
    uptime = time.time() - start_time
    
    return HealthResponse(
        status="healthy",
        timestamp=get_current_timestamp(),
        version=settings.app_version,
        uptime_seconds=round(uptime, 2)
    )


@app.post("/status", response_model=StatusResponse, tags=["Sensors"])
async def update_status(
    data: SensorData,
    store: StorageInterface = Depends(get_storage)
):
    """Update system status with new sensor data.
    
    Args:
        data: Sensor data including status, temperature, and gas levels
        store: Storage instance (injected)
        
    Returns:
        Confirmation response with timestamp
        
    Raises:
        HTTPException: If data validation fails
    """
    try:
        # Add timestamp if not provided
        if not data.timestamp:
            data.timestamp = get_current_timestamp()
        
        # Store the data
        store.add_log(data)
        
        logger.info(
            f"Status updated: {data.status} | "
            f"Temp: {data.temperature}°C | "
            f"Gas: {data.gas} ppm"
        )
        
        return StatusResponse(
            message="Status updated successfully",
            timestamp=get_current_timestamp(),
            data=data
        )
        
    except Exception as e:
        logger.error(f"Error updating status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update status: {str(e)}"
        )


@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
async def dashboard(
    request: Request,
    store: StorageInterface = Depends(get_storage)
):
    """Render the main dashboard.
    
    Args:
        request: FastAPI request object
        store: Storage instance (injected)
        
    Returns:
        Rendered HTML dashboard
    """
    try:
        # Get current status
        current = store.get_current_status()
        
        # Default values if no data exists (use dict, not SensorData)
        if current is None:
            current_dict = {
                "status": "normal",
                "temperature": 0,
                "gas": 0,
                "timestamp": ""
            }
        else:
            current_dict = current.model_dump()
        
        # Get statistics
        stats = store.get_stats()
        
        # Get recent logs (newest first for display)
        recent_logs = store.get_recent_logs(limit=20)
        # Convert SensorData objects to dicts for JSON serialization
        logs_dict = [log.model_dump() for log in recent_logs]
        
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "current": current_dict,
            "logs": logs_dict,
            "danger_count": stats["danger_count"],
            "normal_count": stats["normal_count"]
        })
        
    except Exception as e:
        logger.error(f"Error rendering dashboard: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to render dashboard: {str(e)}"
        )


@app.get("/api/stats", tags=["API"])
async def get_stats(store: StorageInterface = Depends(get_storage)):
    """Get current statistics.
    
    Args:
        store: Storage instance (injected)
        
    Returns:
        Statistics including counts and current status
    """
    stats = store.get_stats()
    current = store.get_current_status()
    
    return {
        **stats,
        "current_status": current.model_dump() if current else None,
        "timestamp": get_current_timestamp()
    }


@app.delete("/api/logs", tags=["API"])
async def clear_logs(store: StorageInterface = Depends(get_storage)):
    """Clear all stored logs (admin endpoint).
    
    Args:
        store: Storage instance (injected)
        
    Returns:
        Confirmation message
    """
    store.clear()
    logger.warning("All logs cleared via API")
    
    return {
        "message": "All logs cleared successfully",
        "timestamp": get_current_timestamp()
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
