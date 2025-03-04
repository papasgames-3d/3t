#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
from pathlib import Path
import shutil
import time

# Regex patterns để tìm các vấn đề
fullscreen_btn_pattern = re.compile(r'<a[^>]*id="fullscreen-btn"[^>]*href="javascript:openFullscreen\(\);"[^>]*>')
iframe_pattern = re.compile(r'<iframe[^>]*\s+(?:src|data-src)=["\']([^"\']+)["\'][^>]*>')
iframe_src_pattern = re.compile(r'<iframe([^>]*)\s+src=["\']([^"\']+)["\']([^>]*)>')
broken_script_pattern = re.compile(r'<script>\s*"\s*src="\${gameUrl}".*?</script>', re.DOTALL)
open_fullscreen_func_pattern = re.compile(r'function\s+openFullscreen\s*\(\s*\)\s*{[^}]*}', re.DOTALL)
load_iframe_func_pattern = re.compile(r'function\s+loadGameIframe\s*\(\s*\)\s*{[^}]*}', re.DOTALL)

# Pattern cho script wgplayer (để sửa lỗi preload)
wgplayer_script_pattern = re.compile(r'<link rel="dns-prefetch" href="https://universal\.wgplayer\.com"/><script[^>]*>[^<]*universal\.wgplayer\.com[^<]*</script>')

# Script mẫu để thay thế hoặc thêm mới
correct_script_template = """
<script>
// Load game iframe after page loads or user interaction
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        loadGameIframe();
    }, 1000); // Đợi 1 giây sau khi trang tải xong
});

document.addEventListener('click', function() {
    loadGameIframe();
}, { once: true }); // Chỉ gọi một lần khi người dùng tương tác đầu tiên

function loadGameIframe() {
    var gameIframe = document.querySelector('iframe[data-src]');
    if (gameIframe && !gameIframe.src) {
        gameIframe.src = gameIframe.getAttribute('data-src');
        console.log('Game iframe loaded');
    }
}

function openFullscreen() {
    // Đảm bảo iframe đã được load trước khi vào chế độ toàn màn hình
    loadGameIframe();
    
    let elem = document.getElementById("game-arena");
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { /* Safari */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE11 */
        elem.msRequestFullscreen();
    }
}
</script>
"""

# Script mới cho việc tải quảng cáo
ad_loader_script = """<link rel="dns-prefetch" href="https://universal.wgplayer.com"/>
<script src="/js/ad-loader.js"></script>
<script>
// Sử dụng ad-loader để tải script quảng cáo thay vì inline script
document.addEventListener('DOMContentLoaded', function() {
    if (window.adLoader) {
        window.adLoader.loadWgPlayerScript();
    }
});
</script>"""

def convert_src_to_data_src(content):
    """Chuyển đổi thuộc tính src thành data-src trong các iframe"""
    return iframe_src_pattern.sub(r'<iframe\1 data-src="\2"\3>', content)

def fix_wgplayer_script(content):
    """Sửa lỗi preload từ script wgplayer"""
    # Kiểm tra nếu file có chứa script wgplayer
    match = wgplayer_script_pattern.search(content)
    if match:
        print(f"  - Tìm thấy script wgplayer, thay thế bằng cách tải qua ad-loader.js")
        # In ra để debug
        print(f"  - Script wgplayer tìm thấy: {match.group(0)[:100]}...")
        # Thay thế script wgplayer bằng link đến ad-loader.js
        return wgplayer_script_pattern.sub(ad_loader_script, content)
    return content

