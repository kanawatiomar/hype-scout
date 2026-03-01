# run_live_scanner.ps1 — Cron-compatible runner for live_scanner.py
# OpenClaw cron prompt: "Run: powershell -File run_live_scanner.ps1
# If output starts with LIVE| reply with everything after the pipe. Otherwise reply NO_REPLY."
$env:PYTHONIOENCODING = "utf-8"
$ProjectDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectDir
python tracker/live_scanner.py
