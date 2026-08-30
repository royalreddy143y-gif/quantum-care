# QuantumCare Platform - Master One-Click Launcher (PowerShell)
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "  QuantumCare Platform - Master One-Click Launcher" -ForegroundColor Cyan
Write-Host "  Hybrid Classical-Quantum Early Disease Detection" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

$root = $PSScriptRoot

Write-Host "[*] Starting FastAPI Backend Server in a new window..." -ForegroundColor Yellow
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-File", "$root\run_backend.ps1"

Write-Host "[*] Starting React + Vite Frontend in a new window..." -ForegroundColor Yellow
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-File", "$root\run_frontend.ps1"

Write-Host ""
Write-Host "[*] Waiting for services to initialize..." -ForegroundColor Yellow

$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    try {
        $res = Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing -TimeoutSec 1 -ErrorAction SilentlyContinue
        if ($res -and $res.StatusCode -eq 200) {
            $ready = $true
            break
        }
    } catch {}
}

Write-Host ""
Write-Host "=======================================================" -ForegroundColor Green
Write-Host "[+] All services are up and running!" -ForegroundColor Green
Write-Host "[+] Frontend URL:  http://localhost:5173" -ForegroundColor Green
Write-Host "[+] Backend API:   http://localhost:8000/docs" -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Green
Write-Host ""
Write-Host "[*] Opening browser to http://localhost:5173 ..." -ForegroundColor Cyan
Start-Process "http://localhost:5173"

Write-Host "`nPress Enter to exit this launcher window (servers will continue running)..."
Read-Host
