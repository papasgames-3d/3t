import os
import re
import glob
import shutil
from datetime import datetime

def backup_file(file_path):
    """Tạo bản sao lưu cho file"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        print(f"  ✅ Đã tạo bản sao lưu: {backup_path}")
        return backup_path
    return None

def restore_homepage():
    """Khôi phục trang chủ về trạng thái ban đầu"""
    print("\n[BẮT ĐẦU KHÔI PHỤC TRANG CHỦ]")
    
    # Đường dẫn trang chủ
    homepage_path = "index.html"
    
    # Tạo bản sao lưu trước khi thực hiện thay đổi
    backup_file(homepage_path)
    
    try:
        # Đọc nội dung trang chủ
        with open(homepage_path, 'r', encoding='utf-8') as file:
            homepage_content = file.read()
        
        # Xác định các thay đổi cần khôi phục
        changes = []
        
        # 1. Khôi phục game "The Last Tiger: Tank Simulator" đã bị xóa
        tiger_pattern = r'<!-- The Last Tiger: Tank Simulator -->[\s\S]+?<a href="/go/the-last-tiger-tank-simulator\.html">'
        if re.search(tiger_pattern, homepage_content):
            confirm = input("\nPhát hiện game 'The Last Tiger: Tank Simulator' đã tồn tại. Bạn có muốn tạo phiên bản thứ hai để phục vụ demo lỗi không? (y/n): ")
            if confirm.lower() == 'y':
                # Tìm vị trí để thêm game
                match = re.search(tiger_pattern, homepage_content)
                if match:
                    pos = match.start()
                    # Tạo HTML cho phiên bản trùng lặp
                    duplicate_html = '''
<!-- The Last Tiger: Tank Simulator -->
<div class="col-lg-2 col-md-4 col-sm-6">
<div class="game-card">
<a href="/go/the-last-tiger:-tank-simulator.html">
<img alt="the-last-tiger:-tank-simulator" class="lazyload" data-src="/img/games/the-last-tiger-tank-simulator.jpg" decoding="async" loading="lazy" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="/>
<h3>The Last Tiger: Tank Simulator</h3>
<p>Play The Last Tiger: Tank Simulator now!</p>
</a>
</div>
</div>
'''
                    # Chèn phiên bản trùng lặp
                    homepage_content = homepage_content[:pos] + duplicate_html + homepage_content[pos:]
                    changes.append("Thêm phiên bản trùng lặp của The Last Tiger: Tank Simulator")
        else:
            print("  ⚠️ Không tìm thấy game 'The Last Tiger: Tank Simulator' trên trang chủ")
        
        # 2. Khôi phục hình ảnh "GT Burnout Parking Simulator" về tên cắt ngắn
        gt_pattern = r'data-src="/img/games/gt-burnout-parking-simulator\.jpg"'
        gt_replacement = r'data-src="/img/games/gt-burnout-parking-simulato.jpg"'
        
        if re.search(gt_pattern, homepage_content):
            confirm = input("\nPhát hiện đường dẫn hình ảnh 'GT Burnout Parking Simulator' đã được sửa. Bạn có muốn khôi phục về phiên bản lỗi không? (y/n): ")
            if confirm.lower() == 'y':
                homepage_content = re.sub(gt_pattern, gt_replacement, homepage_content)
                changes.append("Khôi phục hình ảnh GT Burnout Parking Simulator về tên cắt ngắn")
        
        # Ghi nội dung đã cập nhật vào file trang chủ nếu có thay đổi
        if changes:
            with open(homepage_path, 'w', encoding='utf-8') as file:
                file.write(homepage_content)
            
            print("\n✅ Đã khôi phục trang chủ với các thay đổi sau:")
            for change in changes:
                print(f"  - {change}")
        else:
            print("\n✅ Không có thay đổi nào được thực hiện")
        
        return True
    
    except Exception as e:
        print(f"\n⚠️ Lỗi khi khôi phục trang chủ: {str(e)}")
        return False

if __name__ == "__main__":
    restore_homepage() 