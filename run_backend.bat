@echo off
title QuantumCare - Backend Server
echo ===================================================
echo   QuantumCare - Starting FastAPI Backend Server
echo   Hybrid Quantum-Classical Early Disease Detection
echo ===================================================
echo.

if defined LOCALAPPDATA (
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%ProgramFiles%\Python311;%ProgramFiles%\Python312;%PATH%"
)
cd /d "%~dp0backend"

if exist ".venv" goto RUN_APP

echo [*] Creating Python virtual environment...
python -m venv .venv
if errorlevel 1 goto VENV_ERROR

echo [*] Installing dependencies into virtual environment...
call .venv\Scripts\pip.exe install -r requirements.txt
if errorlevel 1 goto PIP_ERROR

:RUN_APP
echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo ===================================================
echo [+] Backend server starting on http://localhost:8000
echo [+] Interactive API Documentation: http://localhost:8000/docs
echo ===================================================
echo.
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
goto END

:VENV_ERROR
echo [!] Error: Python not found in PATH. Please install Python 3.10+ from python.org.
goto END

:PIP_ERROR
echo [!] Error: pip install failed. Please check requirements.txt.
goto END

:END
pause
