<?php
// Cấu hình
$gameUpDir = './game/game-up/'; // Thư mục chứa trang chi tiết game
$imageUpDir = './assets/img/img-up/'; // Thư mục chứa hình ảnh game
$hotGamesFile = './game-hot-wg.html'; // File chứa danh sách game nóng

// Kiểm tra xem người dùng có submit form không
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = isset($_POST['action']) ? $_POST['action'] : '';
    
    if ($action === 'add_single') {
        // Thêm một game
        $gameName = isset($_POST['game_name']) ? $_POST['game_name'] : '';
        $gameDesc = isset($_POST['game_description']) ? $_POST['game_description'] : '';
        $gameIframe = isset($_POST['game_iframe']) ? $_POST['game_iframe'] : '';
        $gameCategory = isset($_POST['game_category']) ? $_POST['game_category'] : '';
        $gameImageExt = isset($_POST['game_image_ext']) ? $_POST['game_image_ext'] : 'png';
        
        if (empty($gameName) || empty($gameIframe) || empty($gameCategory)) {
            echo json_encode(['success' => false, 'message' => 'Vui lòng điền đầy đủ thông tin bắt buộc (Tên, iframe URL, và Category)']);
            exit;
        }
        
        $gameData = [
            'name' => $gameName,
            'description' => $gameDesc,
            'iframe' => $gameIframe,
            'category' => $gameCategory,
            'imageExt' => $gameImageExt
        ];
        
        $result = addGame($gameData);
        echo json_encode($result);
        exit;
    } 
    else if ($action === 'add_bulk') {
        // Thêm nhiều game
        $bulkGames = isset($_POST['bulk_games']) ? $_POST['bulk_games'] : '';
        
        if (empty($bulkGames)) {
            echo json_encode(['success' => false, 'message' => 'Vui lòng cung cấp dữ liệu JSON']);
            exit;
        }
        
        try {
            $games = json_decode($bulkGames, true);
            
            if (!is_array($games)) {
                echo json_encode(['success' => false, 'message' => 'Định dạng không hợp lệ. Vui lòng sử dụng mảng các đối tượng game']);
                exit;
            }
            
            $invalidEntries = [];
            $addedCount = 0;
            
            foreach ($games as $index => $game) {
                if (empty($game['name']) || empty($game['iframe']) || empty($game['category'])) {
                    $invalidEntries[] = 'Game tại index ' . $index . ' (' . (isset($game['name']) ? $game['name'] : 'Không tên') . ')';
                    continue;
                }
                
                $gameData = [
                    'name' => $game['name'],
                    'description' => isset($game['description']) ? $game['description'] : '',
                    'iframe' => $game['iframe'],
                    'category' => $game['category'],
                    'imageExt' => isset($game['imageExt']) ? $game['imageExt'] : 'png'
                ];
                
                $result = addGame($gameData);
                if ($result['success']) {
                    $addedCount++;
                } else {
                    $invalidEntries[] = 'Game tại index ' . $index . ' (' . $game['name'] . '): ' . $result['message'];
                }
            }
            
            if (count($invalidEntries) > 0) {
                echo json_encode([
                    'success' => true,
                    'message' => 'Đã thêm ' . $addedCount . ' game. Các mục sau không hợp lệ: ' . implode(', ', $invalidEntries)
                ]);
            } else {
                echo json_encode(['success' => true, 'message' => 'Tất cả ' . $addedCount . ' game đã được thêm thành công!']);
            }
            
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'message' => 'Lỗi phân tích dữ liệu JSON: ' . $e->getMessage()]);
        }
        exit;
    }
    else if ($action === 'upload_excel') {
        // Xử lý upload file Excel
        if (!isset($_FILES['excel_file']) || $_FILES['excel_file']['error'] != UPLOAD_ERR_OK) {
            echo json_encode(['success' => false, 'message' => 'Lỗi upload file. Vui lòng thử lại.']);
            exit;
        }

        $file = $_FILES['excel_file']['tmp_name'];
        $fileType = pathinfo($_FILES['excel_file']['name'], PATHINFO_EXTENSION);

        // Kiểm tra loại file: chỉ chấp nhận .xlsx, .xls hoặc .csv
        $ft = strtolower($fileType);
        if (!in_array($ft, ['xlsx', 'xls', 'csv'])) {
            echo json_encode(['success' => false, 'message' => 'Chỉ chấp nhận file Excel (.xlsx, .xls) hoặc CSV (.csv)']);
            exit;
        }

        // Nếu là CSV, xử lý trực tiếp qua fgetcsv
        if ($ft === 'csv') {
            $games = [];
            if (($handle = fopen($file, 'r')) !== false) {
                $headerRow = true;
                while (($data = fgetcsv($handle, 1000, ',', '"', '\\')) !== false) {
                    if ($headerRow) { $headerRow = false; continue; }
                    if (count($data) >= 3) {
                        $gameName = trim($data[0]);
                        $gameDesc = trim($data[1]);
                        $gameIframe = trim($data[2]);
                        $gameCategory = isset($data[3]) ? trim($data[3]) : '';
                        $gameImageExt = isset($data[4]) && trim($data[4]) !== '' ? trim($data[4]) : 'png';
                        if (empty($gameName) || empty($gameIframe) || empty($gameCategory)) { continue; }
                        $games[] = [
                            'name' => $gameName,
                            'description' => $gameDesc,
                            'iframe' => $gameIframe,
                            'category' => $gameCategory,
                            'imageExt' => $gameImageExt
                        ];
                    }
                }
                fclose($handle);
                $invalidEntries = [];
                $addedCount = 0;
                foreach ($games as $index => $game) {
                    $result = addGame($game);
                    if ($result['success']) {
                        $addedCount++;
                    } else {
                        $invalidEntries[] = 'Game tại dòng ' . ($index + 2) . ' (' . $game['name'] . '): ' . $result['message'];
                    }
                }
                if (count($invalidEntries) > 0) {
                    echo json_encode(['success' => true, 'message' => 'Đã thêm ' . $addedCount . ' game từ CSV. Các mục không hợp lệ: ' . implode(', ', $invalidEntries)]);
                } else {
                    echo json_encode(['success' => true, 'message' => 'Tất cả ' . $addedCount . ' game từ CSV đã được thêm thành công!']);
                }
            } else {
                echo json_encode(['success' => false, 'message' => 'Không thể đọc file CSV']);
            }
            exit;
        }
        // Với các file Excel (.xlsx, .xls), tiếp tục xử lý với PhpSpreadsheet
        try {
            // Load the PhpSpreadsheet library (PHP 7+) using simple file inclusion
            // Lưu ý: Bạn cần cài đặt thư viện PhpSpreadsheet trước bằng Composer
            // composer require phpoffice/phpspreadsheet
            if (file_exists('vendor/autoload.php')) {
                require 'vendor/autoload.php';
                
                // Sử dụng PhpSpreadsheet để đọc file Excel
                $spreadsheet = \PhpOffice\PhpSpreadsheet\IOFactory::load($file);
                $sheet = $spreadsheet->getActiveSheet();
                $highestRow = $sheet->getHighestRow();
                
                // Lấy dữ liệu từ file Excel
                $games = [];
                $headerRow = true;
                
                // Thứ tự cột trong Excel: Tên Game, Mô tả, iframe URL, Category, Image Extension
                for ($row = 1; $row <= $highestRow; $row++) {
                    // Bỏ qua hàng đầu tiên (tiêu đề)
                    if ($headerRow) {
                        $headerRow = false;
                        continue;
                    }
                    
                    $gameName = $sheet->getCellByColumnAndRow(1, $row)->getValue();
                    $gameDesc = $sheet->getCellByColumnAndRow(2, $row)->getValue();
                    $gameIframe = $sheet->getCellByColumnAndRow(3, $row)->getValue();
                    $gameCategory = $sheet->getCellByColumnAndRow(4, $row)->getValue();
                    $gameImageExt = $sheet->getCellByColumnAndRow(5, $row)->getValue();
                    
                    // Kiểm tra dữ liệu hợp lệ
                    if (empty($gameName) || empty($gameIframe) || empty($gameCategory)) {
                        continue; // Bỏ qua các dòng không có dữ liệu đầy đủ
                    }
                    
                    $games[] = [
                        'name' => $gameName,
                        'description' => $gameDesc,
                        'iframe' => $gameIframe,
                        'category' => $gameCategory,
                        'imageExt' => !empty($gameImageExt) ? $gameImageExt : 'png'
                    ];
                }
                
                // Thêm các game từ Excel vào hệ thống
                $invalidEntries = [];
                $addedCount = 0;
                
                foreach ($games as $index => $game) {
                    $gameData = [
                        'name' => $game['name'],
                        'description' => $game['description'],
                        'iframe' => $game['iframe'],
                        'category' => $game['category'],
                        'imageExt' => $game['imageExt']
                    ];
                    
                    $result = addGame($gameData);
                    if ($result['success']) {
                        $addedCount++;
                    } else {
                        $invalidEntries[] = 'Game tại dòng ' . ($index + 2) . ' (' . $game['name'] . '): ' . $result['message'];
                    }
                }
                
                if (count($invalidEntries) > 0) {
                    echo json_encode([
                        'success' => true,
                        'message' => 'Đã thêm ' . $addedCount . ' game từ Excel. Các mục sau không hợp lệ: ' . implode(', ', $invalidEntries)
                    ]);
                } else {
                    echo json_encode(['success' => true, 'message' => 'Tất cả ' . $addedCount . ' game từ Excel đã được thêm thành công!']);
                }
            } else {
                echo json_encode(['success' => false, 'message' => 'Thư viện PhpSpreadsheet không có sẵn. Vui lòng cài đặt hoặc sử dụng định dạng CSV thay thế.']);
            }
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'message' => 'Lỗi xử lý file Excel: ' . $e->getMessage()]);
        }
        exit;
    }
}

