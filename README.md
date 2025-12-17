# Fire Detection Dashboard

Real-time fire detection monitoring system with temperature and gas level tracking.

## Features
- 🔥 Live status monitoring (Danger/Normal)
- 📊 Historical data visualization with Chart.js area charts
- 🔄 Auto-refresh every 2 seconds
- 📈 Dual Y-axis tracking for temperature & gas levels
- 🎨 Professional dark-themed dashboard

## Installation

```bash
pip install -r requirements.txt
```

## Running Locally

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then visit `http://localhost:8000`

## API Endpoints

### POST /status
Update system status with sensor data.

**Example Request:**
```json
{
  "status": "danger",
  "temperature": 45,
  "gas": 4500
}
```

### GET /
Dashboard homepage (HTML interface)

## Deployment

Compatible with:
- **Render** (recommended for free hosting)
- **Railway**
- **PythonAnywhere**
- **AWS/DigitalOcean/VPS**

The app automatically uses the `PORT` environment variable when available (defaults to 8000).

## Tech Stack
- FastAPI (Python web framework)
- Jinja2 (templating)
- Chart.js (data visualization)
- Uvicorn (ASGI server)
