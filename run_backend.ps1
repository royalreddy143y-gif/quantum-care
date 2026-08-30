# QuantumCare Backend Launcher (PowerShell)
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  QuantumCare - Starting FastAPI Backend Server" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot\backend"

$venvPython = "$PSScriptRoot\backend\.venv\Scripts\python.exe"
$venvPip = "$PSScriptRoot\backend\.venv\Scripts\pip.exe"
$venvUvicorn = "$PSScriptRoot\backend\.venv\Scripts\uvicorn.exe"

if (-not (Test-Path "$PSScriptRoot\backend\.venv")) {
    Write-Host "[*] Creating Python virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv "$PSScriptRoot\backend\.venv"
}

Write-Host "[*] Installing / Checking dependencies..." -ForegroundColor Yellow
& $venvPip install -r requirements.txt

Write-Host "[*] Seeding database with demo clinician & test cases..." -ForegroundColor Green
& $venvPython -m app.utils.seed_data

Write-Host "`n[+] Backend running at http://localhost:8000" -ForegroundColor Green
Write-Host "[+] Interactive Swagger Docs at http://localhost:8000/docs`n" -ForegroundColor Green
& $venvUvicorn app.main:app --reload --host 127.0.0.1 --port 8000
