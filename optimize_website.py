#!/usr/bin/env python3
# optimize_website.py
import os
import re
import subprocess
import time
from PIL import Image
import shutil
import json

def optimize_images(directory='.', quality=80):
    """Tối ưu hóa tất cả hình ảnh trong thư mục"""
    print("\n=== ĐANG TỐI ƯU HÌNH ẢNH ===")
    total_saved = 0
    count = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and '/img/' in root.replace('\\', '/'):
                file_path = os.path.join(root, file)
                
                # Lấy kích thước ban đầu
                original_size = os.path.getsize(file_path)
                
                try:
                    # Tối ưu hóa hình ảnh với Pillow
                    img = Image.open(file_path)
                    
                    # Nén theo loại file
                    if file.lower().endswith('.png'):
                        webp_path = os.path.splitext(file_path)[0] + '.webp'
                        img.save(webp_path, 'WEBP', quality=quality)
                        # Nếu WebP nhẹ hơn, dùng file đó thay thế trong HTML
                        if os.path.exists(webp_path):
                            if os.path.getsize(webp_path) < original_size:
                                print(f"Đã tạo WebP nhẹ hơn: {webp_path}")
                                new_size = os.path.getsize(webp_path)
                                saved = original_size - new_size
                                total_saved += saved
                                count += 1
                    elif file.lower().endswith(('.jpg', '.jpeg')):
                        img.save(file_path, quality=quality, optimize=True)
                        new_size = os.path.getsize(file_path)
                        saved = original_size - new_size
                        total_saved += saved
                        count += 1
                        print(f"Tối ưu: {file_path} - Tiết kiệm {saved/1024:.2f}KB")
                    elif file.lower().endswith('.webp'):
                        img.save(file_path, 'WEBP', quality=quality)
                        new_size = os.path.getsize(file_path)
                        saved = original_size - new_size
                        total_saved += saved
                        count += 1
                        print(f"Tối ưu: {file_path} - Tiết kiệm {saved/1024:.2f}KB")
                except Exception as e:
                    print(f"Lỗi xử lý {file_path}: {str(e)}")
    
    print(f"\nĐã tối ưu {count} hình ảnh, tiết kiệm tổng cộng {total_saved/1024/1024:.2f}MB")

def update_image_tags(directory='.'):
    """Cập nhật thẻ img để sử dụng WebP và lazy loading"""
    print("\n=== ĐANG CẬP NHẬT THẺ HÌNH ẢNH ===")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Đảm bảo tất cả thẻ img đều có thuộc tính loading=lazy và class=lazyload
                img_pattern = r'<img\s+([^>]*)\s*/?>'
                updated_content = content
                
                for match in re.finditer(img_pattern, content):
                    img_tag = match.group(0)
                    img_attrs = match.group(1)
                    
                    # Kiểm tra xem đã có loading=lazy chưa
                    if 'loading=' not in img_attrs:
                        img_tag_new = img_tag.replace('<img ', '<img loading="lazy" ')
                    else:
                        img_tag_new = img_tag
                    
                    # Kiểm tra xem đã có class=lazyload chưa
                    if 'class=' in img_attrs:
                        if 'lazyload' not in img_attrs:
                            img_tag_new = re.sub(r'class="([^"]*)"', r'class="\1 lazyload"', img_tag_new)
                    else:
                        img_tag_new = img_tag_new.replace('<img ', '<img class="lazyload" ')
                    
                    # Thêm decoding="async" nếu chưa có
                    if 'decoding=' not in img_tag_new:
                        img_tag_new = img_tag_new.replace('<img ', '<img decoding="async" ')
                    
                    # Cập nhật src thành data-src nếu chưa có
                    if 'data-src=' not in img_tag_new and 'src=' in img_tag_new:
                        img_tag_new = re.sub(r'src="([^"]*)"', r'src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="\1"', img_tag_new)
                    
                    # Cập nhật nội dung
                    if img_tag_new != img_tag:
                        updated_content = updated_content.replace(img_tag, img_tag_new)
                
                # Lưu lại nếu có thay đổi
                if updated_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"Đã cập nhật thẻ img trong {file_path}")