/**
 * Thêm một game mới
 * 
 * @param array $gameData Dữ liệu của game
 * @return array Kết quả xử lý
 */
function addGame($gameData) {
    global $gameUpDir, $imageUpDir, $hotGamesFile;
    
    // Tạo slug từ tên game
    $slug = createSlug($gameData['name']);
    
    // Tạo trang chi tiết game
    $gamePageFile = $gameUpDir . $slug . '.html';
    $gamePageContent = generateGamePage($gameData, $slug);
    
    // Lưu trang chi tiết game
    if (!file_put_contents($gamePageFile, $gamePageContent)) {
        return ['success' => false, 'message' => 'Không thể tạo trang chi tiết game'];
    }
    
    // Thêm game vào danh sách game nóng
    if (!addGameToHotList($gameData, $slug)) {
        return ['success' => false, 'message' => 'Không thể thêm game vào danh sách game nóng'];
    }
    
    return ['success' => true, 'message' => 'Game đã được thêm thành công!', 'slug' => $slug];
}

/**
 * Tạo slug từ tên game
 * 
 * @param string $name Tên game
 * @return string Slug
 */
function createSlug($name) {
    // Chuyển đổi sang chữ thường và loại bỏ dấu tiếng Việt
    $slug = strtolower($name);
    $slug = removeVietnameseAccents($slug);
    
    // Loại bỏ các ký tự đặc biệt
    $slug = preg_replace('/[^\w\s-]/', '', $slug);
    
    // Thay thế khoảng trắng bằng dấu gạch ngang
    $slug = preg_replace('/\s+/', '-', $slug);
    
    // Loại bỏ các dấu gạch ngang liên tiếp
    $slug = preg_replace('/-+/', '-', $slug);
    
    // Cắt bỏ khoảng trắng hoặc dấu gạch ngang ở đầu và cuối
    $slug = trim($slug, '-');
    
    return $slug;
}

