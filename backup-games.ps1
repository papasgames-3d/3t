# Script to create a complete backup of the game directory
# This creates a timestamped backup of all game files

# Display script start message
Write-Host "Starting to backup game directory..." -ForegroundColor Yellow

# Create a timestamp for backup folder
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "backup_$timestamp"

# Create the backup directory
Write-Host "Creating backup directory: $backupDir" -ForegroundColor Cyan
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

# Check if the game directory exists
if (-not (Test-Path -Path ".\game")) {
    Write-Error "Game directory not found. Make sure you run this script from the correct location."
    exit 1
}

# Count total files for progress tracking
$totalFiles = (Get-ChildItem -Path ".\game" -Recurse | Measure-Object).Count
Write-Host "Found $totalFiles files to backup." -ForegroundColor Green

# Confirm before proceeding
$confirmation = Read-Host "Do you want to proceed with backing up all $totalFiles files? (y/n)"
if ($confirmation -ne "y") {
    Write-Host "Backup cancelled by user." -ForegroundColor Yellow
    exit 0
}

# Get the current location
$currentPath = (Get-Location).Path
$gameDirPath = Join-Path -Path $currentPath -ChildPath "game"
$backupDirPath = Join-Path -Path $currentPath -ChildPath $backupDir

# Create the game directory in the backup
$gameBackupDir = Join-Path -Path $backupDirPath -ChildPath "game"
New-Item -ItemType Directory -Path $gameBackupDir -Force | Out-Null

# Copy the game directory to the backup with progress
$processed = 0
Get-ChildItem -Path $gameDirPath -Recurse | ForEach-Object {
    $processed++
    $sourceFile = $_.FullName
    
    # Creating the target path properly
    $relPath = $sourceFile.Substring($gameDirPath.Length)
    $targetPath = Join-Path -Path $gameBackupDir -ChildPath $relPath
    
    Write-Progress -Activity "Backing up files" -Status "File $processed of $totalFiles: $relPath" -PercentComplete (($processed / $totalFiles) * 100)
    
    if ($_.PSIsContainer) {
        # It's a directory, create it in the backup
        if (-not (Test-Path -Path $targetPath)) {
            New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
        }
    } else {
        # It's a file, copy it to the backup
        $targetDir = Split-Path -Path $targetPath -Parent
        if (-not (Test-Path -Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
        Copy-Item -Path $sourceFile -Destination $targetPath -Force
    }
}

# Display summary
Write-Host "`nBackup complete!" -ForegroundColor Green
Write-Host "Total files backed up: $processed" -ForegroundColor Cyan
Write-Host "Backup location: $backupDir" -ForegroundColor Green

Write-Host "`nTo restore from this backup, use: restore-backup.ps1 -backupDir $backupDir" -ForegroundColor Yellow 