# Script để dọn dẹp các link game bị đứt trong các file category

# Cấu hình encoding cho tiếng Việt
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Lấy danh sách tất cả các file trong thư mục category
$categoryFiles = Get-ChildItem -Path "category" -Filter "*.html"

foreach ($file in $categoryFiles) {
    Write-Host "`nĐang xử lý file: $($file.Name)" -ForegroundColor Yellow
    
    # Đọc nội dung file
    $content = Get-Content $file.FullName -Raw
    
    # Tìm tất cả các link game
    $gameLinks = [regex]::Matches($content, 'href="/game/([^"]+)"')
    $brokenLinks = @()
    
    foreach ($link in $gameLinks) {
        $gamePath = "game/" + $link.Groups[1].Value
        if (-not (Test-Path $gamePath)) {
            $brokenLinks += $link.Value
        }
    }
    
    if ($brokenLinks.Count -gt 0) {
        Write-Host "Tìm thấy $($brokenLinks.Count) link game bị đứt" -ForegroundColor Red
        
        foreach ($brokenLink in $brokenLinks) {
            # Tìm và xóa div chứa game bị đứt
            $pattern = "<div[^>]*class=`"col-sm-6 col-md-4 col-lg-2 game-item`"[^>]*>.*?$([regex]::Escape($brokenLink)).*?</div>"
            $content = [regex]::Replace($content, $pattern, "")
        }
        
        # Lưu lại nội dung đã cập nhật
        $content | Set-Content $file.FullName -Force
        Write-Host "Đã xóa các game bị đứt khỏi file" -ForegroundColor Green
    } else {
        Write-Host "Không tìm thấy link game bị đứt" -ForegroundColor Green
    }
}

Write-Host "`nHoàn tất dọn dẹp!" -ForegroundColor Green 