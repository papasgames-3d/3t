# Script de xoa cac game bi hong dua tren danh sach da tao

# Kiem tra xem file broken_games.txt co ton tai khong
if (-not (Test-Path "broken_games.txt")) {
    Write-Host "Khong tim thay file 'broken_games.txt'. Vui long chay script 'check_broken_games_fixed.ps1' truoc." -ForegroundColor Red
    exit
}

# Doc danh sach cac game bi hong
$brokenGames = Get-Content -Path "broken_games.txt"

if ($brokenGames.Count -eq 0) {
    Write-Host "Khong tim thay game nao bi hong." -ForegroundColor Green
    exit
}

Write-Host "Da tim thay $($brokenGames.Count) game co the bi hong." -ForegroundColor Yellow

# Tao thu muc backup neu chua ton tai
$backupFolder = ".\backup_broken_games"
if (-not (Test-Path $backupFolder)) {
    New-Item -Path $backupFolder -ItemType Directory | Out-Null
    Write-Host "Da tao thu muc backup: $backupFolder" -ForegroundColor Green
}

# Hien thi danh sach va yeu cau xac nhan
Write-Host "Danh sach game se bi xoa:" -ForegroundColor Yellow
$brokenGames | ForEach-Object { Write-Host " - $($_ -replace '.*\\', '')" }

$confirmation = Read-Host "Ban co chac chan muon xoa cac game nay khong? (Y/N)"

if ($confirmation -ne 'Y') {
    Write-Host "Huy bo thao tac xoa." -ForegroundColor Red
    exit
}

# Xoa hoac di chuyen cac file game bi hong
$removedCount = 0
foreach ($game in $brokenGames) {
    if (Test-Path $game) {
        $filename = $game -replace '.*\\', ''
        
        # Sao luu file vao thu muc backup
        Copy-Item -Path $game -Destination "$backupFolder\$filename"
        
        # Xoa file goc
        Remove-Item -Path $game
        
        Write-Host "Da xoa va sao luu: $filename" -ForegroundColor Green
        $removedCount++
    }
    else {
        Write-Host "Khong tim thay file: $game" -ForegroundColor Red
    }
}

Write-Host "Da xoa $removedCount/$($brokenGames.Count) game." -ForegroundColor Green
Write-Host "Sao luu da duoc luu trong thu muc: $backupFolder" -ForegroundColor Green 