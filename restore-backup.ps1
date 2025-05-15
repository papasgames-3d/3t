# Script to restore from a backup
# This script allows restoring the game directory from a previously created backup

param (
    [string]$backupDir = ""
)

# Display script header
Write-Host "Game Directory Restoration Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# If no backup directory was specified, show available backups and prompt for selection
if ([string]::IsNullOrEmpty($backupDir)) {
    Write-Host "No backup directory specified. Looking for available backups..." -ForegroundColor Yellow
    
    # Look for backup directories
    $backupDirs = Get-ChildItem -Path "." -Directory -Filter "backup_*" | Sort-Object -Property Name -Descending
    
    if ($backupDirs.Count -eq 0) {
        Write-Error "No backup directories found. Make sure you're running this script from the correct location."
        exit 1
    }
    
    Write-Host "Available backups:" -ForegroundColor Green
    for ($i = 0; $i -lt $backupDirs.Count; $i++) {
        Write-Host "[$($i+1)] $($backupDirs[$i].Name)"
    }
    
    $selection = Read-Host "Enter the number of the backup you want to restore from (or 'q' to quit)"
    if ($selection -eq 'q') {
        Write-Host "Restoration cancelled by user." -ForegroundColor Yellow
        exit 0
    }
    
    $index = [int]$selection - 1
    if ($index -lt 0 -or $index -ge $backupDirs.Count) {
        Write-Error "Invalid selection. Please run the script again and select a valid backup."
        exit 1
    }
    
    $backupDir = $backupDirs[$index].Name
}

# Verify the backup directory exists and contains a game directory
if (-not (Test-Path -Path $backupDir)) {
    Write-Error "Backup directory '$backupDir' does not exist."
    exit 1
}

if (-not (Test-Path -Path "$backupDir\game")) {
    Write-Error "Backup directory '$backupDir' does not contain a 'game' directory."
    exit 1
}

# Confirm before proceeding
Write-Host "About to restore from backup: $backupDir" -ForegroundColor Yellow
Write-Host "WARNING: This will overwrite the current game directory contents." -ForegroundColor Red
$confirmation = Read-Host "Do you want to proceed? (y/n)"

if ($confirmation -ne "y") {
    Write-Host "Restoration cancelled by user." -ForegroundColor Yellow
    exit 0
}

# Check if the game directory exists, create it if it doesn't
if (-not (Test-Path -Path ".\game")) {
    Write-Host "Game directory does not exist. Creating it..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path ".\game" -Force | Out-Null
}

# Count files for progress tracking
$totalFiles = (Get-ChildItem -Path "$backupDir\game" -Recurse | Where-Object { -not $_.PSIsContainer } | Measure-Object).Count
Write-Host "Found $totalFiles files to restore." -ForegroundColor Green

# Copy files from backup to the game directory
$processed = 0
Get-ChildItem -Path "$backupDir\game" -Recurse | Where-Object { -not $_.PSIsContainer } | ForEach-Object {
    $processed++
    $backupFile = $_.FullName
    $relativePath = $backupFile.Substring("$backupDir\game".Length)
    $targetFile = ".\game$relativePath"
    
    Write-Progress -Activity "Restoring files" -Status "File $processed of $totalFiles: $relativePath" -PercentComplete (($processed / $totalFiles) * 100)
    
    # Create target directory if it doesn't exist
    $targetDir = Split-Path -Path $targetFile -Parent
    if (-not (Test-Path -Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
    
    # Copy file
    Copy-Item -Path $backupFile -Destination $targetFile -Force
}

# Display summary
Write-Host "`nRestoration complete!" -ForegroundColor Green
Write-Host "Total files restored: $processed" -ForegroundColor Cyan
Write-Host "Game directory has been restored from backup: $backupDir" -ForegroundColor Green 