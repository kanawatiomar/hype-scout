# start_all.ps1 — Launch all Hype Scout components
$ProjectDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "=== Hype Scout v2 — Starting All Components ===" -ForegroundColor Yellow

# Scanner (pump.fun poller)
Write-Host "[1/3] Starting Scanner..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$ProjectDir'; `$env:PYTHONIOENCODING='utf-8'; python scanner/poller.py" `
    -WindowStyle Normal
Start-Sleep -Seconds 2

# Poster daemon
Write-Host "[2/3] Starting Poster Daemon..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$ProjectDir'; `$env:PYTHONIOENCODING='utf-8'; python poster_daemon.py" `
    -WindowStyle Normal
Start-Sleep -Seconds 2

# Telegram bot (only if token is configured)
$envFile = Join-Path $ProjectDir ".env"
if (Test-Path $envFile) {
    $tgToken = (Get-Content $envFile | Where-Object { $_ -match "^TELEGRAM_BOT_TOKEN=" }) -replace "TELEGRAM_BOT_TOKEN=", ""
    if ($tgToken -and $tgToken -ne "YOUR_TELEGRAM_BOT_TOKEN_HERE") {
        Write-Host "[3/3] Starting Telegram Bot..." -ForegroundColor Magenta
        Start-Process powershell -ArgumentList "-NoExit", "-Command", `
            "cd '$ProjectDir'; `$env:PYTHONIOENCODING='utf-8'; python -m notifier.telegram_bot" `
            -WindowStyle Normal
    } else {
        Write-Host "[3/3] Skipping Telegram Bot (token not configured)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "All components launched! Check individual windows for logs." -ForegroundColor Yellow
Write-Host "Logs also available in: $ProjectDir\logs\" -ForegroundColor Gray
