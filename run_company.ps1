# Master runner for ClinicCorp AI Multi-Agent System

param (
    [switch]$Start,
    [switch]$Stop,
    [switch]$Dashboard,
    [int]$Port = 8088,
    [string]$FeatureId = "v3.2.0-telehealth-webrtc",
    [switch]$LiveTests
)

$ErrorActionPreference = "Stop"
$agentDir = "$PSScriptRoot\.agent-company"

if ($Stop) {
    Write-Host "[SYSTEM] Emergency Stop Activated. Halting all agent processes..." -ForegroundColor Red
    try {
        Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*state_graph.py*" -or $_.CommandLine -like "*server.py*" } | Stop-Process -Force
        Write-Host "[SYSTEM] All agent processes stopped." -ForegroundColor Yellow
    } catch {
        Write-Host "[SYSTEM] No active agent processes found." -ForegroundColor DarkGray
    }
    exit 0
}

if ($Dashboard) {
    Write-Host "[SYSTEM] Launching ClinicCorp AI Mission Control Dashboard..." -ForegroundColor Cyan
    Write-Host "Target: http://localhost:$Port" -ForegroundColor Green
    python "$agentDir\src\dashboard\server.py" $Port
    exit 0
}

if ($Start) {
    Write-Host "[SYSTEM] Booting up ClinicCorp AI Orchestrator..." -ForegroundColor Cyan
    Write-Host "================================================="
    Write-Host "Verifying environment requirements..."
    
    # 1. Verify Python
    try {
        $pythonVer = python --version
        Write-Host " [OK] Python detected: $pythonVer" -ForegroundColor Green
    } catch {
        Write-Host " [FAIL] Python 3.10+ is required but not found in PATH." -ForegroundColor Red
        exit 1
    }

    # 2. Verify .NET
    try {
        $dotnetVer = dotnet --version
        Write-Host " [OK] .NET SDK detected: $dotnetVer" -ForegroundColor Green
    } catch {
        Write-Host " [FAIL] .NET 9 SDK is required but not found." -ForegroundColor Red
        exit 1
    }
    
    # 3. Verify Node/npm
    try {
        $nodeVer = node --version
        Write-Host " [OK] Node.js detected: $nodeVer" -ForegroundColor Green
    } catch {
        Write-Host " [FAIL] Node.js is required but not found." -ForegroundColor Red
        exit 1
    }

    Write-Host "================================================="
    Write-Host "[CEO Agent] Initializing Sprint for Feature: $FeatureId" -ForegroundColor Magenta
    Write-Host "[SYSTEM] Transitioning control to Python State Machine..." -ForegroundColor DarkGray

    $stateScript = "$agentDir\src\orchestrator\state_graph.py"
    $pyArgs = @($stateScript, "--feature", $FeatureId)
    if ($LiveTests) {
        $pyArgs += "--live-tests"
    }

    python @pyArgs

    if ($LASTEXITCODE -eq 0) {
        Write-Host "================================================="
        Write-Host "[SUCCESS] Sprint Cycle for $FeatureId completed successfully." -ForegroundColor Green
    } else {
        Write-Host "================================================="
        Write-Host "[ERROR] Sprint Cycle encountered an error (Code: $LASTEXITCODE)." -ForegroundColor Red
        exit $LASTEXITCODE
    }
} else {
    Write-Host "Usage:"
    Write-Host "  .\run_company.ps1 -Start [-FeatureId <ID>] [-LiveTests]"
    Write-Host "  .\run_company.ps1 -Dashboard [-Port 8088]"
    Write-Host "  .\run_company.ps1 -Stop"
}
