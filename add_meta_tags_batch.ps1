# Đường dẫn tới thư mục logs để lưu tiến trình
$logFolder = "meta_logs"
if (-not (Test-Path $logFolder)) {
    New-Item -ItemType Directory -Path $logFolder | Out-Null
}

# Lấy tất cả các file HTML trong thư mục game
$htmlFiles = Get-ChildItem -Path "game\*.html"
$totalFiles = $htmlFiles.Count
$processedFiles = 0
$batchSize = 50 # Xử lý 50 file mỗi lần
$batches = [Math]::Ceiling($totalFiles / $batchSize)

Write-Host "Total HTML files found: $totalFiles"
Write-Host "Processing in $batches batches of $batchSize files each"

# Kiểm tra nếu có file log để tiếp tục từ lần chạy trước
$logFile = "$logFolder\processed_files.txt"
$processedList = @()
if (Test-Path $logFile) {
    $processedList = Get-Content $logFile
    Write-Host "Found $($processedList.Count) previously processed files"
}

# Xử lý theo từng lô
for ($batch = 0; $batch -lt $batches; $batch++) {
    $start = $batch * $batchSize
    $end = [Math]::Min(($batch + 1) * $batchSize, $totalFiles) - 1
    
    Write-Host "Processing batch $($batch + 1) of $batches (files $($start + 1) to $($end + 1))"
    
    # Xử lý từng file trong lô
    for ($i = $start; $i -le $end; $i++) {
        $file = $htmlFiles[$i]
        
        # Kiểm tra nếu file đã được xử lý từ trước
        if ($processedList -contains $file.FullName) {
            Write-Host "Skipping already processed file: $($file.Name)"
            continue
        }
        
        $filename = $file.BaseName
        $imagePath = "../assets/upload/games66ez/jpg/$filename.jpg"
        
        # Đọc nội dung file
        try {
            $content = Get-Content -Path $file.FullName -Raw -ErrorAction Stop
            
            # Kiểm tra nếu meta OG image đã tồn tại
            if ($content -notmatch '<meta property="og:image"') {
                Write-Host "Adding meta tags to $($file.Name)"
                
                # Tạo các thẻ meta
                $metaTags = @"

    <meta property="og:image" content="$imagePath" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:title" content="$($filename.ToUpper()) - Play AT Monkey Mart One" />
    <meta property="og:description" content="$($filename.ToUpper()) - Play AT Monkey Mart One .Gitlab.io: Enjoy browser play, fullscreen action, and an ad-free gaming experience. Dive into fun today!" />
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:image" content="$imagePath" />
"@
                
                # Đặt meta tags trước thẻ đóng head
                $content = $content -replace '</head>', "$metaTags`n    </head>"
                
                # Lưu lại nội dung mới
                Set-Content -Path $file.FullName -Value $content -ErrorAction Stop
                
                # Lưu lại tên file đã xử lý
                Add-Content -Path $logFile -Value $file.FullName -ErrorAction Stop
                
                $processedFiles++
            }
            else {
                Write-Host "Meta tags already exist in $($file.Name)"
                # Vẫn lưu vào danh sách đã xử lý
                Add-Content -Path $logFile -Value $file.FullName -ErrorAction Stop
            }
        }
        catch {
            Write-Host "Error processing file $($file.Name): $_" -ForegroundColor Red
        }
    }
    
    # Thông báo tiến độ sau mỗi lô
    Write-Host "Completed batch $($batch + 1) of $batches. Processed $processedFiles new files so far."
    Write-Host "Taking a short break before next batch..."
    Start-Sleep -Seconds 2
}

Write-Host "Completed adding meta tags. Added to $processedFiles new files." -ForegroundColor Green 