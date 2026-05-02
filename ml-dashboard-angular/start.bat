@echo off
REM Windows batch script to start ML Dashboard with Docker Compose

echo.
echo 🚀 Starting ML Dashboard Application...
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Build and start services
echo 📦 Building Docker images...
docker-compose build

echo.
echo 🐳 Starting services...
docker-compose up -d

echo.
echo ✅ Application started successfully!
echo.
echo 📱 Frontend: http://localhost:4200
echo 🔌 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo 📊 ML Dashboard is now running!
echo.
echo To stop the application, run: docker-compose down
echo To view logs, run: docker-compose logs -f
echo.
pause