/**
 * Loại bỏ dấu tiếng Việt
 * 
 * @param string $str Chuỗi cần xử lý
 * @return string Chuỗi đã xử lý
 */
function removeVietnameseAccents($str) {
    $str = preg_replace("/(à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ)/", 'a', $str);
    $str = preg_replace("/(è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ)/", 'e', $str);
    $str = preg_replace("/(ì|í|ị|ỉ|ĩ)/", 'i', $str);
    $str = preg_replace("/(ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ)/", 'o', $str);
    $str = preg_replace("/(ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ)/", 'u', $str);
    $str = preg_replace("/(ỳ|ý|ỵ|ỷ|ỹ)/", 'y', $str);
    $str = preg_replace("/(đ)/", 'd', $str);
    $str = preg_replace("/(À|Á|Ạ|Ả|Ã|Â|Ầ|Ấ|Ậ|Ẩ|Ẫ|Ă|Ằ|Ắ|Ặ|Ẳ|Ẵ)/", 'A', $str);
    $str = preg_replace("/(È|É|Ẹ|Ẻ|Ẽ|Ê|Ề|Ế|Ệ|Ể|Ễ)/", 'E', $str);
    $str = preg_replace("/(Ì|Í|Ị|Ỉ|Ĩ)/", 'I', $str);
    $str = preg_replace("/(Ò|Ó|Ọ|Ỏ|Õ|Ô|Ồ|Ố|Ộ|Ổ|Ỗ|Ơ|Ờ|Ớ|Ợ|Ở|Ỡ)/", 'O', $str);
    $str = preg_replace("/(Ù|Ú|Ụ|Ủ|Ũ|Ư|Ừ|Ứ|Ự|Ử|Ữ)/", 'U', $str);
    $str = preg_replace("/(Ỳ|Ý|Ỵ|Ỷ|Ỹ)/", 'Y', $str);
    $str = preg_replace("/(Đ)/", 'D', $str);
    return $str;
}

/**
 * Tạo nội dung trang chi tiết game
 * 
 * @param array $gameData Dữ liệu của game
 * @param string $slug Slug của game
 * @return string Nội dung HTML của trang chi tiết game
 */
