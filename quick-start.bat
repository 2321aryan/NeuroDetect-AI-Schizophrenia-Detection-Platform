@echo off
echo 🚀 Quick Start - NeuroDetect AI Platform
echo ========================================

echo.
echo [1/3] Starting Backend Server...
cd project_bolt_backend
start "Backend Server" cmd /k "node server.js"
cd ..

echo.
echo [2/3] Starting AI Model API...
start "AI Model API" cmd /k "python ai_model_api.py"

echo.
echo [3/3] Starting Frontend...
start "Frontend" cmd /k "npm run dev"

echo.
echo ✅ All services starting!
echo.
echo 🌐 Open: http://localhost:5173
echo.
pause