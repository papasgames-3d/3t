# Script để kiểm tra các link game bị đứt trong các file category

# Cấu hình encoding cho tiếng Việt
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Lấy danh sách tất cả các file trong thư mục category
$categoryFiles = Get-ChildItem -Path "category" -Filter "*.html"

foreach ($file in $categoryFiles) {
    Write-Host "`nĐang kiểm tra file: $($file.Name)" -ForegroundColor Yellow
    
    # Đọc nội dung file
    $content = Get-Content $file.FullName -Raw
    
    # Tìm tất cả các link game
    $gameLinks = [regex]::Matches($content, 'href="/game/([^"]+)"')
    
    foreach ($link in $gameLinks) {
        $gamePath = "game/" + $link.Groups[1].Value
        if (-not (Test-Path $gamePath)) {
            Write-Host "Link game bị đứt: $gamePath" -ForegroundColor Red
            
            # Xóa div chứa game bị đứt
            $gameDiv = [regex]::Match($content, "<div[^>]*>.*?$([regex]::Escape($link.Value)).*?</div>").Value
            if ($gameDiv) {
                $content = $content.Replace($gameDiv, "")
                Write-Host "Đã xóa game bị đứt khỏi category" -ForegroundColor Green
            }
        }
    }
    
    # Lưu lại nội dung đã cập nhật
    $content | Set-Content $file.FullName -Force
}

Write-Host "`nHoàn tất kiểm tra!" -ForegroundColor Green 