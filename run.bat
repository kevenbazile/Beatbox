@echo off
echo ========================================
echo   AI Music Generator - Docker Setup
echo ========================================
echo.

REM Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or running!
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo ✅ Docker is available
echo.

REM Create generated_songs directory
if not exist "generated_songs" (
    mkdir generated_songs
    echo ✅ Created generated_songs directory
)

echo 🏗️ Building AI Music Generator...
echo This may take 10-20 minutes on first run...
echo.

REM Build and run the container
docker-compose up --build

echo.
echo 🎵 AI Music Generator should be running at: http://localhost:5000
echo.
pause