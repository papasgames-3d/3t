# Script de tim va hien thi cac iframe URLs trong cac file game
$gameDir = ".\game"
$outputFile = "iframe_urls.txt"
$brokenGamesFile = "broken_games.txt"

# Danh sach cac domain co the da bi hong
$potentiallyBrokenDomains = @(
    "classroom6x.gitlab.io",
    "games66ez.gitlab.io",
    "classroom6x.minecraftapk.com",
    "ghgstore311.github.io",
    "classroom6x.com",
    "games66ez.com",
    "classroom6x.net",
    "games66ez.net"
    # Them cac domain khac neu can
)

# Xoa file output neu da ton tai
if (Test-Path $outputFile) {
    Remove-Item $outputFile
}

if (Test-Path $brokenGamesFile) {
    Remove-Item $brokenGamesFile
}

# Tim tat ca cac file HTML trong thu muc game
$htmlFiles = Get-ChildItem -Path $gameDir -Filter "*.html"

# Thong bao so luong file se duoc kiem tra
Write-Host "Tim thay $($htmlFiles.Count) file HTML de kiem tra."

$brokenGameCount = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Su dung regex de tim tat ca iframe URLs
    $pattern = '<iframe[^>]* src="([^"]+)"'
    $matches = [regex]::Matches($content, $pattern)
    $isBroken = $false
    $brokenUrls = @()
    
    if ($matches.Count -gt 0) {
        # Kiem tra tat ca cac iframe URLs trong file
        foreach ($match in $matches) {
            $url = $match.Groups[1].Value
            
            # Kiem tra xem URL co thuoc domain bi hong khong
            foreach ($brokenDomain in $potentiallyBrokenDomains) {
                if ($url -like "*$brokenDomain*") {
                    $isBroken = $true
                    $brokenUrls += $url
                    break
                }
            }
            
            # Kiem tra duong dan tuong doi khong hop le
            if ($url -like "../game/iframe/*" -and -not (Test-Path (Join-Path $gameDir $url))) {
                $isBroken = $true
                $brokenUrls += $url
            }
        }
        
        # Ghi thong tin vao file
        if ($isBroken) {
            "$($file.Name): Broken URLs found: $($brokenUrls -join ', ')" | Out-File -FilePath $outputFile -Append
            "$($file.FullName)" | Out-File -FilePath $brokenGamesFile -Append
            $brokenGameCount++
        } else {
            "$($file.Name): OK - URLs: $($matches[0].Groups[1].Value)" | Out-File -FilePath $outputFile -Append
        }
    }
    else {
        # Neu khong tim thay iframe, ghi thong tin vao file
        "$($file.Name): No iframe URL found [BROKEN]" | Out-File -FilePath $outputFile -Append
        "$($file.FullName)" | Out-File -FilePath $brokenGamesFile -Append
        $brokenGameCount++
    }
}

Write-Host "Hoan tat! Tim thay $brokenGameCount game co the bi hong."
Write-Host "Thong tin da duoc luu vao $outputFile"
Write-Host "Danh sach game co the bi hong da duoc luu vao $brokenGamesFile" 