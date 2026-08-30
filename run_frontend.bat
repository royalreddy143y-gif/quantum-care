@echo off
title QuantumCare - Frontend Server
echo ===================================================
echo   QuantumCare - Starting React + Vite Frontend
echo ===================================================
echo.

if defined ProgramFiles (
    set "PATH=%ProgramFiles%\nodejs;%ProgramFiles(x86)%\nodejs;%LOCALAPPDATA%\Programs\nodejs;%PATH%"
)
cd /d "%~dp0frontend"

if exist "node_modules" goto RUN_APP

echo [*] Installing Node.js dependencies...
call npm install
if errorlevel 1 goto INSTALL_ERROR

:RUN_APP
echo.
echo ===================================================
echo [+] Frontend web application starting on http://localhost:5173
echo ===================================================
echo.
call npm run dev
goto END

:INSTALL_ERROR
echo [!] Error: npm install failed. Please ensure Node.js is installed.

:END
pause