def check_and_fix_file(html_file):
    """Kiểm tra và sửa chữa các vấn đề trong một file HTML cụ thể"""
    print(f"Đang kiểm tra file: {html_file}")
    
    # Đảm bảo file tồn tại
    if not os.path.isfile(html_file):
        print(f"  - File không tồn tại: {html_file}")
        return False
    
    # Bỏ qua file index.html vì đã được sửa
    if os.path.basename(html_file) == "index.html":
        print(f"  - Bỏ qua file index.html (đã được sửa)")
        return False
    
    try:
        # Đọc nội dung file
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        issues_found = False
        
        # Sửa lỗi preload từ script wgplayer
        new_content = fix_wgplayer_script(content)
        if new_content != content:
            content = new_content
            issues_found = True
            print(f"  - Đã thay thế script wgplayer bằng ad-loader.js")
        
        # Chuyển đổi src thành data-src trong iframe
        if 'src=' in content and '<iframe' in content:
            print(f"  - Kiểm tra thuộc tính src trong iframe")
            new_content = convert_src_to_data_src(content)
            if new_content != content:
                print(f"  - Đang chuyển đổi src thành data-src trong iframe")
                content = new_content
                issues_found = True
        
        # Kiểm tra xem file có iframe không
        iframe_match = iframe_pattern.search(content)
        if iframe_match:
            print(f"  - Tìm thấy iframe")
            
            # Kiểm tra xem file có nút fullscreen không
            if fullscreen_btn_pattern.search(content):
                print(f"  - Tìm thấy nút fullscreen")
                
                # Kiểm tra script bị hỏng
                if broken_script_pattern.search(content):
                    print(f"  - Tìm thấy script bị hỏng, đang sửa...")
                    content = broken_script_pattern.sub('', content)
                    issues_found = True
                
                # Kiểm tra hàm openFullscreen() có tồn tại không
                open_fullscreen_exists = open_fullscreen_func_pattern.search(content)
                load_iframe_exists = load_iframe_func_pattern.search(content)
                
                if not open_fullscreen_exists:
                    print(f"  - Không tìm thấy hàm openFullscreen(), đang thêm...")
                    issues_found = True
                elif not load_iframe_exists:
                    print(f"  - Không tìm thấy hàm loadGameIframe(), đang thêm...")
                    issues_found = True
                elif "loadGameIframe();" not in open_fullscreen_exists.group(0):
                    print(f"  - Hàm openFullscreen() không gọi loadGameIframe(), đang sửa...")
                    # Thay thế hàm openFullscreen cũ bằng phiên bản mới
                    content = open_fullscreen_func_pattern.sub('', content)
                    issues_found = True
                
                # Nếu tìm thấy vấn đề, thêm script đúng sau thẻ iframe
                if issues_found:
                    if load_iframe_exists and open_fullscreen_exists:
                        # Xóa các hàm cũ
                        content = load_iframe_func_pattern.sub('', content)
                        content = open_fullscreen_func_pattern.sub('', content)
                    
                    # Tìm vị trí thích hợp để thêm script mới
                    updated_iframe_match = iframe_pattern.search(content)
                    if updated_iframe_match:
                        iframe_end_pos = updated_iframe_match.end()
                        # Tìm đến thẻ đóng div của game-arena (hoặc phần tử cha gần nhất)
                        div_end_pos = content.find('</div>', iframe_end_pos)
                        if div_end_pos != -1:
                            # Thêm script sau thẻ đóng div
                            content = content[:div_end_pos+6] + correct_script_template + content[div_end_pos+6:]
                
                # Nếu có thay đổi, lưu lại file
                if content != original_content:
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
                    print(f"  - Không cần sửa đổi: {html_file}")
            else:
                print(f"  - Không tìm thấy nút fullscreen")
                # Nếu đã thay đổi iframe từ src sang data-src hoặc sửa script wgplayer
                if content != original_content:
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
            # Kiểm tra nếu không có iframe nhưng có script wgplayer cần sửa
            if content != original_content:
                # Tạo bản sao lưu
                backup_file = html_file + ".bak-" + str(int(time.time()))
                shutil.copy2(html_file, backup_file)
                print(f"  - Đã tạo bản sao lưu: {backup_file}")
                
                # Lưu nội dung đã sửa
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  - Đã sửa script wgplayer và lưu file: {html_file}")
                return True
            else:
                print(f"  - Không tìm thấy iframe, bỏ qua")
        
        return False
    
    except Exception as e:
        print(f"  - Lỗi khi xử lý file {html_file}: {str(e)}")
        return False

def scan_directory(directory):
    """Quét một thư mục và trả về danh sách các file HTML"""
    html_files = []
    
    if not os.path.isdir(directory):
        print(f"Thư mục không tồn tại: {directory}")
        return html_files
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    return html_files

