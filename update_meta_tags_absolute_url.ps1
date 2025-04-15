# Tạo thư mục logs nếu chưa tồn tại
$logFolder = "meta_logs"
if (-not (Test-Path $logFolder)) {
    New-Item -ItemType Directory -Path $logFolder | Out-Null
}

# Lấy tất cả các file HTML trong thư mục game
$htmlFiles = Get-ChildItem -Path "game\*.html"
$totalFiles = $htmlFiles.Count
$processedFiles = 0

# File log
$logFile = "$logFolder\updated_absolute_urls.txt"

# Xóa file log cũ nếu tồn tại
if (Test-Path $logFile) {
    Remove-Item $logFile -Force
}

# Cấu hình batch
$batchSize = 20
$batches = [Math]::Ceiling($totalFiles / $batchSize)

Write-Host "Total HTML files to process: $totalFiles"
Write-Host "Processing in $batches batches of $batchSize files each"

# Định nghĩa domain tuyệt đối
$domainUrl = "https://monkeymart.one"

# Xử lý theo từng lô
for ($batch = 0; $batch -lt $batches; $batch++) {
    $start = $batch * $batchSize
    $end = [Math]::Min(($batch + 1) * $batchSize, $totalFiles) - 1
    
    Write-Host "Processing batch $($batch + 1) of $batches (files $($start + 1) to $($end + 1))" -ForegroundColor Magenta
    
    for ($i = $start; $i -le $end; $i++) {
        $file = $htmlFiles[$i]
        $filename = $file.BaseName
        
        # Hiển thị tên file đang xử lý
        Write-Host "Processing: $($file.Name)" -ForegroundColor Cyan
        
        # Đọc nội dung file
        $content = Get-Content -Path $file.FullName -Raw
        
        # Kiểm tra xem thẻ meta đã tồn tại chưa
        if ($content -notmatch '<meta property="og:image"') {
            Write-Host "Meta tags don't exist in $($file.Name) - skipping" -ForegroundColor Gray
            continue
        }
        
        # Lấy đường dẫn hình ảnh hiện tại
        $ogImageMatch = [regex]::Match($content, '<meta property="og:image" content="([^"]+)"')
        $twitterImageMatch = [regex]::Match($content, '<meta name="twitter:image" content="([^"]+)"')
        
        $currentOgPath = ""
        $currentTwitterPath = ""
        $absoluteOgPath = ""
        $absoluteTwitterPath = ""
        
        if ($ogImageMatch.Success) {
            $currentOgPath = $ogImageMatch.Groups[1].Value
            # Chuyển đổi luôn mà không kiểm tra
            $absoluteOgPath = $currentOgPath -replace "^\.\.", $domainUrl
            $absoluteOgPath = $absoluteOgPath -replace "^/", "$domainUrl/"
            
            # Trong trường hợp đường dẫn không bắt đầu bằng "../" hoặc "/"
            if ($absoluteOgPath -notmatch "^$domainUrl") {
                $absoluteOgPath = "$domainUrl/$absoluteOgPath"
            }
        }
        
        if ($twitterImageMatch.Success) {
            $currentTwitterPath = $twitterImageMatch.Groups[1].Value
            # Chuyển đổi luôn mà không kiểm tra
            $absoluteTwitterPath = $currentTwitterPath -replace "^\.\.", $domainUrl
            $absoluteTwitterPath = $absoluteTwitterPath -replace "^/", "$domainUrl/"
            
            # Trong trường hợp đường dẫn không bắt đầu bằng "../" hoặc "/"
            if ($absoluteTwitterPath -notmatch "^$domainUrl") {
                $absoluteTwitterPath = "$domainUrl/$absoluteTwitterPath"
            }
        }
        
        # Hiển thị thông tin về đường dẫn
        Write-Host "Current paths:" -ForegroundColor Yellow
        Write-Host "  OG Image: $currentOgPath" -ForegroundColor Yellow
        if ($absoluteOgPath) {
            Write-Host "  New OG Image: $absoluteOgPath" -ForegroundColor Green
        }
        
        Write-Host "  Twitter Image: $currentTwitterPath" -ForegroundColor Yellow
        if ($absoluteTwitterPath) {
            Write-Host "  New Twitter Image: $absoluteTwitterPath" -ForegroundColor Green
        }
        
        # Cập nhật đường dẫn trong nội dung
        if ($ogImageMatch.Success -and $absoluteOgPath) {
            $content = $content -replace [regex]::Escape($ogImageMatch.Value), "<meta property=`"og:image`" content=`"$absoluteOgPath`""
        }
        
        if ($twitterImageMatch.Success -and $absoluteTwitterPath) {
            $content = $content -replace [regex]::Escape($twitterImageMatch.Value), "<meta name=`"twitter:image`" content=`"$absoluteTwitterPath`""
        }
        
        # Lưu lại file
        Set-Content -Path $file.FullName -Value $content
        
        # Ghi log
        Add-Content -Path $logFile -Value "$($file.FullName)|$currentOgPath|$absoluteOgPath"
        
        $processedFiles++
        Write-Host "Updated to absolute URLs in file" -ForegroundColor Green
        Write-Host "-----------------------------------------"
    }
    
    # Thông báo tiến độ sau mỗi lô
    Write-Host "Completed batch $($batch + 1) of $batches. Processed $processedFiles files so far." -ForegroundColor Green
    
    # Nếu không phải lô cuối cùng, tạm dừng
    if ($batch -lt $batches - 1) {
        Write-Host "Taking a short break before next batch..." -ForegroundColor Cyan
        Start-Sleep -Seconds 2
    }
}

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Completed updating to absolute URLs in $processedFiles files" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan 