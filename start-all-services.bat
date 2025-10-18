@echo off
echo ========================================
echo 🚀 Enhanced Schizophrenia Detection Platform v2.0
echo ========================================

echo.
echo 🔧 Checking prerequisites...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

echo 🔄 Starting Enhanced Services...
echo.

echo [1/4] 🗄️  Starting Enhanced Backend Server (Port 5002)...
echo        Features: Authentication, Database, Audit Logging, Security
cd project_bolt_backend
start "Enhanced Backend Server" cmd /k "node server.js"
cd ..

echo.
echo [2/4] 🧠 Starting Advanced AI Model API (Port 8000)...
echo        Features: Real EEG/MRI Processing, Deep Learning Models
start "Advanced AI Model API" cmd /k "python ai_model_api.py"

echo.
echo [3/4] 🩺 Starting Enhanced Symptom Checklist AI (Port 8001)...
echo        Features: Intelligent Questioning, Clinical Decision Support
start "Enhanced Symptom Checklist AI" cmd /k "python symptom_checklist_ai.py"

echo.
echo [4/4] 🌐 Starting Progressive Web App Frontend (Port 5173)...
echo        Features: PWA, Offline Support, Enhanced UI/UX
start "PWA Frontend" cmd /k "npm run dev"

echo.
echo ⏳ Waiting for services to initialize...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo 🎉 All Enhanced Services Started!
echo ========================================
echo.
echo 🌟 NEW FEATURES IN v2.0:
echo   ✅ User Authentication & Authorization
echo   ✅ PostgreSQL Database Integration
echo   ✅ Real AI Model Processing
echo   ✅ Advanced Security Features
echo   ✅ Progressive Web App (PWA)
echo   ✅ Audit Logging & Compliance
echo   ✅ Enhanced Error Handling
echo   ✅ Performance Optimizations
echo   ✅ Real-time Notifications
echo   ✅ Mobile Responsive Design
echo.
echo 🔗 Access Points:
echo   🖥️  Frontend (PWA):         http://localhost:5173
echo   🔐 Authentication:         http://localhost:5173/login
echo   🏥 Backend API:            http://localhost:5002
echo   🧠 AI Model API:           http://localhost:8000
echo   🩺 Symptom Checklist AI:   http://localhost:8001
echo.
echo 📊 Health Checks:
echo   Backend:     http://localhost:5002/api/health
echo   AI Models:   http://localhost:8000/health
echo   Symptoms:    http://localhost:8001/health
echo.
echo 🔧 Admin Features:
echo   - User Management
echo   - Audit Logs
echo   - System Monitoring
echo   - Database Management
echo.
echo 📱 Mobile Features:
echo   - Install as PWA
echo   - Offline Functionality
echo   - Push Notifications
echo   - Touch Optimized
echo.
echo ⚠️  IMPORTANT NOTES:
echo   - First time? Register at: http://localhost:5173/register
echo   - Demo credentials available on login page
echo   - Database will auto-initialize on first run
echo   - AI models will load automatically
echo.
echo Press any key to exit this window...
pause > nul