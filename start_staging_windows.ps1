<#
.SYNOPSIS
    Starts the native Windows Staging server for EventAI Pro (Hardened).
.DESCRIPTION
    Runs run_staging_windows.py inside the dedicated virtual environment (.venv) on http://127.0.0.1:5001.
    Logs output to instance_staging\staging.log and saves PID to instance_staging\staging_server.pid.
    Suitable strictly for local QA and academic demonstration; not for public production hosting.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Error "Virtual environment Python not found at: $PythonExe"
    exit 1
}

# Function to check whether a PID belongs to EventAI Pro Staging
function Test-EventAIProcess($pidToCheck) {
    try {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $pidToCheck" -ErrorAction SilentlyContinue
        if ($proc -and ($proc.CommandLine -match "run_staging_windows" -or $proc.ExecutablePath -match [regex]::Escape($PythonExe))) {
            return $true
        }
    } catch {}
    return $false
}

# Check if port 5001 is already in use
$existing = Get-NetTCPConnection -LocalPort 5001 -State Listen -ErrorAction SilentlyContinue
if ($existing) {
    $owningPid = $existing.OwningProcess
    if (Test-EventAIProcess $owningPid) {
        Write-Host "[WARNING] Port 5001 is already in use by EventAI Pro Staging (PID $owningPid)." -ForegroundColor Yellow
        Write-Host "Please run .\stop_staging_windows.ps1 before restarting." -ForegroundColor Yellow
    } else {
        Write-Host "[ERROR] Port 5001 is in use by an external process (PID $owningPid). Cannot start staging." -ForegroundColor Red
    }
    exit 1
}

# Ensure instance_staging directory exists
$StagingDir = Join-Path $ScriptDir "instance_staging"
if (-not (Test-Path $StagingDir)) {
    New-Item -ItemType Directory -Path $StagingDir -Force | Out-Null
}

$PidFile = Join-Path $StagingDir "staging_server.pid"
$LogFile = Join-Path $StagingDir "staging.log"
$ErrLogFile = Join-Path $StagingDir "staging_err.log"

# Clean up stale PID file if process is no longer running
if (Test-Path $PidFile) {
    $oldPid = Get-Content $PidFile -ErrorAction SilentlyContinue
    if (-not (Test-EventAIProcess $oldPid)) {
        Remove-Item -Path $PidFile -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting EventAI Pro Windows Native Staging Server... " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  * Host:              127.0.0.1 (Strict Local Loopback)" -ForegroundColor Gray
Write-Host "  * Port:              5001" -ForegroundColor Gray
Write-Host "  * Target Database:   instance_staging\staging.db" -ForegroundColor Gray
Write-Host "  * Production DB:     instance\event_management.db (Untouched)" -ForegroundColor Gray
Write-Host "  * Notice:            Werkzeug Development Server (QA Only)" -ForegroundColor Yellow
Write-Host "----------------------------------------------------------" -ForegroundColor Gray

$process = Start-Process -FilePath $PythonExe `
    -ArgumentList "run_staging_windows.py" `
    -WorkingDirectory $ScriptDir `
    -RedirectStandardOutput $LogFile `
    -RedirectStandardError $ErrLogFile `
    -PassThru

Set-Content -Path $PidFile -Value $process.Id
Write-Host "[OK] Server process started with PID: $($process.Id)" -ForegroundColor Green

# Wait up to 10 seconds for server to become responsive
Write-Host "Waiting for server to become ready on http://127.0.0.1:5001..." -NoNewline
$ready = $false
for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep -Milliseconds 500
    Write-Host "." -NoNewline
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:5001/" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $ready = $true
            break
        }
    } catch {
        # Continue waiting
    }
}
Write-Host ""

if ($ready) {
    Write-Host "[SUCCESS] EventAI Pro Staging is ACTIVE and reachable at http://127.0.0.1:5001" -ForegroundColor Green
    Write-Host "  * Log File:          instance_staging\staging.log" -ForegroundColor Gray
    Write-Host "  * Local Credentials: Run '.\\.venv\\Scripts\\python.exe scripts\\get_staging_credentials.py'" -ForegroundColor Cyan
    Write-Host "  * Stop Command:      .\\stop_staging_windows.ps1" -ForegroundColor Cyan
} else {
    Write-Host "[WARNING] Server started (PID $($process.Id)) but http://127.0.0.1:5001 did not respond with 200 within 10s." -ForegroundColor Yellow
    Write-Host "Check instance_staging\staging.log for error details." -ForegroundColor Yellow
}