function generateGamePage($gameData, $slug) {
    $gameName = $gameData['name'];
    $gameDesc = $gameData['description'] ? $gameData['description'] : $gameName . ' - Play this amazing game online for free!';
    $gameIframe = $gameData['iframe'];
    
    return '<!DOCTYPE html>
<html data-bs-theme="light" lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <link rel="dns-prefetch" href="https://universal.wgplayer.com"/><script type="text/javascript" async>!function(e,t){a=e.createElement("script"),m=e.getElementsByTagName("script")[0],a.async=1,a.src=t,a.fetchPriority='high',m.parentNode.insertBefore(a,m)}(document,"https://universal.wgplayer.com/tag/?lh="+window.location.hostname+"&wp="+window.location.pathname+"&ws="+window.location.search);</script>
    <title>' . $gameName . ' - Play Online for Free!</title>
    <meta name="description" content="' . $gameDesc . '">
    <link rel="stylesheet" href="../../assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="../../assets/fonts/font-awesome.min.css">
    <link rel="stylesheet" href="../../assets/css/Navbar-Right-Links-icons.css">
    <link rel="stylesheet" href="../../assets/css/styles.css">
    <style>
        .game-iframe {
            max-width: 100%;
            border: none;
            background: black;
        }
        .btn-full {
            margin: 15px 0;
        }
    </style>
</head>

<body>
    <header id="header" class="sticky-top">
        <nav class="navbar navbar-expand-lg py-3">
            <div class="container"><a class="navbar-brand d-flex align-items-center" href="../../index.html"><img
                        src="../../assets/img/logo.png" alt="Website Logo" style="height:40px"></a><button data-bs-toggle="collapse"
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
                        <li class="nav-item"><a class="nav-link" href="../../category/2-player.html">2-Player</a></li>
                        <li class="nav-item"><a class="nav-link" href="../../category/3d.html">3D</a></li>
                        <li class="nav-item"><a class="nav-link" href="../../category/adventure.html">Adventure</a></li>
                        <li class="nav-item"><a class="nav-link" href="../../category/car.html">Car</a></li>
                        <li class="nav-item"><a class="nav-link" href="../../category/moto.html">Moto</a></li>
                        <li class="nav-item"><a class="nav-link" href="../../category/multiplayer.html">Multiplayer</a></li>
                        <li class="nav-item dropdown"><a class="dropdown-toggle nav-link" aria-expanded="false"
                                data-bs-toggle="dropdown" href="#">More</a>
                            <div class="dropdown-menu">
                                <a class="dropdown-item" href="../../category/puzzle.html">Puzzle</a>
                                <a class="dropdown-item" href="../../category/racing.html">Racing</a>
                                <a class="dropdown-item" href="../../category/running.html">Running</a>
                                <a class="dropdown-item" href="../../category/shooting.html">Shooting</a>
                                <a class="dropdown-item" href="../../category/skill.html">Skill</a>
                                <a class="dropdown-item" href="../../category/sports.html">Sports</a>
                                <a class="dropdown-item" href="../../category/stickman.html">Stickman</a>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>
    
    <main>
        <div class="container">
            <h1 class="text-center">Play ' . $gameName . '</h1>
            <div class="gameFrame">
                <div class="game-container">
                    <iframe class="game-iframe" id="gameFrame"
                        src="' . $gameIframe . '"
                        style="background:black;" width="100%" height="600" scrolling="no" frameborder="0" title="' . $gameName . ' Game"></iframe>
                </div>

                <div class="bt-fullscreen text-center"><button class="btn btn-primary btn-full" type="button"
                        onclick="openFullscreen();" aria-label="Play Fullscreen">FullScreen</button></div>
                <div class="text-center mt-2"><a href="../../game-hot-wg.html" class="text-decoration-none">Browse More Hot Games</a></div>
                <div class="row">
                    <p>' . $gameDesc . '</p>
                </div>
            </div>
        </div>
    </main>
    
    <footer>
        <div class="copyright">
            <div class="container">
                <span>Play Games for free!</span>
                <span style="float:right;">
                    <a href="/dmca/">DMCA</a></li>&nbsp;&nbsp;
                    <a href="/terms/">Terms</a></li>&nbsp;&nbsp;
                    <a href="/privacy/">Privacy</a></li>
                </span>
            </div>
        </div>
    </footer>
    
    <a class="go-top" href="#" aria-label="Go to top"><i class="fa fa-arrow-up"></i></a>
    <script src="../../assets/js/jquery.min.js"></script>
    <script src="../../assets/bootstrap/js/bootstrap.min.js"></script>
    <script src="../../assets/js/custom.js"></script>
    <script src="../../assets/js/search_v1_0.js"></script>
    
    <script>
        // Function to open the iframe in fullscreen
        function openFullscreen() {
            const iframe = document.getElementById("gameFrame");
            if (iframe.requestFullscreen) {
                iframe.requestFullscreen();
            } else if (iframe.mozRequestFullScreen) { // Firefox
                iframe.mozRequestFullScreen();
            } else if (iframe.webkitRequestFullscreen) { // Chrome, Safari and Opera
                iframe.webkitRequestFullscreen();
            } else if (iframe.msRequestFullscreen) { // IE/Edge
                iframe.msRequestFullscreen();
            }
        }
    </script>
</body>
</html>';
}

