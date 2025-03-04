import os
import re
import glob
from pathlib import Path
import time
from bs4 import BeautifulSoup

def fix_cors_issues(html_file):
    """
    Thêm các meta tag và thuộc tính liên quan đến CORS vào các thẻ script và link
    để giảm thiểu lỗi và cảnh báo CORS/cookie cross-site
    """
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # Kiểm tra và thêm meta tag CORS nếu cần
        head = soup.find('head')
        if head:
            # Thêm meta tag để quản lý cookie SameSite
            cors_meta = soup.find('meta', attrs={'name': 'cookie-same-site'})
            if not cors_meta:
                cors_meta = soup.new_tag('meta')
                cors_meta['name'] = 'cookie-same-site'
                cors_meta['content'] = 'Lax'
                head.append(cors_meta)
                modified = True
            
            # Thêm meta tag cho CORS
            cors_policy = soup.find('meta', attrs={'http-equiv': 'Cross-Origin-Resource-Policy'})
            if not cors_policy:
                cors_policy = soup.new_tag('meta')
                cors_policy['http-equiv'] = 'Cross-Origin-Resource-Policy'
                cors_policy['content'] = 'same-site'
                head.append(cors_policy)
                modified = True
        
        # Thêm thuộc tính crossorigin cho các thẻ script và link từ domain khác
        for tag in soup.find_all(['script', 'link', 'img', 'iframe']):
            src_attr = 'src' if tag.name in ['script', 'img', 'iframe'] else 'href'
            src = tag.get(src_attr)
            
            if src and (src.startswith('http://') or src.startswith('https://')) and not tag.get('crossorigin'):
                # Không phải domain hiện tại
                if 'googleapis.com' in src or 'googletagmanager.com' in src:
                    # Google resources thường chấp nhận 'anonymous'
                    tag['crossorigin'] = 'anonymous'
                    modified = True
                elif 'wgplayer.com' in src:
                    # Đối với WGPlayer, sử dụng thuộc tính SameSite
                    tag['crossorigin'] = 'anonymous'
                    modified = True
        
        if modified:
            # Tạo file backup
            backup_file = f"{html_file}.cors.bak"
            if not os.path.exists(backup_file):
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Ghi nội dung đã sửa
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            print(f"Đã sửa CORS issues trong: {html_file}")
            return True
        
        return False
    
    except Exception as e:
        print(f"Lỗi khi xử lý file {html_file}: {str(e)}")
        return False

def main():
    # Tìm tất cả các file HTML
    html_files = glob.glob("**/*.html", recursive=True)
    
    print(f"Tìm thấy {len(html_files)} file HTML để kiểm tra")
    
    fixed_files_count = 0
    
    # Duyệt qua từng file và sửa nếu cần
    for html_file in html_files:
        if fix_cors_issues(html_file):
            fixed_files_count += 1
    
    print(f"\nTổng kết:")
    print(f"- Đã kiểm tra: {len(html_files)} file HTML")
    print(f"- Đã sửa: {fixed_files_count} file")
    print(f"- Không cần sửa: {len(html_files) - fixed_files_count} file")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nHoàn thành trong {time.time() - start_time:.2f} giây") 