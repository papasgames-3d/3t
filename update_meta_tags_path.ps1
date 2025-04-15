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
$logFile = "$logFolder\updated_meta_paths.txt"
$errorLog = "$logFolder\image_not_found_update.txt"

# Xóa file log cũ nếu tồn tại
if (Test-Path $errorLog) {
    Remove-Item $errorLog -Force
}
if (Test-Path $logFile) {
    Remove-Item $logFile -Force
}

Write-Host "Total HTML files to process: $totalFiles"

foreach ($file in $htmlFiles) {
    $filename = $file.BaseName
    $imageFound = $false
    $imagePath = ""
    
    # Hiển thị tên file đang xử lý
    Write-Host "Processing: $($file.Name)" -ForegroundColor Cyan
    
    # Đọc nội dung file
    $content = Get-Content -Path $file.FullName -Raw
    
    # Kiểm tra xem thẻ meta đã tồn tại chưa
    if ($content -notmatch '<meta property="og:image"') {
        Write-Host "Meta tags don't exist in $($file.Name) - skipping" -ForegroundColor Gray
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
        # Trong trường hợp này, chúng ta không thay đổi đường dẫn hiện tại
        continue
    }
    
    # Lấy đường dẫn hình ảnh hiện tại
    $ogImageMatch = [regex]::Match($content, '<meta property="og:image" content="([^"]+)"')
    $twitterImageMatch = [regex]::Match($content, '<meta name="twitter:image" content="([^"]+)"')
    
    $currentOgPath = ""
    $currentTwitterPath = ""
    
    if ($ogImageMatch.Success) {
        $currentOgPath = $ogImageMatch.Groups[1].Value
    }
    
    if ($twitterImageMatch.Success) {
        $currentTwitterPath = $twitterImageMatch.Groups[1].Value
    }
    
    # Kiểm tra xem đường dẫn có cần thay đổi không
    $needsUpdate = $false
    
    if ($currentOgPath -ne $imagePath -or $currentTwitterPath -ne $imagePath) {
        $needsUpdate = $true
        Write-Host "Current paths:" -ForegroundColor Yellow
        Write-Host "  OG Image: $currentOgPath" -ForegroundColor Yellow
        Write-Host "  Twitter Image: $currentTwitterPath" -ForegroundColor Yellow
        Write-Host "New path: $imagePath" -ForegroundColor Green
    }
    
    # Chỉ cập nhật nếu cần
    if ($needsUpdate) {
        # Cập nhật đường dẫn trong nội dung
        if ($ogImageMatch.Success) {
            $content = $content -replace [regex]::Escape($ogImageMatch.Value), "<meta property=`"og:image`" content=`"$imagePath`""
        }
        
        if ($twitterImageMatch.Success) {
            $content = $content -replace [regex]::Escape($twitterImageMatch.Value), "<meta name=`"twitter:image`" content=`"$imagePath`""
        }
        
        # Lưu lại file
        Set-Content -Path $file.FullName -Value $content
        
        # Ghi log
        Add-Content -Path $logFile -Value "$($file.FullName)|$currentOgPath|$imagePath"
        
        $processedFiles++
        Write-Host "Updated meta paths in file" -ForegroundColor Green
    }
    else {
        Write-Host "Image paths are already correct - no changes needed" -ForegroundColor Gray
    }
    
    Write-Host "-----------------------------------------"
}

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Completed updating meta tags in $processedFiles files" -ForegroundColor Green
if ($notFoundImages -gt 0) {
    Write-Host "Warning: $notFoundImages files did not have matching images" -ForegroundColor Yellow
    Write-Host "Check $errorLog for details" -ForegroundColor Yellow
}
Write-Host "=============================================" -ForegroundColor Cyan 