#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# canonical_updater.py - Script tự động thêm/cập nhật thẻ canonical cho tất cả file HTML

import os
import re
from datetime import datetime

# Cấu hình
BASE_URL = "https://monkeymart.one"  # URL gốc của website
BACKUP_FOLDER = "_canonical_backup"  # Thư mục sao lưu

def create_backup(file_path):
    """Tạo bản sao lưu của file trước khi sửa đổi"""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUP_FOLDER
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    filename = os.path.basename(file_path)
    backup_path = os.path.join(backup_dir, f"{filename}_{now}.bak")
    
    with open(file_path, 'r', encoding='utf-8') as original:
        with open(backup_path, 'w', encoding='utf-8') as backup:
            backup.write(original.read())
    return backup_path

def update_canonical(file_path):
    """Cập nhật hoặc thêm thẻ canonical cho file HTML"""
    # Tạo bản sao lưu
    backup_path = create_backup(file_path)
    
    # Đọc nội dung file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Xác định canonical URL dựa trên đường dẫn tương đối
    rel_path = os.path.normpath(os.path.relpath(file_path, '.'))
    
    # Xử lý trường hợp đặc biệt
    if rel_path == "index.html" or rel_path == ".\\index.html" or rel_path == "./index.html":
        canonical_url = BASE_URL
    elif rel_path.endswith("index.html"):
        # Xử lý index.html trong thư mục con (ví dụ: category/index.html)
        dir_path = os.path.dirname(rel_path).replace('\\', '/')
        canonical_url = f"{BASE_URL}/{dir_path}/"
    else:
        # Chuẩn hóa đường dẫn cho các file khác
        rel_path = rel_path.replace('\\', '/')
        if rel_path.startswith('./'):
            rel_path = rel_path[2:]
        canonical_url = f"{BASE_URL}/{rel_path}"
    
    # Kiểm tra và cập nhật thẻ canonical
    canonical_pattern = r'<link\s+rel="canonical"\s+href="[^"]*"'
    
    original_content = content
    if re.search(canonical_pattern, content):
        # Nếu đã có, cập nhật
        content = re.sub(canonical_pattern, f'<link rel="canonical" href="{canonical_url}"', content)
        status = "Đã cập nhật"
    else:
        # Nếu chưa có, thêm mới trước </head>
        head_end = "</head>"
        if head_end in content:
            canonical_tag = f'    <link rel="canonical" href="{canonical_url}" />\n    '
            content = content.replace(head_end, canonical_tag + head_end)
            status = "Đã thêm mới"
        else:
            status = "LỖI: Không tìm thấy </head>"
    
    # Nếu không có thay đổi, không cần lưu lại
    if content == original_content:
        status = "Không thay đổi"
        return rel_path, canonical_url, status, backup_path
    
    # Lưu lại file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return rel_path, canonical_url, status, backup_path

def find_and_update_html_files(directory='.'):
    """Tìm và cập nhật tất cả file HTML trong thư mục"""
    print(f"\n=== BẮT ĐẦU CẬP NHẬT CANONICAL URLS (BASE URL: {BASE_URL}) ===")
    print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Thư mục đang xử lý: {os.path.abspath(directory)}")
    print(f"Đã tạo thư mục sao lưu: {os.path.abspath(BACKUP_FOLDER)}")
    print("\nĐang quét tìm file HTML...")
    
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Đã tìm thấy {len(html_files)} file HTML")
    
    # Tạo bảng summary
    summary = []
    
    # Ưu tiên xử lý trang index.html trước
    index_path = os.path.join(directory, "index.html")
    if os.path.exists(index_path):
        print("\nĐang xử lý trang chủ index.html...")
        result = update_canonical(index_path)
        summary.append(result)
        if index_path in html_files:
            html_files.remove(index_path)
    
    # Xử lý các file còn lại
    print(f"\nĐang xử lý {len(html_files)} file HTML còn lại...")
    for file_path in sorted(html_files):
        result = update_canonical(file_path)
        summary.append(result)
    
    # In bảng summary
    print("\n=== KẾT QUẢ CẬP NHẬT CANONICAL URLS ===")
    print("-" * 100)
    print("{:<40} {:<45} {:<15}".format("FILE HTML", "CANONICAL URL", "TRẠNG THÁI"))
    print("-" * 100)
    
    updated = 0
    added = 0
    unchanged = 0
    errors = 0
    
    for file, url, status, _ in summary:
        print("{:<40} {:<45} {:<15}".format(file, url, status))
        if status == "Đã cập nhật":
            updated += 1
        elif status == "Đã thêm mới":
            added += 1
        elif status == "Không thay đổi":
            unchanged += 1
        else:
            errors += 1
    
    print("-" * 100)
    print(f"Tổng cộng: {len(summary)} trang HTML")
    print(f"  - {added} trang đã thêm canonical mới")
    print(f"  - {updated} trang đã cập nhật canonical")
    print(f"  - {unchanged} trang không thay đổi")
    print(f"  - {errors} trang lỗi")
    print(f"\nCác bản sao lưu được lưu trong thư mục: {BACKUP_FOLDER}")
    print(f"Hoàn tất lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return summary

if __name__ == "__main__":
    try:
        find_and_update_html_files()
        print("\n✅ SCRIPT ĐÃ CHẠY THÀNH CÔNG")
    except Exception as e:
        print(f"\n❌ LỖI: {str(e)}")
        print("Vui lòng kiểm tra lại cấu hình và thử lại.")