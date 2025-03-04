import os
import re
import glob
from pathlib import Path
import time
import shutil

def add_quick_iframe_loader(html_file):
    """
    Thêm JavaScript để tải iframe game nhanh hơn, nhưng không thay đổi cấu trúc HTML.
    Giảm timeout từ 1000ms xuống khoảng 100ms và thêm trình xử lý sự kiện window.onload.
    """
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Kiểm tra xem file có chứa iframe với data-src không
    iframe_pattern = r'<iframe[^>]*data-src=["\']([^"\']+)["\'][^>]*>'
    has_iframe = re.search(iframe_pattern, content)
    
    if not has_iframe:
        print(f"Không tìm thấy iframe với data-src trong {html_file}")
        return False
    
    # Kiểm tra xem file có chứa hàm loadGameIframe không
    load_function_pattern = r'function\s+loadGameIframe\s*\(\s*\)\s*\{'
    has_load_function = re.search(load_function_pattern, content)
    
    if not has_load_function:
        print(f"Không tìm thấy hàm loadGameIframe trong {html_file}")
        return False
    
    # Tạo bản sao lưu nếu chưa có
    backup_file = html_file + '.new_fix.bak'
    if not os.path.exists(backup_file):
        shutil.copy2(html_file, backup_file)
    
    # Thêm JavaScript để tải iframe nhanh hơn
    # Tìm vị trí đóng tag script sau function loadGameIframe
    script_end_pattern = r'(// Load game iframe after page loads or user interaction.*?setTimeout\(function\(\) \{\s*loadGameIframe\(\);\s*\}, )1000(.*?</script>)'
    
    if re.search(script_end_pattern, content, re.DOTALL):
        # Giảm timeout từ 1000ms xuống 100ms
        modified_content = re.sub(
            script_end_pattern,
            r'\g<1>100\g<2>',
            content,
            flags=re.DOTALL
        )
        
        # Thêm window.onload handler trước </script> cuối cùng
        onload_script = """
// Also load when window is fully loaded
window.addEventListener('load', function() {
    setTimeout(loadGameIframe, 50);
});
</script>"""
        
        modified_content = re.sub(
            r'</script>(?![^<]*</script>)',
            onload_script,
            modified_content,
            count=1
        )
        
        # Ghi nội dung đã sửa đổi vào file
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        print(f"Đã thêm quick iframe loader vào {html_file}")
        return True
    else:
        print(f"Không thể tìm thấy vị trí để thêm quick iframe loader trong {html_file}")
        return False

def main():
    # Tìm tất cả các file HTML trong thư mục
    html_files = glob.glob("**/*.html", recursive=True)
    
    modified_count = 0
    skipped_count = 0
    
    start_time = time.time()
    
    for html_file in html_files:
        if add_quick_iframe_loader(html_file):
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