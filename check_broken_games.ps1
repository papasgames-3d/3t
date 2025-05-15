# Script để tìm và hiển thị các iframe URLs trong các file game
$gameDir = ".\game"
$outputFile = "iframe_urls.txt"
$brokenGamesFile = "broken_games.txt"

# Danh sách các domain có thể đã bị hỏng
$potentiallyBrokenDomains = @(
    "classroom6x.gitlab.io",
    "games66ez.gitlab.io"
    # Thêm các domain khác nếu cần
)

# Xóa file output nếu đã tồn tại
if (Test-Path $outputFile) {
    Remove-Item $outputFile
}

if (Test-Path $brokenGamesFile) {
    Remove-Item $brokenGamesFile
}

# Tìm tất cả các file HTML trong thư mục game
$htmlFiles = Get-ChildItem -Path $gameDir -Filter "*.html"

# Thông báo số lượng file sẽ được kiểm tra
Write-Host "Tìm thấy $($htmlFiles.Count) file HTML để kiểm tra."

$brokenGameCount = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Sử dụng regex để tìm tất cả iframe URLs
    $pattern = '<iframe[^>]* src="([^"]+)"'
    $matches = [regex]::Matches($content, $pattern)
    
    if ($matches.Count -gt 0) {
        $url = $matches[0].Groups[1].Value
        $isBroken = $false
        
        # Kiểm tra xem URL có thuộc domain bị hỏng không
        foreach ($brokenDomain in $potentiallyBrokenDomains) {
            if ($url -like "*$brokenDomain*") {
                $isBroken = $true
                break
            }
        }
        
        # Ghi thông tin vào file
        if ($isBroken) {
            "$($file.Name): $url [CÓ THỂ BỊ HỎNG]" | Out-File -FilePath $outputFile -Append
            "$($file.FullName)" | Out-File -FilePath $brokenGamesFile -Append
            $brokenGameCount++
        } else {
            "$($file.Name): $url" | Out-File -FilePath $outputFile -Append
        }
    }
    else {
        # Nếu không tìm thấy iframe, ghi thông tin vào file
        "$($file.Name): Không tìm thấy iframe URL [CÓ THỂ BỊ HỎNG]" | Out-File -FilePath $outputFile -Append
        "$($file.FullName)" | Out-File -FilePath $brokenGamesFile -Append
        $brokenGameCount++
    }
}

Write-Host "Hoàn tất! Tìm thấy $brokenGameCount game có thể bị hỏng."
Write-Host "Thông tin đã được lưu vào $outputFile"
Write-Host "Danh sách game có thể bị hỏng đã được lưu vào $brokenGamesFile" 