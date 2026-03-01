# run_leaderboard.ps1 — Cron-compatible runner for leaderboard.py
# OpenClaw cron prompt: "Run: powershell -File run_leaderboard.ps1
# If output starts with LEADERBOARD| reply with everything after the pipe. Otherwise reply NO_REPLY."
$env:PYTHONIOENCODING = "utf-8"
$ProjectDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectDir
python tracker/leaderboard.py
