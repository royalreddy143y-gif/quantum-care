@echo off
title QuantumCare - Push to GitHub
echo =======================================================
echo   QuantumCare - Push to GitHub Repository
echo   Remote: https://github.com/royalreddy143y-gif/quantum-care
echo =======================================================
echo.

if defined LOCALAPPDATA (
    set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%ProgramFiles%\Git\cmd;%ProgramFiles(x86)%\Git\cmd;%PATH%"
)
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

if errorlevel 1 (
    echo.
    echo [!] Push failed or authentication was cancelled.
    echo [*] If the remote repository already has commits (like a README), try:
    echo     git push -u origin main --force
) else (
    echo.
    echo [+] Successfully pushed to https://github.com/royalreddy143y-gif/quantum-care !
)

echo.
pause
