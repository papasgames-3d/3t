# Script de kiem tra va xoa cac game bi hong trong cac file HTML
$brokenGamesFile = "broken_games.txt"

# Doc danh sach cac game bi hong
if (-not (Test-Path $brokenGamesFile)) {
    Write-Host "Khong tim thay file broken_games.txt. Vui long chay check_broken_games_fixed.ps1 truoc." -ForegroundColor Red
    exit
}

$brokenGames = Get-Content $brokenGamesFile | ForEach-Object { 
    $_ -replace '.*\\game\\', '' -replace '\.html$', ''
}

Write-Host "Da tim thay $($brokenGames.Count) game bi hong."

# Danh sach cac file can kiem tra
$filesToCheck = @(
    "index.html",
    "category/*.html"
)

$modifiedFiles = @()

foreach ($filePattern in $filesToCheck) {
    $files = Get-ChildItem -Path $filePattern
    foreach ($file in $files) {
        Write-Host "Dang kiem tra file $($file.Name)..." -ForegroundColor Yellow
        
        $content = Get-Content $file.FullName -Raw
        $modified = $false
        
        # Kiem tra va xoa cac link den game bi hong
        foreach ($brokenGame in $brokenGames) {
            $gamePattern = "(?s)<div class=`"col-sm-6 col-md-4 col-lg-2 game-item`">\s*<a class=`"game-link`" href=`"/game/$brokenGame\.html`".*?</div>"
            if ($content -match $gamePattern) {
                $content = $content -replace $gamePattern, ""
                $modified = $true
                Write-Host "  - Da xoa game $brokenGame" -ForegroundColor Green
            }
        }
        
        # Neu file bi thay doi, luu lai
        if ($modified) {
            $content | Set-Content $file.FullName -Force
            $modifiedFiles += $file.Name
        }
    }
}

if ($modifiedFiles.Count -gt 0) {
    Write-Host "`nDa cap nhat $($modifiedFiles.Count) file:" -ForegroundColor Green
    $modifiedFiles | ForEach-Object { Write-Host "  - $_" -ForegroundColor Green }
} else {
    Write-Host "`nKhong co file nao can cap nhat." -ForegroundColor Yellow
} 