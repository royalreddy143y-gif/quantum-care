@echo off
title QuantumCare - Automated Test Suite
echo ===================================================
echo   QuantumCare - Running Automated Pytest Suite
echo   (Auth, Patients, Swin Transformer, PennyLane VQC)
echo ===================================================
echo.

cd /d "%~dp0backend"

if not exist ".venv" (
    echo [!] Virtual environment not found. Please run run_backend.bat first to set up the environment.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
pytest tests/ -v

echo.
echo ===================================================
echo Tests finished.
echo ===================================================
pause
