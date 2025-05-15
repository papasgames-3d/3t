# Simplified script to apply the modern template to game HTML files
# This version avoids complex path manipulations that might cause linter errors

Write-Host "Starting to apply modern template to game HTML files..." -ForegroundColor Yellow

# Create a timestamp for backup files
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# Get all HTML files in the game directory
$gameFiles = Get-ChildItem -Path ".\game" -Filter "*.html" -Recurse

# Display count of files found
Write-Host "Found $($gameFiles.Count) game HTML files to process." -ForegroundColor Green

# Confirm before proceeding
$confirmation = Read-Host "Do you want to proceed with applying the template to all these files? (y/n)"
if ($confirmation -ne "y") {
    Write-Host "Operation cancelled by user." -ForegroundColor Yellow
    exit
}

# Counter for progress
$processed = 0
$successful = 0
$failed = 0

foreach ($file in $gameFiles) {
    $processed++
    $filePath = $file.FullName
    
    Write-Progress -Activity "Applying template" -Status "Processing file $processed of $($gameFiles.Count): $($file.Name)" -PercentComplete (($processed / $gameFiles.Count) * 100)
    
    try {
        # First create a backup of the original file
        Copy-Item -Path $filePath -Destination "$filePath.backup" -Force
        
        # Read the content of the original file
        $content = Get-Content -Path $filePath -Raw -ErrorAction Stop
        
        # Extract the important information from the original file using simple regex patterns
        if ($content -match '<title>(.*?)</title>') {
            $title = $matches[1]
        } else {
            $title = "Game Title"
        }
        
        if ($content -match '<h1[^>]*?>(.*?)</h1>') {
            $h1Title = $matches[1]
        } else {
            $h1Title = $title
        }
        
        if ($content -match '<iframe[^>]*?src="([^"]*)"[^>]*?>') {
            $iframeSrc = $matches[1]
        } else {
            $iframeSrc = ""
        }
        
        if ($content -match '<meta name="description"[^>]*?content="([^"]*)"[^>]*?>') {
            $description = $matches[1]
        } else {
            $description = "Play this game instantly in your browser for free!"
        }
        
        # Calculate relative path based on file depth
        $depth = ($filePath.Split('\') | Where-Object { $_ -eq "game" }).Count
        if ($depth -eq 1) {
            $relativePath = "../"
        } else {
            $relativePath = "../../"
        }
        
        # Generate the new content using the template
        $newContent = @"
<!DOCTYPE html>
<html data-bs-theme="light" lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    
    <title>$title</title>
    <meta name="description" content="$description">
    <link rel="stylesheet" href="${relativePath}assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="${relativePath}assets/fonts/font-awesome.min.css">
    <link rel="stylesheet" href="${relativePath}assets/css/Navbar-Right-Links-icons.css">
    <link rel="stylesheet" href="${relativePath}assets/css/styles.css">
    <link rel="stylesheet" href="${relativePath}modern-style.css">
    <meta name="robots" content="index, follow">
</head>

<body>
    <header id="header" class="sticky-top">
        <nav class="navbar navbar-expand-lg py-3">
            <div class="container"><a class="navbar-brand d-flex align-items-center" href="/"><img
                        src="${relativePath}assets/img/logo.png" alt="Monkey Mart Logo" style="height:40px"></a><button data-bs-toggle="collapse"
                    class="navbar-toggler" data-bs-target="#navcol-2"><span class="visually-hidden">Toggle
                        navigation</span><span class="navbar-toggler-icon"></span></button>
                <div class="collapse navbar-collapse nav-right" id="navcol-2">
                    <div class="search">
                        <div class="search-game">
                            <div class="form-search"><input type="text" id="search-bar" class="search-bar"
                                    placeholder="Search Games"><svg xmlns="http://www.w3.org/2000/svg" width="1em"
                                    height="1em" fill="currentColor" viewBox="0 0 16 16"
                                    class="bi bi-search icon-search" id="search-button" aria-label="Search button">
                                    <path
                                        d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0">
                                    </path>
                                </svg></div>
                        </div>
                    </div>
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item"><a class="nav-link " href="/category/2-player.html">2-Player</a></li>
                        <li class="nav-item"><a class="nav-link " href="/category/3d.html">3D</a></li>
                        <li class="nav-item"><a class="nav-link " href="/category/adventure.html">Adventure</a></li>
                        <li class="nav-item"><a class="nav-link " href="/category/car.html">Car</a></li>
                        <li class="nav-item"><a class="nav-link " href="/category/moto.html">Moto</a></li>
                        <li class="nav-item"><a class="nav-link " href="/category/multiplayer.html">Multiplayer</a></li>
                        <li class="nav-item dropdown"><a class="dropdown-toggle nav-link" aria-expanded="false"
                                data-bs-toggle="dropdown" href="#">More</a>
                            <div class="dropdown-menu">
                                <a class="dropdown-item " href="/category/puzzle.html">Puzzle</a>
                                <a class="dropdown-item " href="/category/racing.html">Racing</a>
                                <a class="dropdown-item " href="/category/running.html">Running</a>
                                <a class="dropdown-item " href="/category/shooting.html">Shooting</a>
                                <a class="dropdown-item " href="/category/skill.html">Skill</a>
                                <a class="dropdown-item " href="/category/sports.html">Sports</a>
                                <a class="dropdown-item " href="/category/stickman.html">Stickman</a>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>
    <main>
        <div class="container">
            <h1 class="text-center">$h1Title</h1>
            
            <div class="main-content">
                <div class="game-main">
                    <div class="game-container">
                        <iframe class="game-iframe" id="gameFrame" 
                            src="$iframeSrc"
                            scrolling="no" frameborder="0" title="$h1Title Game"></iframe>
                    </div>

                    <div class="bt-fullscreen text-center mt-3"><button class="btn btn-primary btn-full" type="button"
                            onclick="openFullscreen();" aria-label="Play Fullscreen">FullScreen</button></div>
                    <div class="text-center mt-2"><a href="#" class="text-decoration-none">Play $h1Title - Latest Version</a></div>
                    <div class="row">
                        <p>Play $h1Title instantly in fullscreen browser, no downloads, no ads. Explore and enjoy various gaming
                            experiences now!</p>
                    </div>
                </div>
                
                <div class="sidebar">
                    <h3 class="sidebar-title">Recommended Games</h3>
                    
                    <div class="recommended-games">
                        <a href="./crossy-road.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/crossy-road.jpg" alt="Crossy Road">
                            <div class="recommended-game-info">
                                <h4>Crossy Road</h4>
                                <p>Casual • Adventure</p>
                            </div>
                        </a>
                        
                        <a href="./stick-merge.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/stick-merge.jpg" alt="Stick Merge">
                            <div class="recommended-game-info">
                                <h4>Stick Merge</h4>
                                <p>Casual • Strategy</p>
                            </div>
                        </a>
                        
                        <a href="./vex-7.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/vex-7.jpg" alt="Vex 7">
                            <div class="recommended-game-info">
                                <h4>Vex 7</h4>
                                <p>Platformer • Skill</p>
                            </div>
                        </a>
                        
                        <a href="./bitlife.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/bitlife.jpg" alt="BitLife">
                            <div class="recommended-game-info">
                                <h4>BitLife</h4>
                                <p>Simulation • Life</p>
                            </div>
                        </a>
                        
                        <a href="./fnaf.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/fnaf.jpg" alt="FNAF">
                            <div class="recommended-game-info">
                                <h4>FNAF</h4>
                                <p>Horror • Strategy</p>
                            </div>
                        </a>
                        
                        <a href="./eggy-car.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/eggy-car.jpg" alt="Eggy Car">
                            <div class="recommended-game-info">
                                <h4>Eggy Car</h4>
                                <p>Racing • Skills</p>
                            </div>
                        </a>
                        
                        <a href="./drift-hunters.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/drift-hunters.jpg" alt="Drift Hunters">
                            <div class="recommended-game-info">
                                <h4>Drift Hunters</h4>
                                <p>Racing • 3D</p>
                            </div>
                        </a>
                        
                        <a href="./monkey-mart.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/monkey-mart.jpg" alt="Monkey Mart">
                            <div class="recommended-game-info">
                                <h4>Monkey Mart</h4>
                                <p>Simulation • Casual</p>
                            </div>
                        </a>
                        
                        <a href="./papa-louie.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/papa-louie.jpg" alt="Papa Louie">
                            <div class="recommended-game-info">
                                <h4>Papa Louie</h4>
                                <p>Simulation • Cooking</p>
                            </div>
                        </a>
                        
                        <a href="./soccer-skills.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/soccer-skills.jpg" alt="Soccer Skills">
                            <div class="recommended-game-info">
                                <h4>Soccer Skills</h4>
                                <p>Sports • Skill</p>
                            </div>
                        </a>
                        
                        <a href="./snow-rider-3d.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/snow-rider-3d.jpg" alt="Snow Rider 3D">
                            <div class="recommended-game-info">
                                <h4>Snow Rider 3D</h4>
                                <p>Racing • 3D</p>
                            </div>
                        </a>
                        
                        <a href="./tunnel-rush.html" class="recommended-game">
                            <img src="${relativePath}assets/upload/games66ez/jpg/tunnel-rush.jpg" alt="Tunnel Rush">
                            <div class="recommended-game-info">
                                <h4>Tunnel Rush</h4>
                                <p>3D • Skill</p>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </main>
    
    <script>
        function openFullscreen() {
            var elem = document.getElementById("gameFrame");
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.webkitRequestFullscreen) { /* Safari */
                elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) { /* IE11 */
                elem.msRequestFullscreen();
            }
        }
    </script>
    <script src="${relativePath}assets/bootstrap/js/bootstrap.min.js"></script>
</body>

</html>
"@

        # Write the new content to the file
        Set-Content -Path $filePath -Value $newContent
        
        Write-Host "[$processed/$($gameFiles.Count)] Successfully processed: $($file.Name)" -ForegroundColor Green
        $successful++
    }
    catch {
        Write-Host "[$processed/$($gameFiles.Count)] ERROR processing: $($file.Name)" -ForegroundColor Red
        Write-Host "Error details: $_" -ForegroundColor Red
        $failed++
    }
}

# Display summary
Write-Host "`nTemplate application complete!" -ForegroundColor Green
Write-Host "Total files processed: $processed" -ForegroundColor Cyan
Write-Host "Successfully updated: $successful" -ForegroundColor Green
Write-Host "Failed to update: $failed" -ForegroundColor Red

if ($failed -gt 0) {
    Write-Host "`nSome files failed to update. You can restore using restore-from-backups.ps1" -ForegroundColor Yellow
} 