#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import shutil
import time

def fix_cookie_clicker_html(html_file):
    """Sửa lỗi cú pháp JavaScript trong file cookie-clicker.html"""
    print(f"Đang sửa file: {html_file}")
    
    if not os.path.isfile(html_file):
        print(f"  - File không tồn tại: {html_file}")
        return False
    
    try:
        # Đọc nội dung file
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Mẫu JavaScript hoàn chỉnh và đúng cú pháp
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

        # Tìm và thay thế tất cả các đoạn script bị hỏng
        iframe_section_pattern = re.compile(r'<div data-url="[^"]*" id="game-arena">.*?</section>', re.DOTALL)
        iframe_match = iframe_section_pattern.search(content)
        
        if iframe_match:
            # Lấy đoạn mã HTML chứa iframe và phần điều khiển
            iframe_section = iframe_match.group(0)
            
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
                print(f"  - Không có thay đổi nào được thực hiện")
        else:
            print(f"  - Không tìm thấy phần iframe game")
        
        return False
    
    except Exception as e:
        print(f"  - Lỗi khi xử lý file {html_file}: {str(e)}")
        return False

if __name__ == "__main__":
    # Kiểm tra có tham số dòng lệnh không
    if len(sys.argv) > 1:
        # Nếu có tham số, sửa file cụ thể
        file_path = sys.argv[1]
        fix_cookie_clicker_html(file_path)
    else:
        # Nếu không có tham số, sửa file cookie-clicker.html mặc định
        fix_cookie_clicker_html("go/cookie-clicker.html") 