# PowerShell script to remove Play Now buttons from all game pages in both root and go directories
# This script directly embeds the iframe in each game page

Write-Host "Removing Play Now buttons from all game pages..."

# Process HTML files in the go directory
Write-Host "Processing files in go directory..."
$goFiles = Get-ChildItem -Path "go" -Filter "*.html" -Recurse

# Process game HTML files in the root directory
Write-Host "Processing files in root directory..."
$rootFiles = Get-ChildItem -Path "." -Filter "*.html" | Where-Object {
    # Only process files that might be game files (have the Play Now button)
    $content = Get-Content -Path $_.FullName -Raw
    $content -match 'talpa-btn-play' -and $content -match 'function playGame\(\)'
}

# Combine both file lists
$allFiles = $goFiles + $rootFiles

foreach ($file in $allFiles) {
    Write-Host "Processing $($file.FullName)..."
    
    # Read the file content
    $content = Get-Content -Path $file.FullName -Raw
    
    # Skip if there's no Play Now button
    if (-not ($content -match 'talpa-btn-play')) {
        Write-Host "No Play Now button found in $($file.FullName), skipping..."
        continue
    }
    
    # Get the game URL from the data-url attribute using regex
    $urlMatch = [regex]::Match($content, 'data-url="([^"]*)"')
    if ($urlMatch.Success) {
        $gameUrl = $urlMatch.Groups[1].Value
    } else {
        Write-Host "Warning: No game URL found in $($file.FullName), skipping..."
        continue
    }
    
    # Get the game title
    $titleMatch = [regex]::Match($content, '<h1 class="section-title">(.*?)</h1>')
    if ($titleMatch.Success) {
        $gameTitle = $titleMatch.Groups[1].Value
    } else {
        $gameTitle = "Game"
    }
    
    Write-Host "Game URL: $gameUrl"
    Write-Host "Game Title: $gameTitle"
    
    # Replace the splash container with an iframe
    $newContent = [regex]::Replace($content, 
        '(?s)<div class="talpa-splash-container.*?</div></div></div>', 
        "`t`t`t`t`t`t<iframe title=`"$gameTitle`" src=`"$gameUrl`" allowfullscreen frameborder=`"0`" width=`"100%`" height=`"100%`" scrolling=`"none`"></iframe>")
    
    # Remove the playGame() function
    $newContent = [regex]::Replace($newContent, '(?s)function playGame\(\).*?}', '')
    
    # Write the updated content back to the file
    Set-Content -Path $file.FullName -Value $newContent
    
    Write-Host "Updated $($file.FullName)"
}

Write-Host "All files have been updated!" 