/**
 * Thêm game vào danh sách game nóng
 * 
 * @param array $gameData Dữ liệu của game
 * @param string $slug Slug của game
 * @return bool Kết quả xử lý
 */
function addGameToHotList($gameData, $slug) {
    global $hotGamesFile;
    
    // Kiểm tra xem file game-hot-wg.html đã tồn tại chưa
    if (!file_exists($hotGamesFile)) {
        // Tạo file mới nếu chưa tồn tại
        $hotGamesContent = createHotGamesFile();
        file_put_contents($hotGamesFile, $hotGamesContent);
    }
    
    // Đọc nội dung file
    $content = file_get_contents($hotGamesFile);
    
    // Thêm game vào danh sách
    $gameItem = '<div class="col-sm-6 col-md-4 col-lg-2 game-item">
                    <a class="game-link" href="./game/game-up/' . $slug . '.html">
                        <img class="img-fluid game-card__cover"
                            src="./assets/img/img-up/' . $slug . '.' . $gameData['imageExt'] . '" alt="' . $gameData['name'] . ' Game">
                        <h3 class="game-card__title">' . $gameData['name'] . '</h3>
                    </a>
                </div>';
    
    // Tìm vị trí để chèn game vào
    $gameListPos = strpos($content, '<!-- Game items will be added here dynamically -->');
    if ($gameListPos !== false) {
        // Chèn game vào sau comment
        $content = substr_replace($content, "\n                    " . $gameItem, $gameListPos + strlen('<!-- Game items will be added here dynamically -->'), 0);
        
        // Lưu nội dung mới vào file
        return file_put_contents($hotGamesFile, $content) !== false;
    }
    
    return false;
}

/**
 * Tạo nội dung cho file game-hot-wg.html
 * 
 * @return string Nội dung HTML
 */
function createHotGamesFile() {
    return '<!DOCTYPE html>
<html data-bs-theme="light" lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>Hot Games - Best Free Online Gaming Experience</title>
    <meta name="description" content="Explore our collection of hot games. Play now for free!">
    <link rel="stylesheet" href="./assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="./assets/fonts/font-awesome.min.css">
    <link rel="stylesheet" href="./assets/css/Navbar-Right-Links-icons.css">
    <link rel="stylesheet" href="./assets/css/styles.css">
    <style>
        /* Image display improvements */
        .game-card__cover {
            max-width: 100%;
            height: auto;
            display: block;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .game-card__cover:hover {
            transform: scale(1.05);
        }
        
        .game-item {
            margin-bottom: 20px;
        }
        
        .game-card__title {
            font-size: 15px;
            color: #333;
            margin-top: 10px;
            text-align: center;
        }
    </style>
</head>

<body>
    <header id="header" class="sticky-top">
        <nav class="navbar navbar-expand-lg py-3">
            <div class="container"><a class="navbar-brand d-flex align-items-center" href="./index.html"><img
                        src="./assets/img/logo.png" alt="Website Logo" style="height:40px"></a><button data-bs-toggle="collapse"
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
                        <li class="nav-item"><a class="nav-link" href="./category/2-player.html">2-Player</a></li>
                        <li class="nav-item"><a class="nav-link" href="./category/3d.html">3D</a></li>
                        <li class="nav-item"><a class="nav-link" href="./category/adventure.html">Adventure</a></li>
                        <li class="nav-item"><a class="nav-link" href="./category/car.html">Car</a></li>
                        <li class="nav-item"><a class="nav-link" href="./category/moto.html">Moto</a></li>
                        <li class="nav-item"><a class="nav-link" href="./category/multiplayer.html">Multiplayer</a></li>
                        <li class="nav-item dropdown"><a class="dropdown-toggle nav-link" aria-expanded="false"
                                data-bs-toggle="dropdown" href="#">More</a>
                            <div class="dropdown-menu">
                                <a class="dropdown-item" href="./category/puzzle.html">Puzzle</a>
                                <a class="dropdown-item" href="./category/racing.html">Racing</a>
                                <a class="dropdown-item" href="./category/running.html">Running</a>
                                <a class="dropdown-item" href="./category/shooting.html">Shooting</a>
                                <a class="dropdown-item" href="./category/skill.html">Skill</a>
                                <a class="dropdown-item" href="./category/sports.html">Sports</a>
                                <a class="dropdown-item" href="./category/stickman.html">Stickman</a>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>
    
    <main>
        <div class="container">
            <h1 class="text-center mb-4">Hot Games Collection</h1>
            
            <!-- Game List Section -->
            <div class="product-section">
                <div class="row">
                    <div class="col" style="flex:none">
                        <div class="heading">
                            <h2 class="title-sub">&nbsp;<strong>Hot</strong><span style="padding-left:5px">Games</span></h2>
                        </div>
                    </div>
                </div>
                
                <!-- Game list container -->
                <div class="row" id="game-list">
                    <!-- Game items will be added here dynamically -->
                </div>
            </div>
        </div>
    </main>
    
    <footer>
        <div class="copyright">
            <div class="container">
                <span>Play Games for free!</span>
                <span style="float:right;">
                    <a href="/dmca/">DMCA</a></li>&nbsp;&nbsp;
                    <a href="/terms/">Terms</a></li>&nbsp;&nbsp;
                    <a href="/privacy/">Privacy</a></li>
                </span>
            </div>
        </div>
    </footer>
    
    <a class="go-top" href="#" aria-label="Go to top"><i class="fa fa-arrow-up"></i></a>
    <script src="./assets/js/jquery.min.js"></script>
    <script src="./assets/bootstrap/js/bootstrap.min.js"></script>
    <script src="./assets/js/custom.js"></script>
    <script src="./assets/js/search_v1_0.js"></script>
</body>

</html>';
}
?>

<!DOCTYPE html>
<html data-bs-theme="light" lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>Add New Games - Admin Panel</title>
    <link rel="stylesheet" href="./assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="./assets/fonts/font-awesome.min.css">
    <link rel="stylesheet" href="./assets/css/Navbar-Right-Links-icons.css">
    <link rel="stylesheet" href="./assets/css/styles.css">
    <style>
        /* Admin form styles */
        .admin-form {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border: 1px solid #ddd;
        }
        
        .admin-form h2 {
            margin-bottom: 20px;
            color: #333;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .btn-add-game {
            background-color: #8B4513;
            color: white;
        }

        .nav-tabs {
            margin-bottom: 20px;
        }

        .tab-content > .tab-pane {
            display: none;
        }

        .tab-content > .active {
            display: block;
        }

        #result-message {
            display: none;
            margin-top: 20px;
        }

        .excel-template {
            border: 1px dashed #aaa;
            padding: 10px;
            background: #f2f2f2;
            margin-bottom: 15px;
        }
    </style>
