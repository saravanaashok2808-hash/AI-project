@echo off
chcp 65001 > nul
cd /d "%~dp0.."
echo =====================================================================
echo  தமிழ்நாடு அரசுத் திட்ட வழிகாட்டி
echo  Tamil Nadu Multilingual Voice-Based Government Scheme Assistant
echo =====================================================================
echo.

:: 1. Check or setup Python Virtual Environment
if not exist "%CD%\backend\venv\Scripts\python.exe" (
    echo [INFO] Python virtual environment not found. Setting up backend\venv...
    where python >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python is not installed or not in system PATH!
        echo Please install Python 3.10 or 3.11 from python.org and tick "Add to PATH".
        pause
        exit /b 1
    )
    python -m venv backend\venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [INFO] Installing backend dependencies (this may take a few minutes)...
    "%CD%\backend\venv\Scripts\python.exe" -m pip install --upgrade pip
    "%CD%\backend\venv\Scripts\python.exe" -m pip install -r backend\requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install backend dependencies.
        pause
        exit /b 1
    )
)

set PYTHON="%CD%\backend\venv\Scripts\python.exe"

:: 2. Check or setup Frontend node_modules
if not exist "%CD%\frontend\node_modules" (
    echo [INFO] Frontend dependencies not found. Running npm install...
    where npm >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Node.js/npm is not installed or not in system PATH!
        echo Please install Node.js from nodejs.org to run the frontend.
        pause
        exit /b 1
    )
    pushd "%CD%\frontend"
    call npm.cmd install
    popd
    if errorlevel 1 (
        echo [ERROR] npm install failed.
        pause
        exit /b 1
    )
)

echo [1/3] Verifying Scheme Database...
%PYTHON% scripts\ingest_schemes.py
if errorlevel 1 (
    echo [ERROR] Error initializing scheme database!
    pause
    exit /b 1
)
echo.

echo [2/3] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "TN Scheme Assistant - Backend" /D "%CD%\backend" %PYTHON% -m uvicorn app.main:app --host 127.0.0.1 --port 8000

echo [3/3] Starting Vite Frontend on http://127.0.0.1:5173 ...
start "TN Scheme Assistant - Frontend" /D "%CD%\frontend" cmd /c "npm.cmd run dev -- --host 127.0.0.1 --port 5173"

echo.
echo =====================================================================
echo  Both servers have been launched!
echo  Backend:  http://127.0.0.1:8000/docs
echo  Frontend: http://127.0.0.1:5173/
echo =====================================================================
timeout /t 5 > nul
start http://127.0.0.1:5173/
