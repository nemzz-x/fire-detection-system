from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Store logs in memory
logs = []
current_status = {"status": "unknown", "temperature": 0, "gas": 0, "timestamp": ""}

@app.post("/status")
async def update_status(data: dict):
    global current_status
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_status = data
    logs.append(data)
    return {"message": "Status updated"}

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Basic statistics
    danger_count = sum(1 for log in logs if log["status"] == "danger")
    normal_count = sum(1 for log in logs if log["status"] == "normal")
    
    # Get last 20 logs as a list (newest first for display)
    recent_logs = list(reversed(logs[-20:]))
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "current": current_status,
        "logs": recent_logs,  # pass as list, not iterator
        "danger_count": danger_count,
        "normal_count": normal_count
    })


if __name__ == "__main__":
    import uvicorn
    # Use 0.0.0.0 to listen on all interfaces (required for cloud hosting)
    # Port should come from environment variable (most platforms set PORT automatically)
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
