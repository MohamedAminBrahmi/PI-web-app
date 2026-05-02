#!/bin/bash

# Build and run the entire ML Dashboard application with Docker Compose

echo "🚀 Starting ML Dashboard Application..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build and start services
echo "📦 Building Docker images..."
docker-compose build

echo ""
echo "🐳 Starting services..."
docker-compose up -d

echo ""
echo "✅ Application started successfully!"
echo ""
echo "📱 Frontend: http://localhost:4200"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "📊 ML Dashboard is now running!"
echo ""
echo "To stop the application, run: docker-compose down"
echo "To view logs, run: docker-compose logs -f"
