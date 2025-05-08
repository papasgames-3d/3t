# Script to restore from individual .backup files

Write-Host "Checking for .backup files..." -ForegroundColor Yellow
$backupFiles = Get-ChildItem -Path ".\game" -Filter "*.backup" -Recurse

if ($backupFiles.Count -eq 0) {
    Write-Error "No .backup files found in the game directory."
    exit 1
}

Write-Host "Found $($backupFiles.Count) .backup files." -ForegroundColor Green

$answer = Read-Host "Are you sure you want to restore from these .backup files? This will overwrite the current files (y/n)"
if ($answer -ne "y") {
    Write-Host "Restoration cancelled." -ForegroundColor Yellow
    exit 0
}

$totalFiles = $backupFiles.Count
$processed = 0

foreach ($backupFile in $backupFiles) {
    $processed++
    $originalFile = $backupFile.FullName -replace "\.backup$", ""
    
    Write-Progress -Activity "Restoring files" -Status "File: $($backupFile.Name)" -PercentComplete (($processed / $totalFiles) * 100)
    
    # Restore the file
    Copy-Item -Path $backupFile.FullName -Destination $originalFile -Force
    
    Write-Host "[$processed/$totalFiles] Restored: $originalFile" -ForegroundColor Green
}

Write-Host "Restoration from .backup files complete!" -ForegroundColor Green 