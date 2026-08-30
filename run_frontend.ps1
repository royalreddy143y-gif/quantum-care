# QuantumCare Frontend Launcher (PowerShell)
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  QuantumCare - Starting React + Vite Frontend" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot\frontend"

if (-not (Test-Path "node_modules")) {
    Write-Host "[*] Installing dependencies (npm install)..." -ForegroundColor Yellow
    npm.cmd install
}

Write-Host "`n[+] Starting Vite dev server at http://localhost:5173`n" -ForegroundColor Green
npm.cmd run dev
