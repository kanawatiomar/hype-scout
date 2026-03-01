# run_runner_digest.ps1 — Cron-compatible runner for runner_digest.py
# OpenClaw cron prompt: "Run: powershell -File run_runner_digest.ps1
# If output starts with DIGEST| reply with everything after the pipe. Otherwise reply NO_REPLY."
$env:PYTHONIOENCODING = "utf-8"
$ProjectDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectDir
python tracker/runner_digest.py
