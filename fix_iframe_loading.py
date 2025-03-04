import os
import re
import glob
from pathlib import Path
import time
import shutil

def fix_iframe_loading(html_file):
    """
    Sửa đổi cách tải iframe game để nó hiển thị ngay lập tức.
    1. Thay đổi iframe từ data-src thành src trực tiếp
    2. Điều chỉnh script loadGameIframe để tải iframe ngay lập tức
    """
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Kiểm tra xem file có chứa iframe với data-src không
    iframe_pattern = r'<iframe[^>]*data-src=["\']([^"\']+)["\'][^>]*>'
    has_iframe = re.search(iframe_pattern, content)
    
    if not has_iframe:
        print(f"Không tìm thấy iframe với data-src trong {html_file}")
        return False
    
    # Tạo bản sao lưu
    backup_file = html_file + '.bak'
    if not os.path.exists(backup_file):
        shutil.copy2(html_file, backup_file)
    
    # 1. Thay thế data-src bằng src trong iframe
    modified_content = re.sub(
        r'<iframe([^>]*)data-src=(["\'])([^"\']+)(\2)([^>]*)>',
        r'<iframe\1src=\2\3\4\5>',
        content
    )
    
    # 2. Sửa đổi script loadGameIframe để tải ngay lập tức
    script_pattern = r'document\.addEventListener\(\'DOMContentLoaded\', function\(\) \{\s*// Delayed loading to allow ads to load first\s*setTimeout\(function\(\) \{\s*loadGameIframe\(\);\s*\}, 1000\);'
    
    modified_content = re.sub(
        script_pattern,
        r'document.addEventListener(\'DOMContentLoaded\', function() {\n    // Load iframe immediately\n    loadGameIframe();',
        modified_content
    )
    
    # Thêm autoplay cho iframe nếu cần
    modified_content = re.sub(
        r'<iframe([^>]*)src=(["\'])([^"\']+)(\2)([^>]*)>',
        r'<iframe\1src=\2\3\4 allow="autoplay"\5>',
        modified_content
    )
    
    # Ghi nội dung đã sửa đổi vào file
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(modified_content)
    
    print(f"Đã sửa iframe loading trong {html_file}")
    return True

def main():
    # Tìm tất cả các file HTML trong thư mục
    html_files = glob.glob("**/*.html", recursive=True)
    
    modified_count = 0
    skipped_count = 0
    
    start_time = time.time()
    
    for html_file in html_files:
        if fix_iframe_loading(html_file):
            modified_count += 1
        else:
            skipped_count += 1
    
    end_time = time.time()
    
    print(f"\nTổng kết:")
    print(f"- Thời gian thực hiện: {end_time - start_time:.2f} giây")
    print(f"- Số file đã sửa: {modified_count}")
    print(f"- Số file bỏ qua: {skipped_count}")

if __name__ == "__main__":
    main() 