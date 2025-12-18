#!/bin/bash

echo "🔥 Starting Fire Detection System in Docker..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✓ Docker found: $(docker --version)"
echo ""

# Stop and remove existing container if running
if [ "$(docker ps -aq -f name=fire-detection-system)" ]; then
    echo "🛑 Stopping existing container..."
    docker stop fire-detection-system 2>/dev/null
    docker rm fire-detection-system 2>/dev/null
fi

echo "🔨 Building Docker image..."
docker build -f docker/Dockerfile -t fire-detection-system . || {
    echo "❌ Docker build failed!"
    exit 1
}

echo "✓ Docker image built successfully"
echo ""
echo "🚀 Starting container..."

docker run -d \
  --name fire-detection-system \
  -p 8000:8000 \
  -v "$(pwd)/data.json:/app/data.json" \
  --restart unless-stopped \
  fire-detection-system

if [ $? -eq 0 ]; then
    echo "✓ Container started successfully!"
    echo ""
    echo "📍 Dashboard: http://localhost:8000"
    echo "📍 API Docs: http://localhost:8000/docs"
    echo "📍 Health: http://localhost:8000/health"
    echo ""
    echo "📋 View logs: docker logs -f fire-detection-system"
    echo "🛑 Stop server: docker stop fire-detection-system"
    echo ""
    echo "⏳ Waiting for server to start..."
    sleep 3
    docker logs fire-detection-system
else
    echo "❌ Failed to start container"
    exit 1
fi
