# Script để thêm game từ các nguồn WebGL khác

# Cấu hình encoding cho tiếng Việt
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Danh sách game theo danh mục
$gameCategories = @{
    "car" = @(
        @{
            name = "Drift Hunters"
            image = "drift-hunters.jpg"
            iframe = "https://webglmath.github.io/drift-hunters/"
        },
        @{
            name = "Madalin Stunt Cars 3"
            image = "madalin-stunt-cars-3.jpg"
            iframe = "https://webglmath.github.io/madalin-stunt-cars-3/"
        },
        @{
            name = "Highway Racer 3D"
            image = "highway-racer-3d.jpg"
            iframe = "https://webglmath.github.io/highway-racer-3d/"
        },
        @{
            name = "Parking Fury"
            image = "parking-fury.jpg"
            iframe = "https://ubg98.github.io/ParkingFury/"
        },
        @{
            name = "Parking Fury 2"
            image = "parking-fury-2.jpg"
            iframe = "https://ubg98.github.io/ParkingFury2/"
        },
        @{
            name = "Parking Fury 3"
            image = "parking-fury-3.jpg"
            iframe = "https://ubg98.github.io/ParkingFury3/"
        },
        @{
            name = "Park Out"
            image = "park-out.jpg"
            iframe = "https://ubg98.github.io/ParkOut/"
        },
        @{
            name = "Neon Racer"
            image = "neon-racer.jpg"
            iframe = "https://neonracergame.github.io/"
        },
        @{
            name = "Neon Biker"
            image = "neon-biker.jpg"
            iframe = "https://neonbikergame.github.io/"
        },
        @{
            name = "Highway Rider Extreme"
            image = "highway-rider-extreme.jpg"
            iframe = "https://highwayriderextreme.github.io/"
        },
        @{
            name = "Moto X3M"
            image = "moto-x3m.jpg"
            iframe = "https://motox3munblocked.github.io/"
        },
        @{
            name = "Moto X3M 2"
            image = "moto-x3m-2.jpg"
            iframe = "https://motox3munblocked.github.io/2/"
        },
        @{
            name = "Moto X3M 4 Winter"
            image = "moto-x3m-4-winter.jpg"
            iframe = "https://motox3munblocked.github.io/4-winter/"
        },
        @{
            name = "Moto X3M 5 Pool Party"
            image = "moto-x3m-5-pool-party.jpg"
            iframe = "https://motox3munblocked.github.io/5-pool-party/"
        },
        @{
            name = "Moto X3M 6 Spooky Land"
            image = "moto-x3m-6-spooky-land.jpg"
            iframe = "https://motox3munblocked.github.io/6-spooky-land/"
        }
    )

    "fighting" = @(
        @{
            name = "Iron Snout"
            image = "iron-snout.png"
            iframe = "https://webglmath.github.io/iron-snout/"
        },
        @{
            name = "Stickman Fighter Epic Battles"
            image = "stickman-fighter-epic-battles.png"
            iframe = "https://stickmanfightergame.github.io/"
        }
    )

    "sports" = @(
        @{
            name = "Basketball Stars"
            image = "basketball-stars.jpg"
            iframe = "https://webglmath.github.io/basketball-stars/"
        },
        @{
            name = "Basketball Legends"
            image = "basketball-legends.jpg"
            iframe = "https://webglmath.github.io/basketball-legends/"
        },
        @{
            name = "Football Legends"
            image = "football-legends.jpg"
            iframe = "https://webglmath.github.io/football-legends/"
        },
        @{
            name = "Super Liquid Soccer"
            image = "super-liquid-soccer.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        },
        @{
            name = "Penalty Kick Online"
            image = "penalty-kick-online.jpg"
            iframe = "https://ubg98.github.io/PenaltyKickOnline/"
        },
        @{
            name = "Infinite Soccer"
            image = "infinite-soccer.jpg"
            iframe = "https://ubg98.github.io/InfiniteSoccer/"
        },
        @{
            name = "Head Soccer 2023"
            image = "head-soccer-2023.jpg"
            iframe = "https://ubg98.github.io/HeadSoccer2023/"
        },
        @{
            name = "Heads Arena Soccer All Stars"
            image = "heads-arena-soccer-all-stars.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        }
    )

    "adventure" = @(
        @{
            name = "Red Ball 4"
            image = "red-ball-4.jpg"
            iframe = "https://redballunblocked.github.io/4/"
        },
        @{
            name = "Super Mario Wonder"
            image = "super-mario-wonder.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        },
        @{
            name = "Monkey Mart"
            image = "monkey-mart.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        },
        @{
            name = "Raft Wars"
            image = "raft-wars.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        },
        @{
            name = "Raft Wars 2"
            image = "raft-wars-2.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        }
    )

    "skill" = @(
        @{
            name = "Stack"
            image = "stack.jpg"
            iframe = "https://webglmath.github.io/stack/"
        },
        @{
            name = "Slope"
            image = "slope.jpg"
            iframe = "https://webglmath.github.io/slope/"
        },
        @{
            name = "Slope City"
            image = "slope-city.jpg"
            iframe = "https://webglmath.github.io/slope-city/"
        },
        @{
            name = "Vex 3"
            image = "vex-3.jpg"
            iframe = "https://ubg98.github.io/Vex3/"
        },
        @{
            name = "Vex 4"
            image = "vex-4.jpg"
            iframe = "https://ubg98.github.io/Vex4/"
        },
        @{
            name = "Vex 5"
            image = "vex-5.jpg"
            iframe = "https://ubg98.github.io/Vex5/"
        },
        @{
            name = "Vex 6"
            image = "vex-6.jpg"
            iframe = "https://ubg98.github.io/Vex6/"
        },
        @{
            name = "Vex 7"
            image = "vex-7.jpg"
            iframe = "https://ubg98.github.io/Vex7/"
        },
        @{
            name = "Vex 8"
            image = "vex-8.jpg"
            iframe = "https://ubg98.github.io/Vex8/"
        },
        @{
            name = "World's Hardest Game"
            image = "worlds-hardest-game.jpg"
            iframe = "https://ubg98.github.io/WorldsHardestGame/"
        }
    )

    "action" = @(
        @{
            name = "Iron Snout"
            image = "iron-snout.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        },
        @{
            name = "Getaway Shootout"
            image = "getaway-shootout.jpg"
            iframe = "https://webglmath.github.io/getaway-shootout/"
        },
        @{
            name = "Rooftop Snipers"
            image = "rooftop-snipers.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        },
        @{
            name = "Run 3"
            image = "run-3.jpg"
            iframe = "https://ubg98.github.io/Run3/"
        },
        @{
            name = "Subway Surfers"
            image = "subway-surfers.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        },
        @{
            name = "Ninja Cat Exploit"
            image = "ninja-cat-exploit.jpg"
            iframe = "https://ubg98.github.io/NinjaCatExploit/"
        },
        @{
            name = "Mr Bullet"
            image = "mr-bullet.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        },
        @{
            name = "Mr Bullet 3D"
            image = "mr-bullet-3d.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        },
        @{
            name = "Stickman Hook"
            image = "stickman-hook.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        }
    )

    "puzzle" = @(
        @{
            name = "Snail Bob"
            image = "snail-bob.jpg"
            iframe = "https://ubg98.github.io/SnailBob/"
        },
        @{
            name = "Snail Bob 2"
            image = "snail-bob-2.jpg"
            iframe = "https://ubg98.github.io/SnailBob2/"
        },
        @{
            name = "Snail Bob 3"
            image = "snail-bob-3.jpg"
            iframe = "https://ubg98.github.io/SnailBob3/"
        },
        @{
            name = "Snail Bob 4"
            image = "snail-bob-4.jpg"
            iframe = "https://ubg98.github.io/SnailBob4/"
        },
        @{
            name = "Snail Bob 5"
            image = "snail-bob-5.jpg"
            iframe = "https://ubg98.github.io/SnailBob5/"
        },
        @{
            name = "Snail Bob 6"
            image = "snail-bob-6.jpg"
            iframe = "https://ubg98.github.io/SnailBob6/"
        },
        @{
            name = "Snail Bob 7"
            image = "snail-bob-7.jpg"
            iframe = "https://ubg98.github.io/SnailBob7/"
        },
        @{
            name = "Snail Bob 8"
            image = "snail-bob-8.jpg"
            iframe = "https://ubg98.github.io/SnailBob8/"
        },
        @{
            name = "Wood Block Puzzle"
            image = "wood-block-puzzle.jpg"
            iframe = "https://ubg98.github.io/WoodBlockPuzzle/"
        },
        @{
            name = "Pudding Monsters"
            image = "pudding-monsters.jpg"
            iframe = "https://ubg98.github.io/PuddingMonsters/"
        },
        @{
            name = "Marbles Sorting"
            image = "marbles-sorting.jpg"
            iframe = "https://ubg98.github.io/MarblesSorting/"
        }
    )

    "idle" = @(
        @{
            name = "Idle Breakout"
            image = "idle-breakout.jpg"
            iframe = "https://ubg98.github.io/IdleBreakout/"
        },
        @{
            name = "Idle Mining Empire"
            image = "idle-mining-empire.jpg"
            iframe = "https://ubg98.github.io/IdleMiningEmpire/"
        },
        @{
            name = "Idle Restaurants"
            image = "idle-restaurants.jpg"
            iframe = "https://ubg98.github.io/IdleRestaurants/"
        }
    )

    "classic" = @(
        @{
            name = "Pacman HTML5"
            image = "pacman-html5.jpg"
            iframe = "https://ubg98.github.io/ubg98/"
        },
        @{
            name = "Spider Solitaire"
            image = "spider-solitaire.jpg"
            iframe = "https://spidersolitaireunblocked.github.io/"
        },
        @{
            name = "Klondike Solitaire"
            image = "klondike-solitaire.jpg"
            iframe = "https://klondikesolitaire.github.io/"
        }
    )
} 

# Template cho game HTML
$gameTemplate = @'
<!DOCTYPE html>
<html data-bs-theme="light" lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>{0} - Play AT Monkey Mart One</title>
    <meta name="description" content="{1}">
    <link rel="stylesheet" href="../assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="../assets/fonts/font-awesome.min.css">
    <link rel="stylesheet" href="../assets/css/Navbar-Right-Links-icons.css">
    <link rel="stylesheet" href="../assets/css/styles.css">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="/index.html">
</head>
<body>
    <nav class="navbar navbar-expand-md bg-body py-3">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center" href="/"><span class="bs-icon-sm bs-icon-rounded bs-icon-primary d-flex justify-content-center align-items-center me-2 bs-icon"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-bezier">
                        <path fill-rule="evenodd" d="M0 10.5A1.5 1.5 0 0 1 1.5 9h1A1.5 1.5 0 0 1 4 10.5v1A1.5 1.5 0 0 1 2.5 13h-1A1.5 1.5 0 0 1 0 11.5v-1zm1.5-.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1zm10.5.5A1.5 1.5 0 0 1 13.5 9h1a1.5 1.5 0 0 1 1.5 1.5v1a1.5 1.5 0 0 1-1.5 1.5h-1a1.5 1.5 0 0 1-1.5-1.5v-1zm1.5-.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1zM6 4.5A1.5 1.5 0 0 1 7.5 3h1A1.5 1.5 0 0 1 10 4.5v1A1.5 1.5 0 0 1 8.5 7h-1A1.5 1.5 0 0 1 6 5.5v-1zM7.5 4a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1z"></path>
                        <path d="M6 4.5H1.866a1 1 0 1 0 0 1h2.668A6.517 6.517 0 0 0 1.814 9H2.5c.123 0 .244.015.358.043a5.517 5.517 0 0 1 3.185-3.185A1.503 1.503 0 0 1 6 5.5v-1zm3.957 1.358A1.5 1.5 0 0 0 10 5.5v-1h4.134a1 1 0 1 1 0 1h-2.668a6.517 6.517 0 0 1 2.72 3.5H13.5c-.123 0-.243.015-.358.043a5.517 5.517 0 0 0-3.185-3.185z"></path>
                    </svg></span><span>Monkey Mart One</span></a><button data-bs-toggle="collapse" class="navbar-toggler" data-bs-target="#navcol-2"><span class="visually-hidden">Toggle navigation</span><span class="navbar-toggler-icon"></span></button>
            <div class="collapse navbar-collapse" id="navcol-2">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link active" href="/">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/car.html">Car</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/skill.html">Skill</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/action.html">Action</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/sports.html">Sports</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/racing.html">Racing</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/puzzle.html">Puzzle</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="container">
        <div class="gameFrame">
            <h1 class="text-center">{0}</h1>
            <div class="game-container">
                <iframe class="game-iframe" id="gameFrame" src="{2}" style="background:black;" width="100%" height="600" scrolling="no" frameborder="0"></iframe>
            </div>
            <div class="bt-fullscreen text-center">
                <button class="btn btn-primary btn-full" type="button" onclick="openFullscreen();">FullScreen</button>
            </div>
        </div>
    </div>
    <script src="../assets/bootstrap/js/bootstrap.min.js"></script>
</body>
</html>
'@

# Hàm tạo game HTML
function Create-GameFile {
    param (
        [string]$name,
        [string]$iframe,
        [string]$description,
        [string]$category
    )
    
    $safeName = $name.ToLower() -replace '\s+', '-'
    $filePath = "game/$safeName.html"
    
    $gameContent = $gameTemplate -f $name, $description, $iframe
    $gameContent | Out-File -FilePath $filePath -Encoding UTF8
    
    Write-Host "Đã tạo file game: $filePath" -ForegroundColor Green
    
    # Thêm game vào trang danh mục
    $categoryFile = "category/$category.html"
    if (Test-Path $categoryFile) {
        $content = Get-Content $categoryFile -Raw
        
        # Tạo HTML cho game item
        $gameItem = @"
        <div class="col-sm-6 col-md-4 col-lg-2 game-item">
            <a class="game-link" href="/game/$safeName.html">
                <img class="img-fluid game-card__cover" src="../assets/img/img-slope/$($safeName).jpg">
                <h3 class="game-card__title" style="font-size: 15px;">$name</h3>
            </a>
        </div>
"@
        
        # Thêm vào trước </div> cuối cùng
        $content = $content -replace '</div>\s*</div>\s*</div>\s*$', "$gameItem`n</div></div></div>"
        $content | Set-Content $categoryFile -Force
        
        Write-Host "Đã thêm game vào danh mục $category" -ForegroundColor Green
    }
}

# Tạo game cho từng danh mục
foreach ($category in $gameCategories.Keys) {
    Write-Host "`nĐang thêm game vào danh mục $category..." -ForegroundColor Yellow
    
    foreach ($game in $gameCategories[$category]) {
        Create-GameFile -name $game.name -iframe $game.iframe -description $game.description -category $category
    }
}

Write-Host "`nHoàn tất thêm game!" -ForegroundColor Green 