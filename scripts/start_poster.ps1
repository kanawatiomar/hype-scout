# start_poster.ps1 — Launch the poster daemon in a new window
$env:PYTHONIOENCODING = "utf-8"
$ProjectDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectDir

Write-Host "Starting Hype Scout Poster Daemon..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$ProjectDir'; `$env:PYTHONIOENCODING='utf-8'; python poster_daemon.py" `
    -WindowStyle Normal
