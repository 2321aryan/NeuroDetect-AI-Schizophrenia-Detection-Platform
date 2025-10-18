@echo off
echo 🚀 Starting NeuroDetect AI - All Services
echo ==========================================

echo.
echo 🔧 Killing any existing processes...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul

echo.
echo ⏳ Starting services in order...

echo [1/4] 🗄️  Backend Server (Port 5002)...
cd project_bolt_backend
Start-Process cmd -ArgumentList "/k", "node server.js"
cd ..

timeout /t 3 /nobreak >nul

echo [2/4] 🧠 AI Model API (Port 8000)...
Start-Process cmd -ArgumentList "/k", "python ai_model_api.py"

timeout /t 2 /nobreak >nul

echo [3/4] 🩺 Symptom AI (Port 8001)...
Start-Process cmd -ArgumentList "/k", "python symptom_checklist_ai.py"

timeout /t 2 /nobreak >nul

echo [4/4] 🌐 Frontend (Port 5173)...
Start-Process cmd -ArgumentList "/k", "npm run dev"

echo.
echo ⏳ Waiting for all services to initialize...
timeout /t 10 /nobreak >nul

echo.
echo 🎉 ALL SERVICES STARTED!
echo ==========================================
echo.
echo 🌐 Open: http://localhost:5173
echo 📊 Backend: http://localhost:5002
echo 🧠 AI API: http://localhost:8000
echo 🩺 Symptom AI: http://localhost:8001
echo.
echo ✅ Your NeuroDetect AI Platform is ready!
echo.
pause