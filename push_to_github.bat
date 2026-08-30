@echo off
title QuantumCare - Push to GitHub
echo =======================================================
echo   QuantumCare - Push to GitHub Repository
echo   Remote: https://github.com/royalreddy143y-gif/quantum-care
echo =======================================================
echo.

set "PATH=C:\Users\HP\AppData\Local\Programs\Git\cmd;C:\Program Files\Git\cmd;%PATH%"

cd /d "%~dp0"

echo [*] Verifying Git...
git --version
if errorlevel 1 (
    echo [!] Git is not found in PATH.
    pause
    exit /b 1
)

echo.
echo [*] Checking git remote...
git remote -v

echo.
echo [*] Pushing branch 'main' to origin...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [+] Successfully pushed to https://github.com/royalreddy143y-gif/quantum-care !
) else (
    echo.
    echo [!] Push encountered an issue.
)

echo.
pause
