# Automated Desktop Application Generator for Smart Clinic Management System
param (
    [switch]$Clean,
    [switch]$Run,
    [switch]$Installer,
    [string]$OutputDir
)

$ErrorActionPreference = "Stop"
$sw = [System.Diagnostics.Stopwatch]::StartNew()

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Smart Clinic Management System - Automated Desktop Generator" -ForegroundColor Cyan
Write-Host "Version: 8.0.0 Enterprise Desktop Edition (Electron 34 / Angular 20)" -ForegroundColor DarkCyan
Write-Host "=====================================================================" -ForegroundColor Cyan

$root = $PSScriptRoot
$clinicAppDir = Join-Path $root "clinic-app"

if (-not (Test-Path $clinicAppDir)) {
    Write-Error "clinic-app directory not found at: $clinicAppDir"
    exit 1
}

# 1. Environment Verification
Write-Host "[1/5] Verifying environment prerequisites..." -ForegroundColor Yellow
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) {
    Write-Error "Node.js is required but not found in PATH."
    exit 1
}
$nodeVersion = & node -v
Write-Host "  OK - Node.js: $nodeVersion" -ForegroundColor Green

$npmCmd = Get-Command npm -ErrorAction SilentlyContinue
if (-not $npmCmd) {
    Write-Error "npm is required but not found in PATH."
    exit 1
}
$npmVersion = & npm -v
Write-Host "  OK - npm: $npmVersion" -ForegroundColor Green

# 2. Cleanup (if requested)
if ($Clean) {
    Write-Host "[2/5] Cleaning existing build artifacts..." -ForegroundColor Yellow
    $distDir = Join-Path $clinicAppDir "dist"
    $distElectronDir = Join-Path $clinicAppDir "dist-electron"
    $desktopDistDir = Join-Path $clinicAppDir "desktop\dist"

    if (Test-Path $distDir) {
        Remove-Item -Recurse -Force $distDir
        Write-Host "  Cleaned: $distDir" -ForegroundColor DarkGray
    }
    if (Test-Path $distElectronDir) {
        Remove-Item -Recurse -Force $distElectronDir
        Write-Host "  Cleaned: $distElectronDir" -ForegroundColor DarkGray
    }
    if (Test-Path $desktopDistDir) {
        Remove-Item -Recurse -Force $desktopDistDir
        Write-Host "  Cleaned: $desktopDistDir" -ForegroundColor DarkGray
    }
} else {
    Write-Host "[2/5] Preserving existing build caches..." -ForegroundColor DarkGray
}

# 3. Angular Web Bundle Compilation
Write-Host "[3/5] Building Angular 20 Standalone production bundle..." -ForegroundColor Yellow
Push-Location $clinicAppDir
try {
    npm run build
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Angular build failed with exit code $LASTEXITCODE"
        exit $LASTEXITCODE
    }
    Write-Host "  OK - Angular web bundle assembled in dist/clinic-app/browser" -ForegroundColor Green
} finally {
    Pop-Location
}

# 4. Desktop TypeScript Compilation
Write-Host "[4/5] Compiling Electron main and preload TypeScript..." -ForegroundColor Yellow
Push-Location $clinicAppDir
try {
    npm run desktop:compile
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Desktop TypeScript compilation failed with exit code $LASTEXITCODE"
        exit $LASTEXITCODE
    }
    Write-Host "  OK - Desktop main and preload compiled in desktop/dist/" -ForegroundColor Green
} finally {
    Pop-Location
}

# 5. Native Binary Assembly (electron-builder)
Write-Host "[5/5] Packaging native desktop application..." -ForegroundColor Yellow
Push-Location $clinicAppDir
try {
    if ($Installer) {
        Write-Host "  Packaging complete installer binaries..." -ForegroundColor DarkCyan
        npx electron-builder
    } else {
        Write-Host "  Packaging standalone unpacked application..." -ForegroundColor DarkCyan
        npx electron-builder --dir
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Error "electron-builder packaging failed with exit code $LASTEXITCODE"
        exit $LASTEXITCODE
    }
    Write-Host "  OK - Native application packaged successfully" -ForegroundColor Green
} finally {
    Pop-Location
}

# 6. Verification and Integrity Check
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Post-Build Verification and Artifact Audit" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

$unpackedDir = Join-Path $clinicAppDir "dist-electron\win-unpacked"
$exePath = Join-Path $unpackedDir "Smart Clinic.exe"
$asarPath = Join-Path $unpackedDir "resources\app.asar"

if (Test-Path $exePath) {
    $exeItem = Get-Item $exePath
    $exeSizeMB = [math]::Round($exeItem.Length / 1MB, 2)
    Write-Host "  OK - Executable binary: $exePath" -ForegroundColor Green
    Write-Host "       Size: $exeSizeMB MB" -ForegroundColor White
} else {
    Write-Error "Verification failed: Smart Clinic.exe not found at $exePath"
    exit 1
}

if (Test-Path $asarPath) {
    $asarItem = Get-Item $asarPath
    $asarSizeMB = [math]::Round($asarItem.Length / 1MB, 2)
    Write-Host "  OK - Application ASAR archive: $asarPath" -ForegroundColor Green
    Write-Host "       Size: $asarSizeMB MB (includes Angular core and desktop bridge)" -ForegroundColor White
} else {
    Write-Error "Verification failed: app.asar not found at $asarPath"
    exit 1
}

if ($OutputDir) {
    Write-Host "Copying packaged application to: $OutputDir" -ForegroundColor Yellow
    if (-not (Test-Path $OutputDir)) {
        New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    }
    Copy-Item -Path (Join-Path $unpackedDir "*") -Destination $OutputDir -Recurse -Force
    Write-Host "  OK - Copied to destination: $OutputDir" -ForegroundColor Green
}

$sw.Stop()
$elapsedSec = [math]::Round($sw.Elapsed.TotalSeconds, 1)
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "SUCCESS: Desktop Application generated in $elapsedSec seconds!" -ForegroundColor Green
Write-Host "Artifact: $exePath" -ForegroundColor White
Write-Host "=====================================================================" -ForegroundColor Green

if ($Run) {
    Write-Host "Launching Smart Clinic Desktop Application..." -ForegroundColor Cyan
    Start-Process -FilePath $exePath
    Write-Host "Application launched." -ForegroundColor Green
}
