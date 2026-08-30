@echo off
title QuantumCare - Master Launcher
echo =======================================================
echo   QuantumCare Platform - Master One-Click Launcher
echo   Hybrid Classical-Quantum Early Disease Detection
echo =======================================================
echo.
echo [*] Starting Backend Server in a new window...
start "QuantumCare Backend" cmd /k "%~dp0run_backend.bat"

echo [*] Waiting 3 seconds for backend initialization...
timeout /t 3 /nobreak >nul

echo [*] Starting Frontend App in a new window...
start "QuantumCare Frontend" cmd /k "%~dp0run_frontend.bat"

echo.
echo =======================================================
echo [+] Both services launched!
echo [+] Frontend URL:  http://localhost:5173
echo [+] Backend API:   http://localhost:8000/docs
echo =======================================================
echo.
echo [*] Opening browser to http://localhost:5173 ...
start http://localhost:5173

pause
