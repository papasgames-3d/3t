import os
import re
import glob
from pathlib import Path
import time

def add_ad_loader_script(html_file):
    """
    Thêm thẻ script ad-loader.js vào các file HTML nếu chưa có.
    Trả về True nếu file đã được sửa, False nếu không cần sửa.
    """
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Kiểm tra xem file đã có ad-loader chưa
    if 'src="/js/ad-loader.js"' in content or "src='/js/ad-loader.js'" in content:
        return False  # Đã có script ad-loader
    
    # Tạo bản sao lưu trước khi sửa
    backup_path = f"{html_file}.bak-adloader-{int(time.time())}"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Tìm vị trí sau thẻ <head> để thêm script
    head_pattern = r'<head[^>]*>'
    head_match = re.search(head_pattern, content)
    
    if not head_match:
        return False  # Không tìm thấy thẻ head
    
    head_end = head_match.end()
    
    # Chuẩn bị script ad-loader
    ad_loader_script = '\n\t<!-- Ad Loader Script -->\n\t<script src="/js/ad-loader.js" defer></script>\n'
    
    # Chèn script vào sau thẻ <head>
    new_content = content[:head_end] + ad_loader_script + content[head_end:]
    
    # Ghi nội dung đã sửa vào file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    # Tìm tất cả các file HTML
    html_files = glob.glob('**/*.html', recursive=True)
    
    modified_count = 0
    skipped_count = 0
    
    for html_file in html_files:
        print(f'Đang kiểm tra: {html_file}')
        
        # Thêm script ad-loader
        if add_ad_loader_script(html_file):
            print(f'Đã thêm ad-loader script vào: {html_file}')
            modified_count += 1
        else:
            print(f'Bỏ qua (đã có hoặc không cần): {html_file}')
            skipped_count += 1
    
    print(f'\nTổng kết:')
    print(f'- Đã thêm ad-loader script: {modified_count} file')
    print(f'- Bỏ qua: {skipped_count} file')

if __name__ == "__main__":
    main() 