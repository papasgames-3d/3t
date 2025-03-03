import os
import re
import glob
from pathlib import Path

# Đường dẫn đến thư mục chứa các file HTML
html_dir = "go"

# Script để tải iframe sau khi trang đã tải hoặc khi người dùng tương tác
lazy_loading_script = """
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
"""

# Đếm số file đã xử lý
files_processed = 0
files_optimized = 0
already_optimized = []
error_files = []

# Lấy danh sách tất cả các file HTML trong thư mục
html_files = glob.glob(os.path.join(html_dir, "*.html"))

# Tổng số file cần xử lý
total_files = len(html_files)

print()  # Xuống dòng để dễ nhìn

# Xử lý từng file HTML
for html_file in html_files:
    files_processed += 1
    
    # Đọc nội dung file
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Kiểm tra xem file đã được tối ưu hóa chưa
    if 'data-src' in content and 'loadGameIframe' in content:
        print(f"File {os.path.basename(html_file)} đã được tối ưu hóa trước đó.")
        already_optimized.append(os.path.basename(html_file))
        continue
    
    # Tìm tất cả các thẻ iframe có thuộc tính src
    iframe_pattern = re.compile(r'<iframe.*?src=["\'](.*?)["\'].*?(?:/>|></iframe>|</iframe>)', re.DOTALL)
    iframe_match = iframe_pattern.search(content)
    
    if not iframe_match:
        print(f"Không tìm thấy iframe trong file: {os.path.basename(html_file)}")
        error_files.append(f"{os.path.basename(html_file)} - Không tìm thấy iframe")
        continue
    
    # Lấy URL của game từ thuộc tính src
    game_url = iframe_match.group(1)
    
    # Thay thế src thành data-src trong thẻ iframe
    modified_content = content.replace(
        f'src="{game_url}"', 
        f'data-src="{game_url}"'
    )
    
    # Tìm vị trí để thêm script tải trễ
    # Tìm thẻ script đầu tiên sau iframe hoặc thẻ đóng section
    script_pattern = re.compile(r'(</section>|</div>\s*<script>|<!-- End iframe Game -->)', re.DOTALL)
    script_match = script_pattern.search(modified_content, iframe_match.end())
    
    if script_match:
        # Thêm script tải trễ sau thẻ script hoặc section
        insert_pos = script_match.start()
        modified_content = (
            modified_content[:insert_pos] + 
            f"\n<script>{lazy_loading_script}</script>\n" + 
            modified_content[insert_pos:]
        )
        
        # Ghi nội dung đã sửa vào file
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        files_optimized += 1
        progress = (files_processed / total_files) * 100
        # print(f"[{progress:.1f}%] Đã tối ưu hóa: {os.path.basename(html_file)}")
    else:
        error_files.append(f"{os.path.basename(html_file)} - Không tìm thấy vị trí để thêm script")
        print(f"Không thể tìm thấy vị trí để thêm script trong: {os.path.basename(html_file)}")

# Hiển thị kết quả
print(f"\nKết quả: Đã tối ưu thành công {files_optimized}/{total_files} file.")
print(f"Số file đã được tối ưu trước đó: {len(already_optimized)}")
print(f"Số file gặp lỗi: {len(error_files)}")

if error_files:
    print("\nDanh sách file gặp lỗi:")
    for error_file in error_files:
        print(f"- {error_file}")

print("\nHoàn tất quá trình tối ưu hóa iframe!")