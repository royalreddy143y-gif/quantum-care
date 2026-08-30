@echo off
title QuantumCare - Master Launcher
echo =======================================================
echo   QuantumCare Platform - Master One-Click Launcher
echo   Hybrid Classical-Quantum Early Disease Detection
echo =======================================================
echo.

echo [*] Starting Backend Server in a new window...
start "QuantumCare Backend" cmd /k "%~dp0run_backend.bat"

echo [*] Starting Frontend Server in a new window...
start "QuantumCare Frontend" cmd /k "%~dp0run_frontend.bat"

echo.
echo [*] Waiting for Frontend and Backend to initialize...
:: Cross-compatible wait using ping (avoids timeout input redirection errors in PowerShell)
ping -n 6 127.0.0.1 >nul

echo.
echo =======================================================
echo [+] Both services launched!
echo [+] Frontend URL:  http://localhost:5173
echo [+] Backend API:   http://localhost:8000/docs
echo =======================================================
echo.
echo [*] Opening browser to http://localhost:5173 ...
start http://localhost:5173

echo.
echo Note: Keep the spawned Backend and Frontend windows open while using the app.
echo.
pause