</head>

<body>
    <header id="header" class="sticky-top">
        <nav class="navbar navbar-expand-lg py-3">
            <div class="container"><a class="navbar-brand d-flex align-items-center" href="./index.html"><img
                        src="./assets/img/logo.png" alt="Website Logo" style="height:40px"></a><button data-bs-toggle="collapse"
                    class="navbar-toggler" data-bs-target="#navcol-2"><span class="visually-hidden">Toggle
                        navigation</span><span class="navbar-toggler-icon"></span></button>
                <div class="collapse navbar-collapse nav-right" id="navcol-2">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item"><a class="nav-link" href="./index.html">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="./game-hot-wg.html">Hot Games</a></li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>
    
    <main>
        <div class="container">
            <h1 class="text-center mb-4">Add New Games</h1>
            
            <!-- Message alert box -->
            <div id="result-message" class="alert" role="alert"></div>
            
            <!-- Admin Form Section -->
            <div class="admin-form" id="admin-form">
                <ul class="nav nav-tabs" id="gameTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="single-tab" data-bs-toggle="tab" data-bs-target="#single-game" type="button" role="tab" aria-controls="single-game" aria-selected="true">Thêm Một Game</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="bulk-tab" data-bs-toggle="tab" data-bs-target="#bulk-games" type="button" role="tab" aria-controls="bulk-games" aria-selected="false">Thêm Nhiều Game (JSON)</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="excel-tab" data-bs-toggle="tab" data-bs-target="#excel-upload" type="button" role="tab" aria-controls="excel-upload" aria-selected="false">Upload Excel</button>
                    </li>
                </ul>
                
                <div class="tab-content" id="gameTabsContent">
                    <!-- Single Game Tab -->
                    <div class="tab-pane fade show active" id="single-game" role="tabpanel" aria-labelledby="single-tab">
                        <h2>Thêm Game Đơn Lẻ</h2>
                        <form id="single-game-form" method="post" action="add-game.php">
                            <input type="hidden" name="action" value="add_single">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label for="game-name">Tên Game</label>
                                        <input type="text" class="form-control" id="game-name" name="game_name" placeholder="Nhập tên game" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="game-description">Mô Tả Game</label>
                                        <textarea class="form-control" id="game-description" name="game_description" rows="3" placeholder="Nhập mô tả game"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="game-iframe">Game iframe URL</label>
                                        <input type="text" class="form-control" id="game-iframe" name="game_iframe" placeholder="Nhập iframe URL" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label for="game-category">Danh Mục Game</label>
                                        <select class="form-control" id="game-category" name="game_category" required>
                                            <option value="">Chọn Danh Mục</option>
                                            <option value="2-player">2-Player</option>
                                            <option value="3d">3D</option>
                                            <option value="adventure">Adventure</option>
                                            <option value="car">Car</option>
                                            <option value="moto">Moto</option>
                                            <option value="multiplayer">Multiplayer</option>
                                            <option value="puzzle">Puzzle</option>
                                            <option value="racing">Racing</option>
                                            <option value="running">Running</option>
                                            <option value="shooting">Shooting</option>
                                            <option value="skill">Skill</option>
                                            <option value="sports">Sports</option>
                                            <option value="stickman">Stickman</option>
                                        </select>
                                    </div>
                                    <div class="form-group">
                                        <label for="game-image-ext">Định Dạng Hình Ảnh</label>
                                        <div class="input-group">
                                            <input type="text" class="form-control" id="game-image-ext" name="game_image_ext" value="png" placeholder="Định dạng (png, jpg, webp...)">
                                        </div>
                                        <small class="form-text text-muted">Hình ảnh sẽ được sử dụng từ /assets/img/img-up/[slug].[định dạng]</small>
                                    </div>
                                    <div class="form-group mt-4">
                                        <div class="alert alert-info">
                                            <strong>Lưu ý:</strong> Đảm bảo tải hình ảnh game lên thư mục <code>/assets/img/img-up/</code> với tên là slug trước khi thêm game.
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center mt-3">
                                <button type="submit" class="btn btn-add-game" id="add-single-game">Thêm Game</button>
                            </div>
                        </form>
                    </div>
                    
                    <!-- Bulk Games Tab -->
                    <div class="tab-pane fade" id="bulk-games" role="tabpanel" aria-labelledby="bulk-tab">
                        <h2>Thêm Nhiều Game (JSON)</h2>
                        <form id="bulk-games-form" method="post" action="add-game.php">
                            <input type="hidden" name="action" value="add_bulk">
                            <div class="form-group">
                                <label for="bulk-games-data">Dữ Liệu JSON</label>
                                <textarea class="form-control" id="bulk-games-data" name="bulk_games" rows="8" placeholder='[
  {
    "name": "Tên Game",
    "description": "Mô tả game",
    "iframe": "URL",
    "category": "danh-mục",
    "imageExt": "png"
  },
  {
    "name": "Game Khác",
    "description": "Mô tả khác",
    "iframe": "URL",
    "category": "danh-mục",
    "imageExt": "jpg"
  }
]' required></textarea>
                            </div>
                            <div class="text-center mt-3">
                                <button type="submit" class="btn btn-add-game" id="add-bulk-games">Thêm Nhiều Game</button>
                            </div>
                        </form>
                    </div>
                    
                    <!-- Excel Upload Tab -->
                    <div class="tab-pane fade" id="excel-upload" role="tabpanel" aria-labelledby="excel-tab">
                        <h2>Upload File Excel</h2>
                        
                        <div class="excel-template">
                            <h5>Cấu trúc File Excel</h5>
                            <p>File Excel cần có các cột sau theo thứ tự:</p>
                            <ol>
                                <li><strong>Tên Game</strong> (bắt buộc)</li>
                                <li><strong>Mô Tả</strong> (tùy chọn)</li>
                                <li><strong>iframe URL</strong> (bắt buộc)</li>
                                <li><strong>Danh Mục</strong> (bắt buộc)</li>
                                <li><strong>Định Dạng Hình</strong> (tùy chọn, mặc định: png)</li>
                            </ol>
                            <p><strong>Lưu ý:</strong> Dòng đầu tiên được coi là tiêu đề và sẽ được bỏ qua.</p>
                            <p>
                                <a href="download-template.php">Tải xuống mẫu Excel (.xlsx)</a> | 
                                <a href="game-template.csv" download>Tải xuống mẫu CSV</a> | 
                                <a href="excel-template-info.txt" target="_blank">Xem hướng dẫn chi tiết</a>
                            </p>
                        </div>
                        
                        <form id="excel-upload-form" method="post" action="add-game.php" enctype="multipart/form-data">
                            <input type="hidden" name="action" value="upload_excel">
                            <div class="form-group">
                                <label for="excel-file">Chọn File Excel</label>
                                <input type="file" class="form-control" id="excel-file" name="excel_file" accept=".xlsx,.xls,.csv" required>
                                <small class="form-text text-muted">Chấp nhận các định dạng: .xlsx, .xls</small>
                            </div>
                            
                            <div class="form-check mt-3">
                                <input type="checkbox" class="form-check-input" id="use-csv" name="use_csv" value="1">
                                <label class="form-check-label" for="use-csv">Sử dụng file CSV thay thế (khi không có thư viện PhpSpreadsheet)</label>
                            </div>
                            
                            <div class="text-center mt-3">
                                <button type="submit" class="btn btn-add-game" id="upload-excel">Upload và Thêm Games</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            
            <div class="text-center mb-5">
                <a href="./game-hot-wg.html" class="btn btn-primary">Xem Danh Sách Game</a>
            </div>
        </div>
    </main>
    
    <footer>
        <div class="copyright">
            <div class="container">
                <span>Admin Panel</span>
                <span style="float:right;">
                    <a href="/dmca/">DMCA</a></li>&nbsp;&nbsp;
                    <a href="/terms/">Terms</a></li>&nbsp;&nbsp;
                    <a href="/privacy/">Privacy</a></li>
                </span>
            </div>
        </div>
    </footer>
    
    <script src="./assets/js/jquery.min.js"></script>
    <script src="./assets/bootstrap/js/bootstrap.min.js"></script>
    <script src="./assets/js/custom.js"></script>

    <script>
        // Suppress AbortError from unhandled promise rejections (media play/pause race)
        window.onerror = function(message, source, lineno, colno, error) {
            if (error && error.name === 'AbortError') {
                console.warn('Suppressed AbortError:', error);
                return true;
            }
            return false;
        };
        // Suppress Chrome play() AbortError from external media
        window.addEventListener('unhandledrejection', function(event) {
            if (event.reason && event.reason.name === 'AbortError') {
                event.preventDefault();
            }
        });
        // Handle form submissions with AJAX
        document.addEventListener('DOMContentLoaded', function() {
            // Helper function to show messages
            function showMessage(message, isSuccess) {
                const messageElement = document.getElementById('result-message');
                messageElement.textContent = message;
                messageElement.className = isSuccess ? 'alert alert-success' : 'alert alert-danger';
                messageElement.style.display = 'block';
                
                // Scroll to message
                messageElement.scrollIntoView({ behavior: 'smooth' });
                
                // Hide after 5 seconds
                setTimeout(function() {
                    messageElement.style.display = 'none';
                }, 5000);
            }
            
            // Single game form submission
            const singleGameForm = document.getElementById('single-game-form');
            if (singleGameForm) {
                singleGameForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    fetch('add-game.php', {
                        method: 'POST',
                        body: new FormData(singleGameForm)
                    })
                    .then(async response => {
                        const text = await response.text();
                        let data;
                        try {
                            data = JSON.parse(text);
                        } catch (err) {
                            console.error('Invalid JSON response:', text);
                            showMessage('Lỗi máy chủ: ' + text, false);
                            return;
                        }
                        showMessage(data.message, data.success);
                        if (data.success) {
                            singleGameForm.reset();
                        }
                    })
                    .catch(error => {
                        showMessage('Đã xảy ra lỗi: ' + error.message, false);
                    });
                });
            }
            
            // Bulk games form submission
            const bulkGamesForm = document.getElementById('bulk-games-form');
            if (bulkGamesForm) {
                bulkGamesForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    fetch('add-game.php', {
                        method: 'POST',
                        body: new FormData(bulkGamesForm)
                    })
                    .then(async response => {
                        const text = await response.text();
                        let data;
                        try {
                            data = JSON.parse(text);
                        } catch (err) {
                            console.error('Invalid JSON response:', text);
                            showMessage('Lỗi máy chủ: ' + text, false);
                            return;
                        }
                        showMessage(data.message, data.success);
                        if (data.success) {
                            bulkGamesForm.reset();
                        }
                    })
                    .catch(error => {
                        showMessage('Đã xảy ra lỗi: ' + error.message, false);
                    });
                });
            }
            
            // Excel upload form submission
            const excelUploadForm = document.getElementById('excel-upload-form');
            if (excelUploadForm) {
                excelUploadForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    fetch('add-game.php', {
                        method: 'POST',
                        body: new FormData(excelUploadForm)
                    })
                    .then(async response => {
                        const text = await response.text();
                        let data;
                        try {
                            data = JSON.parse(text);
                        } catch (err) {
                            console.error('Invalid JSON response:', text);
                            showMessage('Lỗi máy chủ: ' + text, false);
                            return;
                        }
                        showMessage(data.message, data.success);
                        if (data.success) {
                            excelUploadForm.reset();
                        }
                    })
                    .catch(error => {
                        showMessage('Đã xảy ra lỗi: ' + error.message, false);
                    });
                });
            }
        });
    </script>
</body>

</html> 