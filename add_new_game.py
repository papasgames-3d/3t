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
    slug = re.sub(r'[^\w\s-]', '', slug)
    # Thay khoảng trắng bằng gạch ngang
    slug = re.sub(r'\s+', '-', slug)
    # Loại bỏ các gạch ngang liên tiếp
    slug = re.sub(r'-+', '-', slug)
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
    
    # Chọn một game mẫu để sao chép (ví dụ: cookie-clicker.html)
    template_game_path = os.path.join("go", "cookie-clicker.html")
    
    try:
        # Đọc nội dung của game mẫu
        with open(template_game_path, 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        # Thay thế tên game, iframe URL và các thông tin khác
        # Thay thế tiêu đề
        template_content = re.sub(
            r'<title>.*?</title>',
            f'<title>{game_name} | Monkey Mart Games</title>',
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
            f'<iframe id="game-iframe" scrolling="none" src="{iframe_url}" frameborder="0" height="100%" width="100%" allowfullscreen="">',
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
        
        # Ghi nội dung đã chỉnh sửa vào file mới
        with open(new_game_path, 'w', encoding='utf-8') as file:
            file.write(template_content)
        
        print(f"✅ Đã tạo trang game thành công: {new_game_path}")
        return True
    
    except Exception as e:
        print(f"⚠️ Lỗi khi tạo trang game: {str(e)}")
        return False

def update_homepage(game_name, image_path):
    """Thêm game vào trang chủ"""
    print(f"\n[ĐANG CẬP NHẬT TRANG CHỦ]")
    
    # Tạo slug từ tên game
    slug = create_slug(game_name)
    
    # Đường dẫn trang chủ
    homepage_path = "index.html"
    
    try:
        # Đọc nội dung trang chủ
        with open(homepage_path, 'r', encoding='utf-8') as file:
            homepage_content = file.read()
        
        # Tìm vị trí để thêm game mới (sau một div với class="col-lg-2 col-md-4 col-sm-6 col-6")
        pattern = r'(<!-- ltn__product-item -->[\s\S]+?<div class="col-lg-2 col-md-4 col-sm-6 col-6">[\s\S]+?</div>[\s\S]+?</div>)'
        match = re.search(pattern, homepage_content)
        
        if match:
            # Lấy đoạn HTML mẫu
            template_game_card = match.group(1)
            
            # Tạo đoạn HTML cho game mới theo cấu trúc mới
            image_filename = os.path.basename(image_path)
            
            new_game_card = f'''
<!-- ltn__product-item -->
<div class="col-lg-2 col-md-4 col-sm-6 col-6">
<a title="{game_name}" href="/go/{slug}.html">
<div class="product-img">
<img class="lazyload" alt="{game_name}" src="/img/games/{image_filename}">
<div class="product-badge">
</div>
</div>
<div class="ltn__product-item ltn__product-item-3 text-left">
</div>
</a>
</div>'''
            
            # Chèn game mới vào vị trí thích hợp (sau div của game đầu tiên)
            updated_content = re.sub(
                pattern,
                match.group(1) + new_game_card,
                homepage_content,
                count=1
            )
            
            # Ghi nội dung đã cập nhật vào file trang chủ
            with open(homepage_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print(f"✅ Đã thêm {game_name} vào trang chủ thành công")
            return True
        
        else:
            print("⚠️ Không tìm thấy vị trí thích hợp để thêm game vào trang chủ")
            return False
    
    except Exception as e:
        print(f"⚠️ Lỗi khi cập nhật trang chủ: {str(e)}")
        return False

def update_category_page(game_name, image_path, category):
    """Thêm game vào trang danh mục"""
    print(f"  - Đang thêm game vào danh mục: {category}")
    
    # Tạo slug từ tên game
    slug = create_slug(game_name)
    
    # Đường dẫn trang danh mục
    category_path = os.path.join("category", f"{category}.html")
    
    # Kiểm tra xem danh mục có tồn tại không
    if not os.path.exists(category_path):
        print(f"    ⚠️ Danh mục {category} không tồn tại")
        return False
    
    try:
        # Đọc nội dung trang danh mục
        with open(category_path, 'r', encoding='utf-8') as file:
            category_content = file.read()
        
        # Kiểm tra xem game đã có trong danh mục chưa
        if f'href="/go/{slug}.html"' in category_content:
            print(f"    ℹ️ Game {game_name} đã tồn tại trong danh mục {category}")
            return False
        
        # Tìm vị trí để thêm game mới (sau một div với class="row ltn__tab")
        pattern = r'<div class="row ltn__tab-product-slider-one-active--- slick-arrow-1">'
        match = re.search(pattern, category_content)
        
        if match:
            # Tạo đoạn HTML cho game mới
            image_filename = os.path.basename(image_path)
            
            new_game_card = f'''
<!-- ltn__product-item -->
<div class="col-lg-2 col-md-4 col-sm-6 col-6">
<a title="{game_name}" href="/go/{slug}.html">
<div class="product-img">
<img class="lazyload" alt="{game_name}" src="/img/games/{image_filename}">
<div class="product-badge">
<span class="badge-new">New</span>
</div>
</div>
<div class="ltn__product-item ltn__product-item-3 text-left">
</div>
</a>
</div>'''
            
            # Chèn game mới vào vị trí thích hợp (sau div row)
            position = match.end()
            updated_content = category_content[:position] + new_game_card + category_content[position:]
            
            # Ghi nội dung đã cập nhật vào file danh mục
            with open(category_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print(f"    ✅ Đã thêm {game_name} vào danh mục {category} thành công")
            return True
        
        else:
            print(f"    ⚠️ Không tìm thấy vị trí thích hợp để thêm game vào danh mục {category}")
            return False
    
    except Exception as e:
        print(f"    ⚠️ Lỗi khi cập nhật danh mục {category}: {str(e)}")
        return False

def main():
    """Hàm chính xử lý việc thêm game mới"""
    print("=" * 50)
    print("MONKEYMART3T GAME ADDER")
    print("=" * 50)
    print("Chào mừng! Công cụ này giúp bạn thêm game mới vào dự án MonkeyMart3t.")
    print("Vui lòng cung cấp các thông tin sau chính xác:")
    
    # Nhập thông tin game
    game_name = input("\n1. Tên game (chính xác): ").strip()
    if not game_name:
        print("⚠️ Lỗi: Tên game không được để trống!")
        return
    
    iframe_url = input("\n2. Đường dẫn iframe (URL chính xác): ").strip()
    if not iframe_url:
        print("⚠️ Lỗi: Đường dẫn iframe không được để trống!")
        return
    
    # Xác nhận thông tin đầu vào
    print(f"\nBạn đã nhập:")
    print(f"- Tên game: {game_name}")
    print(f"- URL iframe: {iframe_url}")
    confirm = input("Thông tin đã chính xác? (y/n): ").strip().lower()
    if confirm != 'y':
        print("⚠️ Hủy thêm game. Vui lòng chạy lại và nhập thông tin chính xác.")
        return
    
    # Xử lý đường dẫn hình ảnh
    image_path = input("\n3. Đường dẫn hình ảnh (tương đối hoặc tuyệt đối): ").strip()
    if not image_path:
        print("⚠️ Lỗi: Đường dẫn hình ảnh không được để trống!")
        return
    
    # Trích xuất tên file từ đường dẫn
    image_filename = os.path.basename(image_path)
    
    # Kiểm tra xem hình ảnh đã tồn tại trong thư mục /img/games/ chưa
    target_image_path = os.path.join("img", "games", image_filename)
    if not os.path.exists(target_image_path):
        # Nếu image_path là đường dẫn đến file thật, sao chép file vào thư mục img/games/
        if os.path.exists(image_path):
            try:
                os.makedirs(os.path.dirname(target_image_path), exist_ok=True)
                shutil.copy2(image_path, target_image_path)
                print(f"✅ Đã sao chép hình ảnh vào: {target_image_path}")
            except Exception as e:
                print(f"⚠️ Lỗi khi sao chép hình ảnh: {str(e)}")
                print(f"⚠️ Vui lòng đặt hình ảnh vào thư mục: img/games/ và đặt tên là {image_filename}")
        else:
            print(f"⚠️ Không tìm thấy hình ảnh tại: {image_path}")
            print(f"⚠️ Vui lòng đặt hình ảnh vào thư mục: img/games/ và đặt tên là {image_filename}")
    
    # Hiển thị danh sách category để người dùng chọn
    print("\n4. Chọn các danh mục cho game (nhập số, cách nhau bởi dấu phẩy):")
    for idx, category in enumerate(CATEGORIES, 1):
        print(f"   {idx}. {category}")
    
    category_input = input("\nNhập lựa chọn của bạn (ví dụ: 1,3,5): ").strip()
    selected_indices = [int(idx.strip()) for idx in category_input.split(",") if idx.strip().isdigit()]
    
    if not selected_indices:
        print("⚠️ Lỗi: Bạn chưa chọn danh mục nào!")
        return
    
    selected_categories = [CATEGORIES[idx-1] for idx in selected_indices if 1 <= idx <= len(CATEGORIES)]
    
    print(f"\nĐã chọn các danh mục: {', '.join(selected_categories)}")
    
    # Tạo trang game mới
    if create_game_page(game_name, iframe_url, image_filename, selected_categories):
        # Cập nhật trang chủ
        update_homepage(game_name, image_filename)
        
        # Cập nhật các trang danh mục
        print("\n[ĐANG CẬP NHẬT TRANG DANH MỤC]")
        successful_categories = []
        failed_categories = []
        
        for category in selected_categories:
            if update_category_page(game_name, image_filename, category):
                successful_categories.append(category)
            else:
                failed_categories.append(category)
        
        # Thông báo kết quả
        print("\n" + "=" * 50)
        print(f"KẾT QUẢ THÊM GAME: {game_name}")
        print("=" * 50)
        
        slug = create_slug(game_name)
        print(f"✅ Đã tạo trang game: go/{slug}.html")
        print("✅ Đã cập nhật trang chủ")
        
        if successful_categories:
            print(f"✅ Đã thêm vào {len(successful_categories)} danh mục: {', '.join(successful_categories)}")
        
        if failed_categories:
            print(f"⚠️ Không thể thêm vào {len(failed_categories)} danh mục: {', '.join(failed_categories)}")
        
        print(f"\n⭐ Lưu ý: Đảm bảo rằng hình ảnh đã được đặt trong thư mục img/games/ với tên {image_filename}")
        print("=" * 50)
    
    print("\nCảm ơn bạn đã sử dụng công cụ!")

if __name__ == "__main__":
    main() 