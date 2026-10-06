<#
.SYNOPSIS
    Registers a Windows Scheduled Task for Periodic Production Health Monitoring
.DESCRIPTION
    Creates an automated Scheduled Task named 'ClinicApp-Production-Watchdog'
    that executes monitor_health_telemetry.ps1 periodically (default: every 1 hour).
#>

[CmdletBinding()]
param(
    [int]$IntervalMinutes = 60,
    [string]$TaskName = "ClinicApp-Production-Watchdog",
    [switch]$Unregister
)

$ScriptPath = Join-Path $PSScriptRoot "monitor_health_telemetry.ps1"
$LogDir = Join-Path $PSScriptRoot "logs"
$LogFile = Join-Path $LogDir "production_watchdog.log"

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

if ($Unregister) {
    Write-Host "Unregistering scheduled task '$TaskName'..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Task unregistered successfully." -ForegroundColor Green
    return
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " ⏰ REGISTERING PRODUCTION WATCHDOG SCHEDULED TASK              " -ForegroundColor Cyan
Write-Host " Task Name:         $TaskName" -ForegroundColor DarkGray
Write-Host " Target Script:     $ScriptPath" -ForegroundColor DarkGray
Write-Host " Execution Log:     $LogFile" -ForegroundColor DarkGray
Write-Host " Interval:          Every $IntervalMinutes minutes" -ForegroundColor DarkGray
Write-Host "=================================================================" -ForegroundColor Cyan

# Action: launch powershell hidden and append to log
$ActionArg = "-NoProfile -NonInteractive -ExecutionPolicy Bypass -Command `"& '$ScriptPath' *>> '$LogFile'`""
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $ActionArg -WorkingDirectory $PSScriptRoot

# Trigger: repeat every $IntervalMinutes indefinitely
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes) -RepetitionDuration (New-TimeSpan -Days 3650)

# Settings: run on battery, wake if needed, stop if hung
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 15)

try {
    # Unregister existing if present
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

    # Register new task for current user
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "Periodic automated health probe for Smart Clinic production endpoints (Vercel & Azure)" | Out-Null
    Write-Host "✅ Scheduled Task '$TaskName' registered successfully!" -ForegroundColor Green
    Write-Host "The health probe will automatically execute every $IntervalMinutes minutes in the background." -ForegroundColor Green
    Write-Host "To view real-time logs: Get-Content '$LogFile' -Wait -Tail 20" -ForegroundColor DarkGray
} catch {
    Write-Host "❌ Failed to register scheduled task: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Ensure you run PowerShell as Administrator if user permissions restrict task creation." -ForegroundColor Yellow
}