def scan_and_fix_directories():
    """Quét nhiều thư mục và sửa chữa tất cả các file HTML trong đó"""
    fixed_count = 0
    error_count = 0
    scanned_count = 0
    ads_fixed_count = 0
    
    # Danh sách thư mục cần quét
    directories = [".", "go"]
    
    all_html_files = []
    
    # Thu thập tất cả các file HTML từ các thư mục
    for directory in directories:
        print(f"Đang quét thư mục: {directory}")
        directory_files = scan_directory(directory)
        print(f"Tìm thấy {len(directory_files)} file HTML trong thư mục {directory}")
        all_html_files.extend(directory_files)
    
    print(f"\nTổng cộng: {len(all_html_files)} file HTML để kiểm tra")
    
    # Xử lý từng file
    for html_file in all_html_files:
        scanned_count += 1
        try:
            if check_and_fix_file(html_file):
                fixed_count += 1
                # Kiểm tra nếu fixed vì quảng cáo
                with open(html_file, 'r', encoding='utf-8') as f:
                    if "ad-loader.js" in f.read():
                        ads_fixed_count += 1
        except Exception as e:
            print(f"Lỗi khi xử lý file {html_file}: {str(e)}")
            error_count += 1
    
    print("\nKết quả:")
    print(f"- Đã quét: {scanned_count} file HTML")
    print(f"- Đã sửa: {fixed_count} file")
    print(f"- Đã sửa lỗi quảng cáo: {ads_fixed_count} file")
    print(f"- Số lỗi: {error_count} file")

def fix_specific_file(file_path):
    """Sửa một file cụ thể"""
    if os.path.exists(file_path):
        print(f"Đang sửa file cụ thể: {file_path}")
        try:
            # Đọc nội dung file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"Đã đọc nội dung file: {len(content)} ký tự")
            
            # Kiểm tra script wgplayer
            if 'universal.wgplayer.com' in content:
                print(f"Tìm thấy script wgplayer trong file")
                
                # In ra đoạn có chứa script wgplayer để debug
                match = re.search(r'<link[^>]*universal\.wgplayer\.com[^>]*>[^<]*<script[^>]*>[^<]*universal\.wgplayer\.com[^<]*</script>', content)
                if match:
                    print(f"Script wgplayer tìm thấy: {match.group(0)[:100]}...")
                
                new_content = fix_wgplayer_script(content)
                if new_content != content:
                    print(f"Đã sửa script wgplayer")
                    # Lưu nội dung đã sửa
                    backup_file = file_path + ".bak-" + str(int(time.time()))
                    shutil.copy2(file_path, backup_file)
                    print(f"Đã tạo bản sao lưu: {backup_file}")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Đã lưu nội dung đã sửa")
                    return True
                else:
                    print(f"Không thể thay thế script wgplayer")
            
            # Kiểm tra xem file có iframe không
            if '<iframe' in content:
                print(f"Tìm thấy thẻ iframe trong file")
                
                # Kiểm tra thuộc tính src
                if 'src=' in content and 'data-src=' not in content:
                    print(f"File có iframe với thuộc tính src nhưng không có data-src")
                    
                    # Chuyển đổi src thành data-src
                    new_content = convert_src_to_data_src(content)
                    if new_content != content:
                        print(f"Đã chuyển đổi src thành data-src")
                        
                        # Tạo bản sao lưu
                        backup_file = file_path + ".bak-" + str(int(time.time()))
                        shutil.copy2(file_path, backup_file)
                        print(f"Đã tạo bản sao lưu: {backup_file}")
                        
                        # Lưu nội dung đã sửa
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Đã lưu nội dung đã sửa")
                        return True
                    else:
                        print(f"Không thể chuyển đổi src thành data-src")
                else:
                    print(f"File không cần chuyển đổi src thành data-src")
            else:
                print(f"Không tìm thấy thẻ iframe trong file")
            
            if check_and_fix_file(file_path):
                print(f"Đã sửa file thành công: {file_path}")
                return True
            else:
                print(f"Không cần sửa hoặc không thể sửa file: {file_path}")
                return False
        except Exception as e:
            print(f"Lỗi khi xử lý file {file_path}: {str(e)}")
            return False
    else:
        print(f"File không tồn tại: {file_path}")
        return False

if __name__ == "__main__":
    # Kiểm tra có tham số dòng lệnh không
    if len(sys.argv) > 1:
        # Nếu có tham số, sửa file cụ thể
        file_path = sys.argv[1]
        fix_specific_file(file_path)
    else:
        # Nếu không có tham số, quét và sửa tất cả các file
        scan_and_fix_directories() 