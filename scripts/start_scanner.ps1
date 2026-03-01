# start_scanner.ps1 — Launch the Pump.fun poller in a new window
$env:PYTHONIOENCODING = "utf-8"
$ProjectDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectDir

Write-Host "Starting Hype Scout Scanner..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$ProjectDir'; `$env:PYTHONIOENCODING='utf-8'; python scanner/poller.py" `
    -WindowStyle Normal
