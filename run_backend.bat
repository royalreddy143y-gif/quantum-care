@echo off
title QuantumCare - Backend Server
echo ===================================================
echo   QuantumCare - Starting FastAPI Backend Server
echo   Hybrid Quantum-Classical Early Disease Detection
echo ===================================================
echo.

set PATH=C:\Users\HP\AppData\Local\Programs\Python\Python311;C:\Users\HP\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
cd /d "%~dp0backend"

:: Check if virtual environment exists
if not exist ".venv" (
    echo [*] Creating Python virtual environment (.venv)...
    python -m venv .venv
    if errorlevel 1 (
        echo [!] Error: Python not found in PATH. Please install Python 3.10+ from python.org.
        pause
        exit /b 1
    )
)

echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [*] Installing / Verifying dependencies (requirements.txt)...
pip install -r requirements.txt
if errorlevel 1 (
    echo [!] Warning: Some dependencies failed to install. Continuing...
)

echo.
echo [*] Seeding demo doctor account and sample clinical cases...
python -m app.utils.seed_data

echo.
echo ===================================================
echo [+] Backend server is starting on http://localhost:8000
echo [+] Interactive API Documentation: http://localhost:8000/docs
echo ===================================================
echo.
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
