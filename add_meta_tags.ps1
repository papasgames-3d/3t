$htmlFiles = Get-ChildItem -Path "game\*.html"

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
        
        # Chèn meta tags vào trước thẻ </head>
        $content = $content -replace '(<meta name="robots" content="index, follow">)\s*</head>', "`$1$metaTags`n    </head>"
        
        # Lưu lại file
        Set-Content -Path $file.FullName -Value $content
    }
    else {
        Write-Host "Meta tags already exist in $($file.Name)"
    }
}

Write-Host "Completed adding meta tags to all HTML files in the game directory." 