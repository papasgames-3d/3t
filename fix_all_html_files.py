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

def fix_html_file(html_file):
    """Sửa lỗi cú pháp JavaScript và iframe trong file HTML"""
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
        
        # Mẫu JavaScript hoàn chỉnh và đúng cú pháp cho openFullscreen() và loadGameIframe()
        correct_script = """<script>
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

function loadGameIframe() {
    var gameIframe = document.querySelector('iframe[data-src]');
    if (gameIframe && !gameIframe.src) {
        gameIframe.src = gameIframe.getAttribute('data-src');
        console.log('Game iframe loaded');
    }
}

// Load game iframe after page loads or user interaction
document.addEventListener('DOMContentLoaded', function() {
    // Delayed loading to allow ads to load first
    setTimeout(function() {
        loadGameIframe();
    }, 1000); // Adjust timing as needed
    
    // Alternatively, load on first user interaction
    document.addEventListener('click', function loadOnFirstInteraction() {
        loadGameIframe();
        document.removeEventListener('click', loadOnFirstInteraction);
    }, {once: true});
});
</script>"""

        # Sửa 1: Kiểm tra và sửa đoạn script bị hỏng xung quanh iframe
        iframe_section_pattern = re.compile(r'<div data-url="[^"]*" id="game-arena">.*?</section>', re.DOTALL)
        iframe_match = iframe_section_pattern.search(content)
        
        if iframe_match:
            # Lấy đoạn mã HTML chứa iframe và phần điều khiển
            iframe_section = iframe_match.group(0)
            
            # Kiểm tra xem có script lỗi không
            broken_script_pattern = re.compile(r'<script>.*?else if \(elem\..*?</script>', re.DOTALL)
            if broken_script_pattern.search(iframe_section):
                # Loại bỏ tất cả các đoạn script hiện tại
                iframe_section_clean = re.sub(r'<script>.*?</script>', '', iframe_section, flags=re.DOTALL)
                
                # Tìm vị trí để thêm script mới
                iframe_pattern = re.compile(r'<iframe.*?</iframe>', re.DOTALL)
                iframe_match = iframe_pattern.search(iframe_section_clean)
                
                if iframe_match:
                    iframe_end_pos = iframe_match.end()
                    
                    # Tạo đoạn mã mới với script đúng
                    new_iframe_section = iframe_section_clean[:iframe_end_pos] + "\n" + correct_script + iframe_section_clean[iframe_end_pos:]
                    
                    # Thay thế đoạn cũ bằng đoạn mới trong nội dung gốc
                    content = content.replace(iframe_section, new_iframe_section)
                    modified = True
                    print(f"  - Đã sửa script lỗi xung quanh iframe")
        
        # Sửa 2: Chuyển src thành data-src trong các iframe
        iframe_src_pattern = re.compile(r'<iframe([^>]*) src="([^"]*)"([^>]*)>', re.DOTALL)
        iframe_src_matches = list(iframe_src_pattern.finditer(content))
        
        if iframe_src_matches:
            for match in reversed(iframe_src_matches):  # Xử lý từ cuối lên để không ảnh hưởng đến vị trí các match khác
                # Kiểm tra xem iframe này đã có data-src chưa
                if 'data-src=' not in match.group(0):
                    # Thay thế src bằng data-src
                    new_iframe = f'<iframe{match.group(1)} data-src="{match.group(2)}"{match.group(3)}>'
                    content = content[:match.start()] + new_iframe + content[match.end():]
                    modified = True
                    print(f"  - Đã chuyển src thành data-src trong iframe")
        
        # Sửa 3: Thêm ad-loader.js nếu chưa có và thay thế script quảng cáo inline
        ad_loader_pattern = re.compile(r'<script src="/js/ad-loader\.js"></script>', re.DOTALL)
        wgplayer_inline_pattern = re.compile(r'<script>[^<]*universal\.wgplayer\.com[^<]*</script>', re.DOTALL)
        
        head_tag_pattern = re.compile(r'<head>.*?</head>', re.DOTALL)
        head_match = head_tag_pattern.search(content)
        
        if head_match and wgplayer_inline_pattern.search(content) and not ad_loader_pattern.search(content):
            # Thêm ad-loader.js vào <head>
            head_content = head_match.group(0)
            new_head_content = head_content.replace('<head>', '''<head>
\t<link rel="dns-prefetch" href="https://universal.wgplayer.com"/>
<script src="/js/ad-loader.js"></script>
<script>
// Sử dụng ad-loader để tải script quảng cáo thay vì inline script
document.addEventListener('DOMContentLoaded', function() {
    if (window.adLoader) {
        window.adLoader.loadWgPlayerScript();
    }
});
</script>''')
            
            content = content.replace(head_content, new_head_content)
            
            # Xóa script inline wgplayer
            content = wgplayer_inline_pattern.sub('', content)
            modified = True
            print(f"  - Đã thêm ad-loader.js và xóa script inline")
        
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
        
        return modified
    
    except Exception as e:
        print(f"  - Lỗi khi xử lý file {html_file}: {str(e)}")
        return False

def main():
    # Kiểm tra có tham số dòng lệnh không
    if len(sys.argv) > 1:
        # Kiểm tra cờ --all hoặc -a
        if sys.argv[1] == '--all' or sys.argv[1] == '-a':
            print("Đang sửa tất cả các file HTML...")
            # Lấy thư mục hiện tại
            current_dir = os.getcwd()
            html_files = find_html_files(current_dir)
            
            count_total = len(html_files)
            count_modified = 0
            
            for file_path in html_files:
                if fix_html_file(file_path):
                    count_modified += 1
            
            print(f"\nĐã xử lý {count_total} file, sửa đổi {count_modified} file.")
        else:
            # Nếu có tham số, sửa file cụ thể
            file_path = sys.argv[1]
            fix_html_file(file_path)
    else:
        # Nếu không có tham số, hiển thị hướng dẫn
        print("Sử dụng:\n")
        print("  python fix_all_html_files.py <file_path>    # Sửa một file HTML cụ thể")
        print("  python fix_all_html_files.py --all          # Sửa tất cả các file HTML")

if __name__ == "__main__":
    main() 