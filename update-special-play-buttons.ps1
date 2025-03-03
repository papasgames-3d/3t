# Update Special Play Buttons Script
# Đây là script để xử lý các trang web tương tự như 11-11.html, với một cấu trúc nút "Play Now" đặc biệt

# Tạo file log
$logFilePath = Join-Path -Path $PSScriptRoot -ChildPath "update-special-buttons-log.txt"
"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Bắt đầu xử lý các trang chơi game đặc biệt..." | Out-File -FilePath $logFilePath

# Hàm để ghi log
function LogMessage {
    param (
        [string]$Message
    )
    
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    "$timestamp - $Message" | Out-File -FilePath $logFilePath -Append
    Write-Host $Message
}

# Hàm để cập nhật file HTML
function UpdateSpecialHtmlFile {
    param (
        [string]$FilePath
    )
    
    try {
        # Đọc nội dung file HTML
        $htmlContent = Get-Content -Path $FilePath -Raw -Encoding UTF8
        $fileName = Split-Path -Path $FilePath -Leaf
        
        # Kiểm tra xem file có chứa nút "Play Now" đặc biệt không
        if ($htmlContent -match '<div class="talpa-btn-play">') {
            LogMessage "Xử lý file: $fileName"
            
            # Kiểm tra xem file đã có iframe trực tiếp chưa
            if ($htmlContent -match '<iframe\s+title="[^"]*"\s+src="([^"]+)"\s+allowfullscreen') {
                # Lấy URL của game từ iframe
                $gameUrl = $matches[1]
                LogMessage "  - Đã tìm thấy URL game trong iframe: $gameUrl"
                
                # Tạo mẫu để tìm và thay thế
                $patternToReplace = '<div data-url="[^"]*" id="game-arena">(?:\s|.)*?<div class="talpa-btn-play">(?:\s|.)*?<\/div>(?:\s|.)*?<iframe.*?<\/iframe>(?:\s|.)*?<\/div>'
                $replacement = @"
<div data-url="$gameUrl" id="game-arena">
    <iframe title="$fileName" src="$gameUrl" allowfullscreen frameborder="0" width="100%" height="100%" scrolling="none"></iframe>
</div>
"@
                
                # Thực hiện thay thế
                $updatedContent = $htmlContent -replace $patternToReplace, $replacement
                
                # Nếu không thay thế được bằng regex, thử tìm và thay thế theo cách khác
                if ($updatedContent -eq $htmlContent) {
                    LogMessage "  - Pattern match not successful, trying alternative approach"
                    
                    # Tạo đối tượng HTML để phân tích
                    $tempFile = [System.IO.Path]::GetTempFileName()
                    $htmlContent | Out-File -FilePath $tempFile -Encoding UTF8
                    
                    # Đọc lại nội dung từ tempFile và sử dụng string manipulation
                    $htmlContent = Get-Content -Path $tempFile -Raw -Encoding UTF8
                    
                    # Tìm khu vực game-arena
                    $startIndex = $htmlContent.IndexOf('<div data-url=')
                    $endIndex = $htmlContent.IndexOf('</div>', $startIndex)
                    
                    # Tìm điểm kết thúc thực sự của div game-arena (có thể có nhiều thẻ div lồng nhau)
                    $nestLevel = 1
                    $searchIndex = $endIndex + 6
                    
                    while (($nestLevel -gt 0) -and ($searchIndex -lt $htmlContent.Length)) {
                        $nextOpenDiv = $htmlContent.IndexOf('<div', $searchIndex)
                        $nextCloseDiv = $htmlContent.IndexOf('</div>', $searchIndex)
                        
                        if (($nextOpenDiv -ne -1) -and ($nextOpenDiv -lt $nextCloseDiv)) {
                            $nestLevel++
                            $searchIndex = $nextOpenDiv + 4
                        } 
                        elseif ($nextCloseDiv -ne -1) {
                            $nestLevel--
                            $searchIndex = $nextCloseDiv + 6
                        } 
                        else {
                            break
                        }
                    }
                    
                    if ($searchIndex -gt $endIndex) {
                        $endIndex = $searchIndex
                    }
                    
                    # Tạo nội dung mới
                    $beforeGameArena = $htmlContent.Substring(0, $startIndex)
                    $afterGameArena = $htmlContent.Substring($endIndex)
                    
                    $newGameArena = @"
<div data-url="$gameUrl" id="game-arena">
    <iframe title="$fileName" src="$gameUrl" allowfullscreen frameborder="0" width="100%" height="100%" scrolling="none"></iframe>
</div>
"@
                    
                    $updatedContent = $beforeGameArena + $newGameArena + $afterGameArena
                    Remove-Item -Path $tempFile
                }
                
                # Lưu nội dung đã cập nhật
                $updatedContent | Out-File -FilePath $FilePath -Encoding UTF8
                
                LogMessage "  - Đã cập nhật thành công: $fileName"
                return "Updated"
            } 
            else {
                LogMessage "  - Không tìm thấy URL trong iframe: $fileName"
                return "Skipped"
            }
        } 
        else {
            # LogMessage "  - Không cần cập nhật (không tìm thấy nút Play Now đặc biệt): $fileName"
            return "NotNeeded"
        }
    } 
    catch {
        LogMessage "  - LỖI xử lý file $FilePath : $_"
        return "Error"
    }
}

# Tìm và xử lý tất cả các file HTML trong thư mục gốc và thư mục 'go'
$rootDirectory = $PSScriptRoot
$goDirectory = Join-Path -Path $rootDirectory -ChildPath "go"

# Khởi tạo bộ đếm
$totalFiles = 0
$updatedFiles = 0
$skippedFiles = 0
$errorFiles = 0
$notNeededFiles = 0

# Xử lý các file trong thư mục 'go'
LogMessage "Đang xử lý các file HTML trong thư mục 'go'..."
$goHtmlFiles = Get-ChildItem -Path $goDirectory -Filter "*.html"
LogMessage "Đã tìm thấy $($goHtmlFiles.Count) file HTML trong thư mục 'go'"

foreach ($file in $goHtmlFiles) {
    $totalFiles++
    $result = UpdateSpecialHtmlFile -FilePath $file.FullName
    
    switch ($result) {
        "Updated" { $updatedFiles++ }
        "Skipped" { $skippedFiles++ }
        "Error" { $errorFiles++ }
        "NotNeeded" { $notNeededFiles++ }
    }
}

# Xử lý các file trong thư mục gốc
LogMessage "Đang xử lý các file HTML trong thư mục gốc..."
$rootHtmlFiles = Get-ChildItem -Path $rootDirectory -Filter "*.html" | Where-Object { $_.Name -ne "index.html" }
LogMessage "Đã tìm thấy $($rootHtmlFiles.Count) file HTML trong thư mục gốc"

foreach ($file in $rootHtmlFiles) {
    $totalFiles++
    $result = UpdateSpecialHtmlFile -FilePath $file.FullName
    
    switch ($result) {
        "Updated" { $updatedFiles++ }
        "Skipped" { $skippedFiles++ }
        "Error" { $errorFiles++ }
        "NotNeeded" { $notNeededFiles++ }
    }
}

# Tổng kết
$summary = @"
=== KẾT QUẢ XỬ LÝ ===
Tổng số file đã xử lý: $totalFiles
Số file đã cập nhật: $updatedFiles
Số file bỏ qua (không tìm thấy URL): $skippedFiles
Số file không cần cập nhật: $notNeededFiles
Số file lỗi: $errorFiles
"@

LogMessage $summary
LogMessage "Hoàn thành! Chi tiết xem tại: $logFilePath" 