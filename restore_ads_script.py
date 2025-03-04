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

def restore_original_ad_script(html_file):
    """Khôi phục lại script quảng cáo ban đầu trong file HTML"""
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
        
        # Script quảng cáo ban đầu (không bao gồm dns-prefetch)
        original_ad_script = '''<script type="text/javascript" async>!function(e,t){a=e.createElement("script"),m=e.getElementsByTagName("script")[0],a.async=1,a.src=t,a.fetchPriority='high',m.parentNode.insertBefore(a,m)}(document,"https://universal.wgplayer.com/tag/?lh="+window.location.hostname+"&wp="+window.location.pathname+"&ws="+window.location.search);</script>'''
        
        # Kiểm tra và xóa các dns-prefetch trùng lặp 
        dns_prefetch_tag = '<link rel="dns-prefetch" href="https://universal.wgplayer.com"/>'
        dns_prefetch_pattern = re.compile(r'<link rel="dns-prefetch" href="https://universal\.wgplayer\.com"/>', re.DOTALL)
        
        # Đếm số lượng thẻ dns-prefetch hiện có
        dns_prefetch_count = len(dns_prefetch_pattern.findall(content))
        
        # Nếu có nhiều hơn 1 thẻ dns-prefetch, xóa tất cả trừ thẻ đầu tiên
        if dns_prefetch_count > 1:
            # Tìm vị trí của thẻ dns-prefetch đầu tiên
            first_match = dns_prefetch_pattern.search(content)
            if first_match:
                first_pos = first_match.start()
                # Xóa tất cả các thẻ dns-prefetch
                content = dns_prefetch_pattern.sub('', content)
                # Thêm lại một thẻ dns-prefetch vào đầu head
                head_pattern = re.compile(r'<head>', re.DOTALL)
                content = head_pattern.sub(f'<head>\n\t{dns_prefetch_tag}', content)
                modified = True
                print(f"  - Đã xóa {dns_prefetch_count-1} thẻ dns-prefetch trùng lặp")
        
        # Kiểm tra xem có dns-prefetch chưa
        dns_prefetch_exists = dns_prefetch_pattern.search(content)
        
        # Kiểm tra và loại bỏ reference đến ad-loader.js
        ad_loader_pattern = re.compile(r'<script src="/js/ad-loader\.js"></script>', re.DOTALL)
        if ad_loader_pattern.search(content):
            content = ad_loader_pattern.sub('', content)
            modified = True
            print(f"  - Đã xóa tham chiếu đến ad-loader.js")
        
        # Xóa script đã thêm để sử dụng ad-loader
        ad_loader_usage_pattern = re.compile(r'<script>\s*// Sử dụng ad-loader để tải script quảng cáo.*?</script>', re.DOTALL)
        if ad_loader_usage_pattern.search(content):
            content = ad_loader_usage_pattern.sub('', content)
            modified = True
            print(f"  - Đã xóa script sử dụng ad-loader")
        
        # Kiểm tra xem đã có script quảng cáo ban đầu chưa
        original_ad_script_pattern = re.compile(r'<script[^>]*>.*?wgplayer\.com/tag/.*?</script>', re.DOTALL)
        
        head_tag_pattern = re.compile(r'<head>.*?</head>', re.DOTALL)
        head_match = head_tag_pattern.search(content)
        
        if head_match and not original_ad_script_pattern.search(content):
            # Thêm script quảng cáo ban đầu vào <head>
            head_content = head_match.group(0)
            
            # Nếu chưa có dns-prefetch, thêm vào cùng với script quảng cáo
            if not dns_prefetch_exists:
                new_head_content = head_content.replace('<head>', f'<head>\n\t{dns_prefetch_tag}\n\t{original_ad_script}\n')
            else:
                # Nếu đã có dns-prefetch, chỉ thêm script quảng cáo
                new_head_content = head_content.replace('<head>', f'<head>\n\t{original_ad_script}\n')
            
            content = content.replace(head_content, new_head_content)
            modified = True
            print(f"  - Đã thêm script quảng cáo ban đầu")
        
        # Nếu có thay đổi, lưu lại file
        if modified:
            # Tạo bản sao lưu
            backup_file = html_file + ".bak-restore-" + str(int(time.time()))
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
            print("Đang khôi phục script quảng cáo ban đầu cho tất cả các file HTML...")
            # Lấy thư mục hiện tại
            current_dir = os.getcwd()
            html_files = find_html_files(current_dir)
            
            count_total = len(html_files)
            count_modified = 0
            
            for file_path in html_files:
                if restore_original_ad_script(file_path):
                    count_modified += 1
            
            print(f"\nĐã xử lý {count_total} file, sửa đổi {count_modified} file.")
        else:
            # Nếu có tham số, sửa file cụ thể
            file_path = sys.argv[1]
            restore_original_ad_script(file_path)
    else:
        # Nếu không có tham số, hiển thị hướng dẫn
        print("Sử dụng:\n")
        print("  python restore_ads_script.py <file_path>    # Khôi phục script quảng cáo ban đầu cho một file HTML cụ thể")
        print("  python restore_ads_script.py --all          # Khôi phục script quảng cáo ban đầu cho tất cả các file HTML")

if __name__ == "__main__":
    main() 