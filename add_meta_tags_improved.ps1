$htmlFiles = Get-ChildItem -Path "game\*.html"
$count = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    $filename = $file.BaseName
    $imagePath = "../assets/upload/games66ez/jpg/$filename.jpg"
    
    # Kiểm tra xem meta đã tồn tại chưa
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
        
        # Tìm vị trí để chèn meta tags
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
        $count++
    }
    else {
        Write-Host "Meta tags already exist in $($file.Name)"
    }
}

Write-Host "Completed adding meta tags to $count HTML files in the game directory." 