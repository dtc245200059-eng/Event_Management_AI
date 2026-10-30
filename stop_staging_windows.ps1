<#
.SYNOPSIS
    Stops the native Windows Staging server for EventAI Pro (Hardened).
.DESCRIPTION
    Safely terminates ONLY the process belonging to EventAI Pro Staging.
    Verifies process identity via command line and binary path.
    Prevents terminating unrelated Python processes or recycled PIDs.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"
$PidFile = Join-Path $ScriptDir "instance_staging\staging_server.pid"
$stopped = $false

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

# 1. Check PID file
if (Test-Path $PidFile) {
    $procId = Get-Content $PidFile -ErrorAction SilentlyContinue
    if ($procId -match '^\d+$') {
        $targetPid = [int]$procId
        if (Test-EventAIProcess $targetPid) {
            Write-Host "Stopping verified EventAI Pro Staging process (PID: $targetPid)..." -ForegroundColor Yellow
            Stop-Process -Id $targetPid -Force -ErrorAction SilentlyContinue
            $stopped = $true
        } else {
            Write-Host "[INFO] Stale PID file detected (PID $targetPid is not EventAI Pro). Cleaning up." -ForegroundColor Gray
        }
    }
    Remove-Item -Path $PidFile -Force -ErrorAction SilentlyContinue
}

# 2. Check any remaining listener on port 5001
$conns = Get-NetTCPConnection -LocalPort 5001 -State Listen -ErrorAction SilentlyContinue
if ($conns) {
    foreach ($conn in $conns) {
        $pidToKill = $conn.OwningProcess
        if (Test-EventAIProcess $pidToKill) {
            Write-Host "Stopping verified listener on port 5001 (PID: $pidToKill)..." -ForegroundColor Yellow
            Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
            $stopped = $true
        } else {
            Write-Host "[WARNING] Port 5001 is held by unrelated process (PID: $pidToKill). Skipping." -ForegroundColor Red
        }
    }
}

if ($stopped) {
    Write-Host "[SUCCESS] EventAI Pro Staging server has been stopped safely." -ForegroundColor Green
} else {
    Write-Host "[INFO] No active EventAI Pro staging server found on port 5001." -ForegroundColor Gray
}
