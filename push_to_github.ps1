# Refresh PATH in current PowerShell session
$env:Path = "$env:LOCALAPPDATA\Programs\Git\cmd;$env:Path"

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "  QuantumCare - Pushing to GitHub" -ForegroundColor Cyan
Write-Host "  Remote: https://github.com/royalreddy143y-gif/quantum-care" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot"

Write-Host "`n[*] Git Version:" -ForegroundColor Yellow
git --version

Write-Host "`n[*] Pushing to origin main..." -ForegroundColor Yellow
git push -u origin main
