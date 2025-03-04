import os
import re
import glob
from pathlib import Path
import time

def fix_duplicate_wgplayer_scripts(html_file):
    """
    Kiểm tra và sửa các script WGPlayer trùng lặp trong file HTML.
    Trả về True nếu file đã được sửa, False nếu không cần sửa.
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Mẫu regex để tìm script WGPlayer
    wgplayer_pattern = r'<script type="text/javascript" async>!function\(e,t\)\{a=e\.createElement\("script"\),m=e\.getElementsByTagName\("script"\)\[0\],a\.async=1,a\.src=t,a\.fetchPriority=\'high\',m\.parentNode\.insertBefore\(a,m\)\}\(document,"https://universal\.wgplayer\.com/tag/\?lh="\+window\.location\.hostname\+"&wp="\+window\.location\.pathname\+"&ws="\+window\.location\.search\);</script>'
    
    # Đếm số lần script xuất hiện
    matches = re.findall(wgplayer_pattern, content)
    
    if len(matches) <= 1:
        return False  # Không cần sửa
    
    # Tạo bản sao lưu trước khi sửa
    backup_path = f"{html_file}.bak-wgplayer-fix-{int(time.time())}"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Thay thế tất cả các script trùng lặp bằng một script duy nhất
    first_occurrence = True
    fixed_content = ''
    for line in content.splitlines():
        if wgplayer_pattern in line:
            if first_occurrence:
                fixed_content += line + '\n'
                first_occurrence = False
            else:
                # Xóa script trùng lặp, giữ lại phần meta nếu có
                meta_part = line.split('</script>')
                if len(meta_part) > 1:
                    fixed_content += meta_part[1] + '\n'
        else:
            fixed_content += line + '\n'
    
    # Ghi nội dung đã sửa vào file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    return True

def main():
    # Tìm tất cả các file HTML
    html_files = glob.glob('**/*.html', recursive=True)
    
    fixed_count = 0
    skipped_count = 0
    
    for html_file in html_files:
        print(f'Đang kiểm tra: {html_file}')
        if fix_duplicate_wgplayer_scripts(html_file):
            print(f'Đã sửa: {html_file}')
            fixed_count += 1
        else:
            print(f'Không cần sửa: {html_file}')
            skipped_count += 1
    
    print(f'\nTổng kết:')
    print(f'- Đã sửa: {fixed_count} file')
    print(f'- Không cần sửa: {skipped_count} file')

if __name__ == "__main__":
    main() 