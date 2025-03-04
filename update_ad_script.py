#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import shutil
import time
from pathlib import Path

def find_html_files(start_dir):
    """Tìm tất cả các file HTML trong thư mục và các thư mục con"""
    html_files = []
    for path in Path(start_dir).rglob('*.html'):
        html_files.append(str(path))
    return html_files

def update_ad_script(html_file):
    """Cập nhật script quảng cáo trong file HTML (chỉ script JS, không có dns-prefetch)"""
    print(f"Đang xử lý file: {html_file}")
    
    if not os.path.isfile(html_file):
        print(f"  - File không tồn tại: {html_file}")
        return False
    
    try:
        # Đọc nội dung file
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # Script quảng cáo mới (chỉ JS, không có dns-prefetch)
        new_ad_script = '''<script type="text/javascript" async>!function(e,t){a=e.createElement("script"),m=e.getElementsByTagName("script")[0],a.async=1,a.src=t,a.fetchPriority='high',m.parentNode.insertBefore(a,m)}(document,"https://universal.wgplayer.com/tag/?lh="+window.location.hostname+"&wp="+window.location.pathname+"&ws="+window.location.search);</script>'''
        
        # Pattern để tìm cả dns-prefetch và script quảng cáo
        combined_pattern = re.compile(r'<link rel="dns-prefetch" href="https://universal\.wgplayer\.com"/>\s*(<script[^>]*>.*?wgplayer\.com/tag/.*?</script>)?', re.DOTALL)
        
        # Pattern để tìm chỉ script quảng cáo (không kèm dns-prefetch)
        script_only_pattern = re.compile(r'<script[^>]*>.*?wgplayer\.com/tag/.*?</script>', re.DOTALL)
        
        # Kiểm tra xem có dns-prefetch và script không
        combined_match = combined_pattern.search(content)
        
        # Kiểm tra xem chỉ có script không
        script_only_match = script_only_pattern.search(content)
        
        if combined_match:
            # Xóa cả dns-prefetch và script hiện tại, thay thế bằng script mới
            content = combined_pattern.sub(new_ad_script, content)
            modified = True
            print(f"  - Đã xóa dns-prefetch và cập nhật script quảng cáo")
        elif script_only_match and not combined_match:
            # Thay thế script hiện tại bằng script mới
            content = script_only_pattern.sub(new_ad_script, content)
            modified = True
            print(f"  - Đã cập nhật script quảng cáo")
        else:
            # Nếu không tìm thấy script quảng cáo nào, thêm script mới vào <head>
            head_pattern = re.compile(r'<head>', re.DOTALL)
            if head_pattern.search(content):
                content = head_pattern.sub(f'<head>\n\t{new_ad_script}', content)
                modified = True
                print(f"  - Đã thêm script quảng cáo mới")
            else:
                print(f"  - Không tìm thấy thẻ <head> trong file")
                return False
        
        # Nếu có thay đổi, lưu lại file
        if modified:
            # Tạo bản sao lưu
            backup_file = html_file + ".bak-" + str(int(time.time()))
            shutil.copy2(html_file, backup_file)
            print(f"  - Đã tạo bản sao lưu: {backup_file}")
            
            # Lưu nội dung đã sửa
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  - Đã sửa và lưu file: {html_file}")
            return True
        else:
            print(f"  - Không có thay đổi nào được thực hiện")
            return False
    
    except Exception as e:
        print(f"  - Lỗi khi xử lý file {html_file}: {str(e)}")
        return False

def main():
    # Kiểm tra có tham số dòng lệnh không
    if len(sys.argv) > 1:
        # Kiểm tra cờ --all hoặc -a
        if sys.argv[1] == '--all' or sys.argv[1] == '-a':
            print("Đang cập nhật script quảng cáo cho tất cả các file HTML...")
            # Lấy thư mục hiện tại
            current_dir = os.getcwd()
            html_files = find_html_files(current_dir)
            
            count_total = len(html_files)
            count_modified = 0
            
            for file_path in html_files:
                if update_ad_script(file_path):
                    count_modified += 1
            
            print(f"\nĐã xử lý {count_total} file, sửa đổi {count_modified} file.")
        else:
            # Nếu có tham số, sửa file cụ thể
            file_path = sys.argv[1]
            update_ad_script(file_path)
    else:
        # Nếu không có tham số, hiển thị hướng dẫn
        print("Sử dụng:\n")
        print("  python update_ad_script.py <file_path>    # Cập nhật script quảng cáo cho một file HTML cụ thể")
        print("  python update_ad_script.py --all          # Cập nhật script quảng cáo cho tất cả các file HTML")

if __name__ == "__main__":
    main() 