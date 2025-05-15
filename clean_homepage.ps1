# Script để dọn dẹp các game bị đứt trong trang chủ

# Cấu hình encoding cho tiếng Việt
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Đang dọn dẹp trang chủ..." -ForegroundColor Yellow

# Đọc nội dung file index.html
$content = Get-Content "index.html" -Raw

# Tìm tất cả các div game-item
$pattern = '<div class="col-sm-6 col-md-4 col-lg-2 game-item">.*?<a class="game-link" href="(.*?)".*?<h3 class="game-card__title">(.*?)</h3>.*?</div>'
$matches = [regex]::Matches($content, $pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)

Write-Host "`nTổng số game tìm thấy: $($matches.Count)" -ForegroundColor Cyan
$brokenGames = @()

foreach ($match in $matches) {
    $fullDiv = $match.Value
    $link = $match.Groups[1].Value
    $name = $match.Groups[2].Value.Trim()
    $path = "." + $link
    $path = $path -replace "/", "\"
    
    if (-not (Test-Path $path)) {
        $brokenGames += @{
            'name' = $name
            'link' = $link
            'div' = $fullDiv
        }
    }
}

if ($brokenGames.Count -gt 0) {
    Write-Host "`nTìm thấy $($brokenGames.Count) game bị đứt:" -ForegroundColor Red
    
    # Tạo backup trước khi sửa
    $backupPath = "index_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').html"
    $content | Set-Content $backupPath -Force -Encoding UTF8
    Write-Host "Đã tạo backup tại: $backupPath" -ForegroundColor Yellow
    
    foreach ($game in $brokenGames) {
        Write-Host "`nXóa game: $($game.name)" -ForegroundColor Yellow
        Write-Host "Link: $($game.link)" -ForegroundColor Yellow
        # Xóa div game bị đứt
        $content = $content.Replace($game.div, "")
    }
    
    # Lưu lại nội dung đã cập nhật
    $content | Set-Content "index.html" -Force -Encoding UTF8
    Write-Host "`nĐã xóa tất cả các game bị đứt khỏi trang chủ" -ForegroundColor Green
} else {
    Write-Host "`nKhông tìm thấy game bị đứt trong trang chủ" -ForegroundColor Green
}

Write-Host "`nHoàn tất dọn dẹp trang chủ!" -ForegroundColor Green 