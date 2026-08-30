@echo off
title QuantumCare - Frontend Server
echo ===================================================
echo   QuantumCare - Starting React + Vite Frontend
echo ===================================================
echo.

set PATH=C:\Program Files\nodejs;%PATH%
cd /d "%~dp0frontend"

:: Check if node_modules exists
if not exist "node_modules" (
    echo [*] Installing Node.js dependencies (npm install)...
    call npm.cmd install
    if errorlevel 1 (
        echo [!] Error: npm install failed. Please ensure Node.js is installed.
        pause
        exit /b 1
    )
)

echo.
echo ===================================================
echo [+] Frontend web application starting on http://localhost:5173
echo ===================================================
echo.
call npm.cmd run dev

pause
