# Script để xóa các game bị hỏng dựa trên danh sách đã tạo

# Kiểm tra xem file broken_games.txt có tồn tại không
if (-not (Test-Path "broken_games.txt")) {
    Write-Host "Không tìm thấy file 'broken_games.txt'. Vui lòng chạy script 'check_broken_games.ps1' trước." -ForegroundColor Red
    exit
}

# Đọc danh sách các game bị hỏng
$brokenGames = Get-Content -Path "broken_games.txt"

if ($brokenGames.Count -eq 0) {
    Write-Host "Không tìm thấy game nào bị hỏng." -ForegroundColor Green
    exit
}

Write-Host "Đã tìm thấy $($brokenGames.Count) game có thể bị hỏng." -ForegroundColor Yellow

# Tạo thư mục backup nếu chưa tồn tại
$backupFolder = ".\backup_broken_games"
if (-not (Test-Path $backupFolder)) {
    New-Item -Path $backupFolder -ItemType Directory | Out-Null
    Write-Host "Đã tạo thư mục backup: $backupFolder" -ForegroundColor Green
}

# Hiển thị danh sách và yêu cầu xác nhận
Write-Host "Danh sách game sẽ bị xóa:" -ForegroundColor Yellow
$brokenGames | ForEach-Object { Write-Host " - $($_ -replace '.*\\', '')" }

$confirmation = Read-Host "Bạn có chắc chắn muốn xóa các game này không? (Y/N)"

if ($confirmation -ne 'Y') {
    Write-Host "Hủy bỏ thao tác xóa." -ForegroundColor Red
    exit
}

# Xóa hoặc di chuyển các file game bị hỏng
$removedCount = 0
foreach ($game in $brokenGames) {
    if (Test-Path $game) {
        $filename = $game -replace '.*\\', ''
        
        # Sao lưu file vào thư mục backup
        Copy-Item -Path $game -Destination "$backupFolder\$filename"
        
        # Xóa file gốc
        Remove-Item -Path $game
        
        Write-Host "Đã xóa và sao lưu: $filename" -ForegroundColor Green
        $removedCount++
    }
    else {
        Write-Host "Không tìm thấy file: $game" -ForegroundColor Red
    }
}

Write-Host "Đã xóa $removedCount/$($brokenGames.Count) game." -ForegroundColor Green
Write-Host "Sao lưu đã được lưu trong thư mục: $backupFolder" -ForegroundColor Green 