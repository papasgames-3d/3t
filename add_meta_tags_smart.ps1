# Tạo thư mục logs nếu chưa tồn tại
$logFolder = "meta_logs"
if (-not (Test-Path $logFolder)) {
    New-Item -ItemType Directory -Path $logFolder | Out-Null
}

# Danh sách các thư mục upload cần kiểm tra
$uploadFolders = @(
    "games66ez",
    "topvaz",
    "classroom6x"
)

# Lấy tất cả các file HTML trong thư mục game
$htmlFiles = Get-ChildItem -Path "game\*.html"
$totalFiles = $htmlFiles.Count
$processedFiles = 0
$notFoundImages = 0

# File log
$logFile = "$logFolder\processed_smart.txt"
$errorLog = "$logFolder\image_not_found.txt"

# Xóa file log cũ nếu tồn tại
if (Test-Path $errorLog) {
    Remove-Item $errorLog -Force
}

Write-Host "Total HTML files to process: $totalFiles"

# Tạo file log trống
Set-Content -Path $logFile -Value ""
Set-Content -Path $errorLog -Value ""

foreach ($file in $htmlFiles) {
    $filename = $file.BaseName
    $imageFound = $false
    $imagePath = ""
    
    # Hiển thị tên file đang xử lý
    Write-Host "Processing: $($file.Name)" -ForegroundColor Cyan
    
    # Kiểm tra xem meta đã tồn tại chưa
    $content = Get-Content -Path $file.FullName -Raw
    if ($content -match '<meta property="og:image"') {
        Write-Host "Meta tags already exist in $($file.Name)" -ForegroundColor Gray
        continue
    }
    
    # Tìm kiếm ảnh trong tất cả các thư mục upload
    foreach ($folder in $uploadFolders) {
        # Đường dẫn tuyệt đối để kiểm tra sự tồn tại
        $jpgAbsolutePath = Join-Path -Path $PWD -ChildPath "assets\upload\$folder\jpg\$filename.jpg"
        $pngAbsolutePath = Join-Path -Path $PWD -ChildPath "assets\upload\$folder\png\$filename.png"
        
        # Đường dẫn tương đối để sử dụng trong HTML
        $jpgRelativePath = "../assets/upload/$folder/jpg/$filename.jpg"
        $pngRelativePath = "../assets/upload/$folder/png/$filename.png"
        
        # Kiểm tra file JPG
        if (Test-Path $jpgAbsolutePath) {
            $imagePath = $jpgRelativePath
            $imageFound = $true
            Write-Host "Found JPG image in $folder folder" -ForegroundColor Green
            break
        }
        
        # Kiểm tra file PNG
        if (Test-Path $pngAbsolutePath) {
            $imagePath = $pngRelativePath
            $imageFound = $true
            Write-Host "Found PNG image in $folder folder" -ForegroundColor Green
            break
        }
    }
    
    # Nếu không tìm thấy ảnh, ghi vào log lỗi
    if (-not $imageFound) {
        Write-Host "No image found for $filename" -ForegroundColor Yellow
        Add-Content -Path $errorLog -Value "$filename"
        $notFoundImages++
        
        # Sử dụng đường dẫn mặc định
        $imagePath = "../assets/upload/games66ez/jpg/$filename.jpg"
        Write-Host "Using default path instead: $imagePath" -ForegroundColor Yellow
    }
    
    Write-Host "Adding meta tags to $($file.Name) with image: $imagePath"
    
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
    
    # Xử lý các trường hợp khác nhau của vị trí chèn
    if ($content -match '<meta name="robots" content="index, follow">') {
        # Trường hợp 1: Có thẻ robots
        $content = $content -replace '(<meta name="robots" content="index, follow">)\s*</head>', "`$1$metaTags`n    </head>"
    } 
    elseif ($content -match '<link rel="canonical"') {
        # Trường hợp 2: Có thẻ canonical
        $content = $content -replace '(<link rel="canonical"[^>]*>)\s*</head>', "`$1$metaTags`n    </head>"
    }
    else {
        # Trường hợp 3: Chèn trước thẻ đóng head
        $content = $content -replace '</head>', "$metaTags`n    </head>"
    }
    
    # Lưu lại file
    Set-Content -Path $file.FullName -Value $content
    
    # Ghi nhật ký
    Add-Content -Path $logFile -Value "$($file.FullName)|$imagePath"
    
    $processedFiles++
    Write-Host "Progress: $processedFiles / $totalFiles" -ForegroundColor Green
    Write-Host "-----------------------------------------"
}

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Completed adding meta tags to $processedFiles files" -ForegroundColor Green
if ($notFoundImages -gt 0) {
    Write-Host "Warning: $notFoundImages files did not have matching images" -ForegroundColor Yellow
    Write-Host "Check $errorLog for details" -ForegroundColor Yellow
}
Write-Host "=============================================" -ForegroundColor Cyan 