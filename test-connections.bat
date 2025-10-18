@echo off
echo ========================================
echo Testing All Service Connections
echo ========================================

echo.
echo [1/4] Testing Backend Server (Port 5002)...
curl -s http://localhost:5002 > nul
if %errorlevel% == 0 (
    echo ✅ Backend Server: RUNNING
) else (
    echo ❌ Backend Server: NOT RUNNING
)

echo.
echo [2/4] Testing AI Model API (Port 8000)...
curl -s http://localhost:8000/health > nul
if %errorlevel% == 0 (
    echo ✅ AI Model API: RUNNING
) else (
    echo ❌ AI Model API: NOT RUNNING
)

echo.
echo [3/4] Testing Symptom Checklist AI (Port 8001)...
curl -s http://localhost:8001/health > nul
if %errorlevel% == 0 (
    echo ✅ Symptom Checklist AI: RUNNING
) else (
    echo ❌ Symptom Checklist AI: NOT RUNNING
)

echo.
echo [4/4] Testing Symptom Checklist Integration...
curl -s -X POST http://localhost:5002/api/symptom-checklist/health > nul
if %errorlevel% == 0 (
    echo ✅ Symptom Checklist Integration: WORKING
) else (
    echo ❌ Symptom Checklist Integration: NOT WORKING
)

echo.
echo ========================================
echo Connection Test Complete
echo ========================================
echo.
pause