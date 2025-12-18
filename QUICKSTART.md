# Fire Detection System

Clean and organized fire detection monitoring system.

## 📂 Project Structure

```
fire-detection-system/
├── backend/              # Backend application
│   ├── __init__.py      
│   └── main.py          # FastAPI application
├── frontend/             # Frontend templates
│   └── templates/
│       └── dashboard.html
├── docker/               # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt      # Python dependencies
├── run.sh               # Quick start script
└── README.md
```

## 🚀 Quick Start

### Method 1: Using run script (Linux/Mac)
```bash
chmod +x run.sh
./run.sh
```

### Method 2: Manual
```bash
pip install -r requirements.txt
cd backend
python main.py
```

### Method 3: Docker
```bash
cd docker
docker-compose up -d
```

## 📡 API Endpoints

- `GET /` - Dashboard
- `GET /health` - Health check
- `POST /status` - Submit sensor data
- `GET /api/stats` - Get statistics
- `DELETE /api/logs` - Clear logs

## 🔧 Configuration

Set via environment variables:
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `MAX_LOGS` - Max logs to store (default: 100)

## 📊 Data Storage

Data is stored in `data.json` file (auto-created).
