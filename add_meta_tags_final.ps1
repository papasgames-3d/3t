$htmlFiles = Get-ChildItem -Path "game\*.html"
$count = 0

foreach ($file in $htmlFiles) {
    $filename = $file.BaseName
    $imagePath = "../assets/upload/games66ez/jpg/$filename.jpg"
    
    # Đọc toàn bộ nội dung file
    $content = Get-Content -Path $file.FullName -Raw
    
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
        
        # Phương pháp chèn thẻ meta mới - đọc file theo từng dòng
        $lines = Get-Content -Path $file.FullName
        $newContent = @()
        $metaAdded = $false
        
        for ($i = 0; $i -lt $lines.Count; $i++) {
            $newContent += $lines[$i]
            
            # Chèn meta tags vào trước thẻ đóng head
            if ($lines[$i] -match '</head>' -and -not $metaAdded) {
                # Thêm meta ngay trước thẻ đóng head
                $headLine = $newContent[-1]
                $newContent[-1] = $headLine -replace '</head>', "$metaTags`n    </head>"
                $metaAdded = $true
            }
        }
        
        # Ghi nội dung mới vào file
        Set-Content -Path $file.FullName -Value $newContent
        $count++
    }
    else {
        Write-Host "Meta tags already exist in $($file.Name)"
    }
}

Write-Host "Completed adding meta tags to $count HTML files in the game directory." 