# start_telegram.ps1 — Launch the Telegram bot in a new window
$env:PYTHONIOENCODING = "utf-8"
$ProjectDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectDir

Write-Host "Starting Hype Scout Telegram Bot..." -ForegroundColor Magenta
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$ProjectDir'; `$env:PYTHONIOENCODING='utf-8'; python -m notifier.telegram_bot" `
    -WindowStyle Normal
