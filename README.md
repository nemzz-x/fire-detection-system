# Fire Detection Dashboard
![f](images/plate1.jpeg)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124.4-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A simple, real-time fire detection monitoring system with temperature and gas level tracking. Features a modern web dashboard with live data visualization and a REST API for sensor integration.

## ✨ Features

- 🔥 **Real-time Monitoring** - Live status updates with danger/normal detection
- 📊 **Data Visualization** - Interactive Chart.js graphs with dual Y-axis tracking
- 🔄 **Auto-refresh** - Dashboard updates every 2 seconds
- 🎨 **Modern UI** - Professional dark-themed interface with glassmorphism
- 🚀 **FastAPI Backend** - High-performance async API
- 💾 **JSON Storage** - Simple file-based data persistence
- 📝 **Logging** - Structured logging for monitoring
- 🐳 **Docker Ready** - Containerized deployment support

## 🏗️ Architecture

```
fire-detection-system/
├── app/
│   ├── backend/
│   │   ├── __init__.py
│   │   └── main.py      # Complete API application
│   └── frontend/
│       └── templates/
│           └── dashboard.html   # Web dashboard
├── docker/
│   ├── Dockerfile       # Container configuration
│   └── docker-compose.yml   # Docker compose setup
├── requirements.txt     # Python dependencies
├── data.json            # JSON storage (auto-created)
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fire-detection-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   cd app/backend
   python main.py
   ```
   
   Or with uvicorn:
   ```bash
   uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the dashboard**
   - Dashboard: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📡 API Reference

### Endpoints

#### `GET /`
Main dashboard interface (HTML)

#### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-18 16:00:00",
  "version": "1.0.0",
  "uptime_seconds": 123.45
}
```

#### `POST /status`
Update sensor status with new readings

**Request Body:**
```json
{
  "status": "danger",
  "temperature": 45.5,
  "gas": 4500
}
```

**Response:**
```json
{
  "message": "Status updated successfully",
  "timestamp": "2025-12-18 16:00:00",
  "data": {
    "status": "danger",
    "temperature": 45.5,
    "gas": 4500,
    "timestamp": "2025-12-18 16:00:00"
  }
}
```

#### `GET /api/stats`
Get current statistics

**Response:**
```json
{
  "danger_count": 5,
  "normal_count": 95,
  "total_logs": 100,
  "current_status": {
    "status": "normal",
    "temperature": 22.0,
    "gas": 3800,
    "timestamp": "2025-12-18 16:00:00"
  },
  "timestamp": "2025-12-18 16:00:00"
}
```

#### `DELETE /api/logs`
Clear all stored logs

**Response:**
```json
{
  "message": "All logs cleared successfully",
  "timestamp": "2025-12-18 16:00:00"
}
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
cd docker
docker-compose up -d
```

### Using Docker

```bash
# Build the image
docker build -f docker/Dockerfile -t fire-detection-system .

# Run the container
docker run -d -p 8000:8000 --name fire-detection fire-detection-system
```

## 🔧 Configuration

Configure via environment variables:

```bash
HOST=0.0.0.0          # Server host
PORT=8000             # Server port
MAX_LOGS=100          # Maximum logs to keep in memory
```

## 📊 Data Validation

- **Temperature**: -50°C to 150°C (2 decimal places)
- **Gas Level**: 0 to 10000 ppm (integer)
- **Status**: "danger" or "normal"
- **Timestamp**: Auto-generated if not provided

## 🔌 Arduino/IoT Integration

Send sensor data via HTTP POST:

```cpp
// Example Arduino code
#include <WiFi.h>
#include <HTTPClient.h>

void sendSensorData(String status, float temp, int gas) {
  HTTPClient http;
  http.begin("http://your-server:8000/status");
  http.addHeader("Content-Type", "application/json");
  
  String payload = "{\"status\":\"" + status + 
                   "\",\"temperature\":" + String(temp) + 
                   ",\"gas\":" + String(gas) + "}";
  
  int httpCode = http.POST(payload);
  http.end();
}
```

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

**Request Body:**
```json
{
  "status": "danger",
  "temperature": 45.5,
  "gas": 4500
}
```

**Response:**
```json
{
  "message": "Status updated successfully",
  "timestamp": "2025-12-17 16:00:00",
  "data": {
    "status": "danger",
    "temperature": 45.5,
    "gas": 4500,
    "timestamp": "2025-12-17 16:00:00"
  }
}
```

**Validation Rules:**
- `status`: Must be either "danger" or "normal"
- `temperature`: Float, 0-100°C (validated range: -50 to 150°C)
- `gas`: Integer, 0-10000 ppm (must be non-negative)

#### `GET /api/stats`
Get current statistics

**Response:**
```json
{
  "danger_count": 5,
  "normal_count": 15,
  "total_logs": 20,
  "current_status": { ... },
  "timestamp": "2025-12-17 16:00:00"
}
```

#### `DELETE /api/logs`
Clear all stored logs (admin endpoint)

## ⚙️ Configuration

Create a `.env` file in the project root (see `.env.example`):

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=false

# Application
APP_NAME=Fire Detection System
APP_VERSION=1.0.0
DEBUG=false

# Logging
LOG_LEVEL=INFO

# Storage
MAX_LOGS=100
```

## 🐳 Docker Deployment

### Using Docker

```bash
# Build the image
docker build -t fire-detection-system .

# Run the container
docker run -p 8000:8000 fire-detection-system
```

### Using Docker Compose

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## ☁️ Cloud Deployment

### Render

1. Create a new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy!

### Railway

1. Create new project from GitHub repo
2. Railway auto-detects Python and uses `requirements.txt`
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy!

### AWS/VPS

```bash
# Install dependencies
pip install -r requirements.txt

# Run with production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🧪 Testing

### Run all tests
```bash
pytest tests/ -v
```

### Run with coverage
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

### Run specific test files
```bash
pytest tests/test_api.py -v
pytest tests/test_models.py -v
pytest tests/test_storage.py -v
```

## 🛠️ Development

### Install development dependencies
```bash
pip install -r requirements.txt
```

### Code formatting
```bash
black .
```

### Linting
```bash
ruff check .
```

### Run in development mode
```bash
uvicorn main:app --reload --log-level debug
```

## 📊 Tech Stack

- **Backend**: FastAPI (Python async web framework)
- **Validation**: Pydantic (data validation and settings)
- **Templating**: Jinja2 (HTML rendering)
- **Visualization**: Chart.js (interactive charts)
- **Server**: Uvicorn (ASGI server)
- **Testing**: Pytest + HTTPX
- **Containerization**: Docker

## 🔒 Security Considerations

- Input validation with Pydantic models
- CORS configuration for cross-origin requests
- Environment-based configuration (no hardcoded secrets)
- Health check endpoint for monitoring
- Structured logging for audit trails

## 📈 Performance

- Async/await for non-blocking operations
- In-memory storage for fast access (configurable to database)
- Automatic log rotation (max 100 entries by default)
- Efficient Chart.js rendering with canvas

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Dashboard not loading
- Check that the server is running on the correct port
- Verify `templates/dashboard.html` exists
- Check browser console for JavaScript errors

### API validation errors
- Ensure temperature is within -50 to 150°C
- Ensure gas is non-negative
- Status must be "danger" or "normal"

### Tests failing
- Install test dependencies: `pip install pytest pytest-cov httpx`
- Ensure all modules are importable
- Check Python version (3.11+ required)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review the architecture documentation in `ARCHITECTURE.md`

---

**Built with ❤️ using FastAPI and modern web technologies**
