#!/usr/bin/env python3
# image_optimizer.py
import os
import subprocess
from PIL import Image

def optimize_images(directory='.', quality=80):
    """Tối ưu hóa tất cả hình ảnh trong thư mục"""
    total_saved = 0
    count = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                file_path = os.path.join(root, file)
                
                # Lấy kích thước ban đầu
                original_size = os.path.getsize(file_path)
                
                try:
                    # Tối ưu hóa hình ảnh với Pillow
                    img = Image.open(file_path)
                    
                    # Chuyển PNG sang WebP (tiết kiệm dung lượng)
                    if file.lower().endswith('.png'):
                        webp_path = os.path.splitext(file_path)[0] + '.webp'
                        img.save(webp_path, 'WEBP', quality=quality)
                        if os.path.exists(webp_path) and os.path.getsize(webp_path) < original_size:
                            print(f"Chuyển đổi: {file_path} -> {webp_path}")
                            # Giữ lại bản gốc cho trường hợp tương thích
                    
                    # Nén JPG/JPEG
                    elif file.lower().endswith(('.jpg', '.jpeg')):
                        img.save(file_path, quality=quality, optimize=True)
                    
                    # Nén WebP hiện có
                    elif file.lower().endswith('.webp'):
                        img.save(file_path, 'WEBP', quality=quality)
                    
                    # Tính toán dung lượng đã tiết kiệm
                    new_size = os.path.getsize(file_path)
                    saved = original_size - new_size
                    total_saved += saved
                    count += 1
                    
                    print(f"Tối ưu: {file_path} - Tiết kiệm {saved/1024:.2f}KB ({saved/original_size*100:.1f}%)")
                    
                except Exception as e:
                    print(f"Lỗi xử lý {file_path}: {str(e)}")
    
    print(f"\nĐã tối ưu {count} hình ảnh, tiết kiệm tổng cộng {total_saved/1024/1024:.2f}MB")

if __name__ == "__main__":
    optimize_images()