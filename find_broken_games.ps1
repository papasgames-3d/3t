# Script để tìm các game bị đứt

# Cấu hình encoding cho tiếng Việt
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Đang tìm các game bị đứt..." -ForegroundColor Yellow

# Đọc nội dung file index.html
$content = Get-Content "index.html" -Raw

# Tìm tất cả các div game-item
$pattern = '<div class="col-sm-6 col-md-4 col-lg-2 game-item">.*?<a class="game-link" href="(.*?)".*?<h3 class="game-card__title">(.*?)</h3>'
$matches = [regex]::Matches($content, $pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)

Write-Host "`nTổng số game tìm thấy: $($matches.Count)" -ForegroundColor Cyan

foreach ($match in $matches) {
    $link = $match.Groups[1].Value
    $name = $match.Groups[2].Value.Trim()
    $path = "." + $link
    $path = $path -replace "/", "\"
    
    if (-not (Test-Path $path)) {
        Write-Host "`nPhát hiện game bị đứt!" -ForegroundColor Red
        Write-Host "Tên game: $name" -ForegroundColor Red
        Write-Host "Path: $path" -ForegroundColor Red
        Write-Host "Link: $link" -ForegroundColor Red
    }
} 