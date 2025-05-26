$files = Get-ChildItem -Path "game" -Filter "*.html"
$headerContent = @"
    <div class="main-wrapper">
      <header class="header">
        <div class="container">
          <div class="header-content">
            <div class="logo">
              <a href="/">
                <img src="../assets/img/monkey-mart.jpg" alt="Monkey Mart Logo">
              </a>
            </div>
            <nav class="nav-menu">
              <ul>
                <li><a href="/" title="Monkey Mart"><i class="fas fa-home"></i> Home</a></li>
                <li><a href="../category/game.html" title="Tất Cả Game Tại Monkey Mart"><i class="fas fa-gamepad"></i> All Games</a></li>
                <li><a href="../category/play-more.html"><i class="fas fa-cogs"></i> Play More</a></li>
              </ul>
            </nav>
          </div>
        </div>
      </header>
      
      <main class="main-content">
"@

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $newContent = $content -replace '<button class="menu-toggle".*?<div class="main-wrapper">', '<div class="main-wrapper">'
    $newContent = $newContent -replace '<header class="header">.*?<main class="main-content">', $headerContent
    $newContent | Set-Content $file.FullName -Force
} 