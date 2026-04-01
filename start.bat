@echo off
REM Emergency Triage System - Windows Startup Script

echo ========================================
echo Emergency Triage Decision Support System
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Using system Python.
)

REM Check if dependencies are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Dependencies not found. Installing...
    pip install -r requirements.txt
    echo.
)

REM Check if database exists
if not exist "database\triage_system.db" (
    echo.
    echo Database not found. Running setup...
    python scripts\setup_system.py
    echo.
)

REM Check if model exists
if not exist "models\saved_models\triage_classifier.pkl" (
    echo.
    echo ML model not found. Training model...
    python scripts\train_model.py
    echo.
)

REM Start the application
echo.
echo ========================================
echo Starting Emergency Triage System...
echo ========================================
echo.
echo Access points:
echo   - Patient Intake:     http://localhost:5000/
echo   - Dispatcher Console: http://localhost:5000/dispatcher
echo   - Nurse Queue:        http://localhost:5000/nurse
echo   - KPI Dashboard:      http://localhost:5000/dashboard
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