def add_resource_hints(file_path):
    """Thêm resource hints vào trang"""
    print(f"\n=== ĐANG THÊM RESOURCE HINTS VÀO {file_path} ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Danh sách domain cần preconnect
    preconnect_domains = [
        "https://www.googletagmanager.com", 
        "https://fonts.googleapis.com", 
        "https://fonts.gstatic.com",
        "https://cdn.jsdelivr.net"
    ]
    
    # Tạo các thẻ preconnect
    preconnect_tags = ""
    for domain in preconnect_domains:
        preconnect_tags += f'    <link rel="preconnect" href="{domain}" crossorigin>\n'
    
    # Thêm preload cho CSS và JS quan trọng
    preload_tags = """
    <link rel="preload" href="/css/style.css" as="style">
    <link rel="preload" href="/js/main.js" as="script">
    <link rel="preload" href="/img/logo.png" as="image">
"""
    
    # Thêm vào sau thẻ <head>
    if '<head>' in content:
        new_content = content.replace('<head>', '<head>\n' + preconnect_tags + preload_tags)
        
        # Lưu lại nếu có thay đổi
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Đã thêm resource hints vào {file_path}")
    else:
        print(f"Không tìm thấy thẻ <head> trong {file_path}")

def optimize_javascript(directory='.'):
    """Tối ưu JavaScript bằng cách thêm 'defer' và 'async'"""
    print("\n=== ĐANG TỐI ƯU JAVASCRIPT ===")
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Thêm defer cho script không phải analytics hoặc critical
                script_pattern = r'<script\s+([^>]*)src="([^"]*)"([^>]*)></script>'
                updated_content = content
                
                for match in re.finditer(script_pattern, content):
                    script_tag = match.group(0)
                    attrs_before = match.group(1)
                    src = match.group(2)
                    attrs_after = match.group(3)
                    
                    # Bỏ qua script đã có async hoặc defer, hoặc là analytics
                    if 'async' in script_tag or 'defer' in script_tag:
                        continue
                    if 'googletagmanager' in src or 'analytics' in src:
                        continue
                    
                    # Thêm defer cho script khác
                    script_new = script_tag.replace('></script>', ' defer></script>')
                    updated_content = updated_content.replace(script_tag, script_new)
                
                # Lưu lại nếu có thay đổi
                if updated_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"Đã tối ưu script trong {file_path}")

def create_htaccess(directory='.'):
    """Tạo file .htaccess để tối ưu server performance"""
    htaccess_path = os.path.join(directory, '.htaccess')
    
    htaccess_content = """# Tối ưu performance
# Enable Gzip compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/x-javascript application/json application/xml
</IfModule>

# Browser caching
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpg "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/gif "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType image/x-icon "access plus 1 year"
  ExpiresByType image/ico "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/pdf "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType text/javascript "access plus 1 month"
  ExpiresByType text/x-javascript "access plus 1 month"
  ExpiresByType text/html "access plus 1 week"
  ExpiresByType application/xhtml+xml "access plus 1 week"
</IfModule>

# Keep-alive connections
<IfModule mod_headers.c>
  Header set Connection keep-alive
  
  # CORS headers
  <FilesMatch "\.(ttf|ttc|otf|eot|woff|woff2|font.css|css|js)$">
    Header set Access-Control-Allow-Origin "*"
  </FilesMatch>
</IfModule>

# Security headers
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set X-XSS-Protection "1; mode=block"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

# Redirect from www to non-www
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\.(.*)$ [NC]
RewriteRule ^(.*)$ https://%1/$1 [R=301,L]

# Redirect HTTP to HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
"""
    
    with open(htaccess_path, 'w', encoding='utf-8') as f:
        f.write(htaccess_content)
    
    print(f"\n=== ĐÃ TẠO FILE .HTACCESS ===")
    print(f"File .htaccess đã được tạo tại: {htaccess_path}")

def run_full_optimization():
    """Chạy tất cả các bước tối ưu"""
    start_time = time.time()
    
    print("=== BẮT ĐẦU QUÁ TRÌNH TỐI ƯU WEBSITE ===")
    
    # 1. Tối ưu hình ảnh
    optimize_images()
    
    # 2. Cập nhật thẻ img
    update_image_tags()
    
    # 3. Thêm resource hints
    if os.path.exists('index.html'):
        add_resource_hints('index.html')
    
    # 4. Tối ưu JavaScript
    optimize_javascript()
    
    # 5. Tạo file .htaccess
    create_htaccess()
    
    # 6. Tạo báo cáo
    print("\n=== BÁO CÁO TỐI ƯU ===")
    print(f"Thời gian thực hiện: {(time.time() - start_time):.2f} giây")
    print("Các biện pháp đã thực hiện:")
    print("1. Tối ưu hình ảnh và tạo WebP")
    print("2. Cập nhật thẻ img với lazy loading")
    print("3. Thêm resource hints vào trang chủ")
    print("4. Tối ưu JavaScript với defer")
    print("5. Tạo file .htaccess tối ưu")
    
    print("\n=== HOÀN THÀNH ===")
    print("""
    Các bước tiếp theo:
    1. Kiểm tra website với Google PageSpeed Insights: https://pagespeed.web.dev/
    2. Tải website lên server và kiểm tra hiệu suất thực tế
    3. Xem xét sử dụng CDN cho tài nguyên tĩnh
    """)

if __name__ == "__main__":
    run_full_optimization()