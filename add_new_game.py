import os
import shutil
import re
from datetime import datetime
import sys

# Danh sách tất cả các danh mục có thể thêm game vào
CATEGORIES = [
    "2-player", "3d", "action", "adventure", "car", "fighting", "fnf", 
    "hot-game", "idle", "moto", "multiplayer", "new", "papa-game", 
    "popular", "puzzle", "racing", "running", "shooting", "skill", 
    "sports", "stickman"
]

def create_slug(text):
    """Tạo slug từ văn bản, loại bỏ các ký tự đặc biệt"""
    # Chuyển sang chữ thường
    slug = text.lower()
    # Xóa tất cả ký tự đặc biệt và thay bằng gạch ngang
    slug = re.sub(r'[^\w\s-]', '-', slug)
    # Thay khoảng trắng bằng gạch ngang
    slug = re.sub(r'\s+', '-', slug)
    # Loại bỏ các gạch ngang liên tiếp
    slug = re.sub(r'-+', '-', slug)
    # Loại bỏ gạch ngang ở đầu và cuối
    slug = slug.strip('-')
    return slug

def create_game_page(game_name, iframe_url, image_path, categories):
    """Tạo trang game mới bằng cách sao chép từ game mẫu và thay đổi nội dung"""
    print(f"\n[ĐANG TẠO TRANG GAME: {game_name}]")
    
    # Tạo slug từ tên game
    slug = create_slug(game_name)
    
    # Đường dẫn đến file HTML của game mới
    new_game_path = os.path.join("go", f"{slug}.html")
    
    # Kiểm tra xem game đã tồn tại chưa
    if os.path.exists(new_game_path):
        print(f"⚠️ Lỗi: Game {game_name} đã tồn tại tại đường dẫn: {new_game_path}")
        return False
    
    # Sử dụng stack-bump-3d.html làm mẫu thay vì cookie-clicker.html
    template_game_path = os.path.join("go", "stack-bump-3d.html")
    
    # Kiểm tra xem file mẫu có tồn tại không
    if not os.path.exists(template_game_path):
        print(f"⚠️ Lỗi: Không tìm thấy file mẫu: {template_game_path}")
        print("Đang chuyển sang sử dụng file mẫu dự phòng...")
        template_game_path = os.path.join("go", "cookie-clicker.html")
        if not os.path.exists(template_game_path):
            print(f"⚠️ Lỗi: Không tìm thấy file mẫu dự phòng: {template_game_path}")
            return False
    
    try:
        # Đọc nội dung của game mẫu
        with open(template_game_path, 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        # Thay thế tên game, iframe URL và các thông tin khác
        # Thay thế tiêu đề để sử dụng tên game mới
        template_content = re.sub(
            r'<title>.*?</title>',
            f'<title>{game_name} | Monkey Mart Games</title>',
            template_content
        )
        
        # Thay thế tên game trong tiêu đề H1 nếu có
        template_content = re.sub(
            r'<h1.*?>.*?</h1>',
            f'<h1>{game_name}</h1>',
            template_content
        )
        
        # Thay thế mô tả
        template_content = re.sub(
            r'<meta content=".*?" name="description"/>',
            f'<meta content="Play {game_name}, an exciting online game at Monkey Mart Games. Have fun with this free browser game!" name="description"/>',
            template_content
        )
        
        # Thay thế từ khóa
        keywords = f"{slug}, {', '.join(categories)}, free online games"
        template_content = re.sub(
            r'<meta content=".*?" name="keywords"/>',
            f'<meta content="{keywords}" name="keywords"/>',
            template_content
        )
        
        # Thay thế các meta OG
        template_content = re.sub(
            r'<meta content=".*?" property="og:title"/>',
            f'<meta content="{game_name} | Monkey Mart Games" property="og:title"/>',
            template_content
        )
        
        template_content = re.sub(
            r'<meta content=".*?" property="og:description"/>',
            f'<meta content="Play {game_name}, an exciting online game at Monkey Mart Games. Have fun with this free browser game!" property="og:description"/>',
            template_content
        )
        
        # Thay thế đường dẫn hình ảnh
        image_filename = os.path.basename(image_path)
        template_content = re.sub(
            r'<meta content="https://monkeymart.one/img/games/.*?" property="og:image"/>',
            f'<meta content="https://monkeymart.one/img/games/{image_filename}" property="og:image"/>',
            template_content
        )
        
        # Thay thế URL
        template_content = re.sub(
            r'<meta content="https://monkeymart.one/go/.*?" property="og:url"/>',
            f'<meta content="https://monkeymart.one/go/{slug}.html" property="og:url"/>',
            template_content
        )
        
        template_content = re.sub(
            r'<link href="https://monkeymart.one/go/.*?" rel="canonical"/>',
            f'<link href="https://monkeymart.one/go/{slug}.html" rel="canonical"/>',
            template_content
        )
        
        # Thay thế iframe URL
        template_content = re.sub(
            r'<iframe.*?data-src=".*?".*?>',
            f'<iframe allowfullscreen="" data-src="{iframe_url}" frameborder="0" height="100%" scrolling="none" title="{game_name}" width="100%">',
            template_content
        )
        
        # Cập nhật các Schema.org
        template_content = re.sub(
            r'"@id": "https://monkeymart.one/go/.*?#.*?"',
            f'"@id": "https://monkeymart.one/go/{slug}.html#{slug}"',
            template_content
        )
        
        template_content = re.sub(
            r'"name": ".*?"',
            f'"name": "{game_name}"',
            template_content, count=1
        )
        
        template_content = re.sub(
            r'"description": ".*?"',
            f'"description": "{game_name} is an exciting online game available at Monkey Mart Games. Enjoy hours of gameplay for free right in your browser."',
            template_content, count=1
        )
        
        template_content = re.sub(
            r'"url": "https://monkeymart.one/go/.*?"',
            f'"url": "https://monkeymart.one/go/{slug}.html"',
            template_content, count=1
        )
        
        template_content = re.sub(
            r'"image": "https://monkeymart.one/img/games/.*?"',
            f'"image": "https://monkeymart.one/img/games/{image_filename}"',
            template_content, count=1
        )
        
        template_content = re.sub(
            r'"screenshot": "https://monkeymart.one/img/games/.*?"',
            f'"screenshot": "https://monkeymart.one/img/games/{image_filename}"',
            template_content, count=1
        )
        
        # Cập nhật danh mục game trong Schema
        genre_str = ", ".join([f'"{cat.capitalize()}"' for cat in categories])
        template_content = re.sub(
            r'"genre": \[.*?\]',
            f'"genre": [{genre_str}]',
            template_content
        )
        
        # Đảm bảo cập nhật tất cả các phần chứa tên game cũ (Stack Bump 3D) thành tên game mới
        template_content = re.sub(
            r'Stack Bump 3D',
            game_name,
            template_content
        )
        
        template_content = re.sub(
            r'stack-bump-3d',
            slug,
            template_content
        )
        
        # Ghi nội dung đã chỉnh sửa vào file mới
        with open(new_game_path, 'w', encoding='utf-8') as file:
            file.write(template_content)
        
        print(f"✅ Đã tạo trang game thành công: {new_game_path}")
        return True
    
    except Exception as e:
        print(f"⚠️ Lỗi khi tạo trang game: {str(e)}")
        return False

def update_homepage(game_name, image_path):
    """Cập nhật trang chủ với game mới"""
    try:
        print("\n[ĐANG CẬP NHẬT TRANG CHỦ]")
        
        # Đường dẫn tới file trang chủ
        homepage_path = "index.html"
        
        # Kiểm tra xem file trang chủ có tồn tại không
        if not os.path.exists(homepage_path):
            print(f"⚠️ Không tìm thấy file trang chủ: {homepage_path}")
            return False
        
        # Tạo slug từ tên game
        slug = create_slug(game_name)
        
        # Đường dẫn hình ảnh
        image_filename = os.path.basename(image_path)
        
        # Đọc nội dung file trang chủ
        with open(homepage_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Kiểm tra xem game đã có trong trang chủ chưa
        game_link = f'href="go/{slug}.html"'
        if game_link in content:
            print(f"⚠️ Game '{game_name}' đã tồn tại trong trang chủ")
            if input(f"Bạn có muốn thêm lại game vào trang chủ? (y/n): ").lower() != 'y':
                print(f"Đã bỏ qua thêm game vào trang chủ")
                return False
        
        # Tìm container chứa danh sách game
        container_patterns = [
            '<div class="row ltn__product-slider-item-three-active-full-width slick-arrow-1">',
            '<div class="row ltn__tab-product-slider-one-active--- slick-arrow-1">',
            '<div class="row game-container">'
        ]
        
        container_start_pos = -1
        for pattern in container_patterns:
            container_start_pos = content.find(pattern)
            if container_start_pos != -1:
                # Tìm thẻ đóng của container div
                insert_pos = content.find('>', container_start_pos) + 1
                break
        
        if container_start_pos == -1:
            print(f"⚠️ Không tìm thấy container chứa danh sách game trong file {homepage_path}")
            return False
        
        # Chuẩn bị mã HTML cho game mới
        game_html = f'''
<!-- {game_name} -->
<div class="col-lg-2 col-md-4 col-sm-6">
    <a href="go/{slug}.html">
        <div class="game-card">
            <img class="lazyload" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="img/games/{image_filename}" alt="{game_name}">
            <h5>{game_name}</h5>
            <div class="game-card-info">
            </div>
        </div>
    </a>
</div>'''
        
        # Chèn game mới vào đầu danh sách game (sau thẻ mở container)
        new_content = content[:insert_pos] + game_html + content[insert_pos:]
        
        # Ghi nội dung mới vào file
        with open(homepage_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"✅ Đã thêm {game_name} vào trang chủ thành công")
        return True
    except Exception as e:
        print(f"⚠️ Lỗi khi cập nhật trang chủ: {str(e)}")
        return False

def update_category_page(game_name, image_path, category):
    """Cập nhật trang danh mục với game mới"""
    try:
        # Kiểm tra cả hai vị trí cho file danh mục
        category_file = f"{category}.html"
        category_file_in_folder = os.path.join("category", f"{category}.html")
        
        # Đường dẫn tới file thực tế
        actual_category_file = None
        
        # Kiểm tra file ở thư mục gốc
        if os.path.exists(category_file):
            actual_category_file = category_file
        # Kiểm tra file ở thư mục category/
        elif os.path.exists(category_file_in_folder):
            actual_category_file = category_file_in_folder
        else:
            print(f"⚠️ Không tìm thấy file danh mục: {category} (đã kiểm tra ở cả thư mục gốc và thư mục category/)")
            return False
        
        # Tạo slug từ tên game
        slug = create_slug(game_name)
        
        # Đường dẫn hình ảnh
        image_filename = os.path.basename(image_path)
        
        # Đọc nội dung file danh mục
        with open(actual_category_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Kiểm tra xem game đã có trong danh mục chưa
        game_link = f'href="go/{slug}.html"'
        alternative_game_link = f'href="/go/{slug}.html"'
        
        if game_link in content or alternative_game_link in content:
            print(f"⚠️ Game '{game_name}' đã tồn tại trong danh mục '{category}'")
            if input(f"Bạn có muốn thêm lại game vào danh mục '{category}'? (y/n): ").lower() != 'y':
                print(f"Đã bỏ qua thêm game vào danh mục '{category}'")
                return False
        
        # Tìm container chứa danh sách game
        container_patterns = [
            '<div class="row ltn__tab-product-slider-one-active--- slick-arrow-1">',
            '<div class="row ltn__product-slider-item-three-active-full-width slick-arrow-1">',
            '<div class="row">'
        ]
        
        container_start_pos = -1
        for pattern in container_patterns:
            container_start_pos = content.find(pattern)
            if container_start_pos != -1:
                # Tìm thẻ đóng của container div
                insert_pos = content.find('>', container_start_pos) + 1
                break
        
        if container_start_pos == -1:
            print(f"⚠️ Không tìm thấy container chứa danh sách game trong file {actual_category_file}")
            return False
        
        # Chuẩn bị mã HTML cho game mới dựa trên cấu trúc của file
        in_category_folder = "category" in actual_category_file
        
        if in_category_folder:
            # Mẫu HTML cho file trong thư mục category/
            game_html = f'''
<!-- {game_name} -->
<div class="col-lg-2 col-md-4 col-sm-6 col-6">
<a href="/go/{slug}.html" title="{slug}">
<div class="product-img">
<img alt="{slug}" class="lazyload" data-src="/img/games/{image_filename}" decoding="async" loading="lazy" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="/>
<div class="product-badge">
<span class="badge-new">New</span>
</div>
</div>
<div class="ltn__product-item ltn__product-item-3 text-left">
<h6>{game_name}</h6>
</div>
</a>
</div>'''
        else:
            # Mẫu HTML cho file ở thư mục gốc
            game_html = f'''
<!-- {game_name} -->
<div class="col-lg-2 col-md-4 col-sm-6">
<a href="go/{slug}.html">
<div class="game-card">
<img class="lazyload" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="img/games/{image_filename}" alt="{game_name}">
<h5>{game_name}</h5>
<div class="game-card-info">
<p>Chơi ngay</p>
</div>
</div>
</a>
</div>'''
        
        # Chèn game mới vào đầu danh sách game (sau thẻ mở container)
        new_content = content[:insert_pos] + game_html + content[insert_pos:]
        
        # Ghi nội dung mới vào file
        with open(actual_category_file, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"✅ Đã thêm '{game_name}' vào danh mục: {category}")
        return True
    except Exception as e:
        print(f"⚠️ Lỗi khi cập nhật trang danh mục {category}: {str(e)}")
        return False

def check_and_fix_errors():
    """Kiểm tra và sửa lỗi sau khi thêm game"""
    print("\n[KIỂM TRA VÀ SỬA LỖI SAU KHI THÊM GAME]")
    
    # Kiểm tra lỗi trùng lặp trong homepage
    check_homepage_for_duplicates()
    
    # Kiểm tra lỗi trùng lặp trong trang danh mục
    check_category_pages_for_duplicates()
    
    # Kiểm tra lỗi tên tệp hình ảnh
    check_image_paths()
    
    print("✅ Đã hoàn tất kiểm tra và sửa lỗi")

def check_homepage_for_duplicates():
    """Kiểm tra và sửa lỗi trùng lặp trong trang chủ"""
    try:
        # Đọc nội dung trang chủ
        with open('index.html', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Tìm kiếm các game-card trong trang chủ
        game_cards = re.findall(r'<div class="game-card">.*?</div>\s*</div>\s*</a>\s*</div>', content, re.DOTALL)
        
        # Dictionary để theo dõi các game đã gặp
        seen_games = {}
        duplicates = []
        
        # Tìm kiếm trùng lặp
        for card in game_cards:
            # Lấy tên game
            match = re.search(r'<h5>(.*?)</h5>', card)
            if match:
                game_name = match.group(1)
                if game_name in seen_games:
                    duplicates.append(game_name)
                else:
                    seen_games[game_name] = card
        
        # Thông báo và sửa lỗi nếu có trùng lặp
        if duplicates:
            print(f"⚠️ Phát hiện {len(duplicates)} game trùng lặp trong trang chủ: {', '.join(duplicates)}")
            
            if input("Bạn có muốn xóa các mục trùng lặp? (y/n): ").lower() == 'y':
                for game in duplicates:
                    # Giữ lại game đầu tiên, xóa các game trùng lặp
                    pattern = r'<div class="col-lg-2 col-md-4 col-sm-6">\s*<a href="go/.*?\.html">\s*<div class="game-card">.*?<h5>' + re.escape(game) + r'</h5>.*?</div>\s*</div>\s*</a>\s*</div>'
                    
                    # Tìm tất cả các trường hợp
                    matches = list(re.finditer(pattern, content, re.DOTALL))
                    
                    # Xóa từ lần xuất hiện thứ hai trở đi
                    if len(matches) > 1:
                        for match in reversed(matches[1:]):  # Xử lý từ cuối lên để tránh thay đổi vị trí
                            content = content[:match.start()] + content[match.end():]
                
                # Ghi nội dung mới vào file
                with open('index.html', 'w', encoding='utf-8') as file:
                    file.write(content)
                
                print(f"✅ Đã xóa các mục trùng lặp trong trang chủ")
            else:
                print("⚠️ Đã bỏ qua việc xóa các mục trùng lặp trong trang chủ")
        else:
            print("✅ Không phát hiện game trùng lặp trong trang chủ")
        
    except Exception as e:
        print(f"⚠️ Lỗi khi kiểm tra trùng lặp trong trang chủ: {str(e)}")

def check_category_pages_for_duplicates():
    """Kiểm tra và sửa lỗi trùng lặp trong trang danh mục"""
    try:
        # Kiểm tra từng trang danh mục
        for category in CATEGORIES:
            category_file = f"{category}.html"
            
            if not os.path.exists(category_file):
                continue
                
            # Đọc nội dung trang danh mục
            with open(category_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Tìm kiếm các game-card trong trang danh mục
            game_cards = re.findall(r'<div class="game-card">.*?</div>\s*</div>\s*</a>\s*</div>', content, re.DOTALL)
            
            # Dictionary để theo dõi các game đã gặp
            seen_games = {}
            duplicates = []
            
            # Tìm kiếm trùng lặp
            for card in game_cards:
                # Lấy tên game
                match = re.search(r'<h5>(.*?)</h5>', card)
                if match:
                    game_name = match.group(1)
                    if game_name in seen_games:
                        duplicates.append(game_name)
                    else:
                        seen_games[game_name] = card
            
            # Thông báo và sửa lỗi nếu có trùng lặp
            if duplicates:
                print(f"⚠️ Phát hiện {len(duplicates)} game trùng lặp trong danh mục '{category}': {', '.join(duplicates)}")
                
                if input(f"Bạn có muốn xóa các mục trùng lặp trong danh mục '{category}'? (y/n): ").lower() == 'y':
                    for game in duplicates:
                        # Giữ lại game đầu tiên, xóa các game trùng lặp
                        pattern = r'<div class="col-lg-2 col-md-4 col-sm-6">\s*<a href="go/.*?\.html">\s*<div class="game-card">.*?<h5>' + re.escape(game) + r'</h5>.*?</div>\s*</div>\s*</a>\s*</div>'
                        
                        # Tìm tất cả các trường hợp
                        matches = list(re.finditer(pattern, content, re.DOTALL))
                        
                        # Xóa từ lần xuất hiện thứ hai trở đi
                        if len(matches) > 1:
                            for match in reversed(matches[1:]):  # Xử lý từ cuối lên để tránh thay đổi vị trí
                                content = content[:match.start()] + content[match.end():]
                    
                    # Ghi nội dung mới vào file
                    with open(category_file, 'w', encoding='utf-8') as file:
                        file.write(content)
                    
                    print(f"✅ Đã xóa các mục trùng lặp trong danh mục '{category}'")
                else:
                    print(f"⚠️ Đã bỏ qua việc xóa các mục trùng lặp trong danh mục '{category}'")
            else:
                print(f"✅ Không phát hiện game trùng lặp trong danh mục '{category}'")
        
    except Exception as e:
        print(f"⚠️ Lỗi khi kiểm tra trùng lặp trong trang danh mục: {str(e)}")

def check_image_paths():
    """Kiểm tra và sửa lỗi đường dẫn hình ảnh"""
    try:
        # Đọc nội dung trang chủ
        with open('index.html', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Tìm kiếm các đường dẫn hình ảnh trong trang chủ
        image_paths = re.findall(r'data-src="img/games/(.*?)"', content)
        
        # Kiểm tra từng đường dẫn hình ảnh
        broken_images = []
        for path in image_paths:
            full_path = os.path.join('img', 'games', path)
            if not os.path.exists(full_path):
                broken_images.append(path)
        
        # Thông báo và sửa lỗi nếu có đường dẫn hình ảnh bị hỏng
        if broken_images:
            print(f"⚠️ Phát hiện {len(broken_images)} đường dẫn hình ảnh bị hỏng: {', '.join(broken_images)}")
            print("⚠️ Vui lòng đảm bảo tất cả hình ảnh đã được đặt trong thư mục img/games/")
            
            for img in broken_images:
                img_name = os.path.splitext(img)[0]
                suggestion = f"Bạn có thể cần kiểm tra tên file ảnh hoặc đặt ảnh vào thư mục img/games/"
                print(f"   - Ảnh bị thiếu: {img} - {suggestion}")
        else:
            print("✅ Tất cả đường dẫn hình ảnh đều hợp lệ")
        
    except Exception as e:
        print(f"⚠️ Lỗi khi kiểm tra đường dẫn hình ảnh: {str(e)}")

def main():
    """Hàm chính xử lý việc thêm game mới"""
    print("\n===== MONKEYMART3T GAME ADDER =====")
    print("Công cụ này sẽ giúp bạn thêm game mới vào website Monkey Mart 3T")
    print("Công cụ này sẽ yêu cầu xác nhận trước mỗi thay đổi")
    
    # Nhập thông tin game từ người dùng
    game_info = collect_game_info()
    
    # Xác nhận tạo trang game
    confirm_create = input("\nBạn có muốn tạo trang game mới? (y/n): ")
    if confirm_create.lower() != 'y':
        print("Đã hủy tạo trang game.")
        return
    
    # Tạo trang game mới
    if create_game_page(game_info["name"], game_info["iframe_url"], game_info["image_path"], game_info["categories"]):
        # Xác nhận cập nhật trang chủ
        confirm_homepage = input("\nBạn có muốn cập nhật trang chủ với game mới? (y/n): ")
        if confirm_homepage.lower() == 'y':
            # Cập nhật trang chủ
            update_homepage(game_info["name"], game_info["image_path"])
        else:
            print("Đã bỏ qua cập nhật trang chủ.")
        
        # Cập nhật các trang danh mục
        if game_info["categories"]:
            confirm_categories = input("\nBạn có muốn cập nhật các trang danh mục đã chọn? (y/n): ")
            if confirm_categories.lower() == 'y':
                print("\n[ĐANG CẬP NHẬT TRANG DANH MỤC]")
                for category in game_info["categories"]:
                    update_category_page(game_info["name"], game_info["image_path"], category)
            else:
                print("Đã bỏ qua cập nhật trang danh mục.")
        
        # Kiểm tra và sửa lỗi sau khi thêm game
        confirm_check = input("\nBạn có muốn kiểm tra và sửa lỗi sau khi thêm game? (y/n): ")
        if confirm_check.lower() == 'y':
            check_and_fix_errors()
        else:
            print("Đã bỏ qua kiểm tra và sửa lỗi.")
        
        print(f"\nLưu ý: Đảm bảo bạn đã đặt hình ảnh tại: img/games/{os.path.basename(game_info['image_path'])}")
        print("\n===== HOÀN THÀNH =====")
        print("Cảm ơn bạn đã sử dụng công cụ thêm game Monkey Mart 3T!")

def collect_game_info():
    """Thu thập thông tin game từ người dùng và cho phép chỉnh sửa"""
    game_info = {}
    editing = True
    
    while editing:
        if "name" not in game_info:
            game_info["name"] = input("\nNhập tên game: ")
        if "iframe_url" not in game_info:
            game_info["iframe_url"] = input("Nhập đường dẫn iframe URL: ")
        if "image_path" not in game_info:
            game_info["image_path"] = input("Nhập đường dẫn hình ảnh (ví dụ: game-name.jpg): ")
        
        # Tạo slug từ tên game
        slug = create_slug(game_info["name"])
        print(f"\nSlug được tạo: {slug}")
        
        # Kiểm tra tên game đã tồn tại chưa
        game_path = os.path.join("go", f"{slug}.html")
        if os.path.exists(game_path):
            print(f"⚠️ Game với slug '{slug}' đã tồn tại!")
            continue_anyway = input("Bạn có muốn tiếp tục không? (y/n): ")
            if continue_anyway.lower() != 'y':
                print("Đã hủy thêm game.")
                sys.exit(0)
        
        # Hiển thị danh sách danh mục nếu chưa chọn
        if "categories" not in game_info:
            print("\nDanh sách các danh mục có thể thêm game vào:")
            for i, category in enumerate(CATEGORIES, 1):
                print(f"{i}. {category}")
            
            # Nhập các danh mục từ người dùng
            category_indices = input("\nNhập các số thứ tự danh mục muốn thêm, cách nhau bởi dấu phẩy (ví dụ: 1,3,5): ")
            game_info["categories"] = []
            
            try:
                indices = [int(idx.strip()) for idx in category_indices.split(",") if idx.strip()]
                for idx in indices:
                    if 1 <= idx <= len(CATEGORIES):
                        game_info["categories"].append(CATEGORIES[idx-1])
                    else:
                        print(f"⚠️ Danh mục với số {idx} không tồn tại, bỏ qua.")
            except ValueError:
                print("⚠️ Lỗi khi đọc danh mục, vui lòng nhập các số cách nhau bởi dấu phẩy.")
        
        # Hiển thị thông tin đã nhập
        print("\n=== THÔNG TIN GAME ===")
        print(f"Tên game: {game_info['name']}")
        print(f"Iframe URL: {game_info['iframe_url']}")
        print(f"Đường dẫn hình ảnh: {game_info['image_path']}")
        if game_info["categories"]:
            print(f"Các danh mục đã chọn: {', '.join(game_info['categories'])}")
        else:
            print("Không có danh mục nào được chọn, game sẽ chỉ được thêm vào trang chủ.")
        
        # Hỏi người dùng có muốn chỉnh sửa thông tin không
        edit_choice = input("\nBạn có muốn chỉnh sửa thông tin không? (y/n): ")
        
        if edit_choice.lower() == 'y':
            edit_what = input("\nChọn thông tin muốn chỉnh sửa (nhập số):\n1. Tên game\n2. Iframe URL\n3. Đường dẫn hình ảnh\n4. Danh mục\n5. Chỉnh sửa tất cả\nLựa chọn của bạn: ")
            
            if edit_what == "1":
                game_info["name"] = input("Nhập tên game mới: ")
            elif edit_what == "2":
                game_info["iframe_url"] = input("Nhập iframe URL mới: ")
            elif edit_what == "3":
                game_info["image_path"] = input("Nhập đường dẫn hình ảnh mới: ")
            elif edit_what == "4":
                # Xóa danh mục đã chọn và chọn lại
                del game_info["categories"]
            elif edit_what == "5":
                # Xóa tất cả thông tin và nhập lại
                game_info.clear()
            else:
                print("Lựa chọn không hợp lệ, giữ nguyên thông tin.")
        else:
            editing = False
    
    return game_info

if __name__ == "__main__":
    main() 