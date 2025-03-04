import os
import glob
import shutil
import time

def restore_from_backup(backup_file):
    """
    Khôi phục file gốc từ file backup (.bak)
    """
    if not backup_file.endswith('.bak'):
        print(f"Không phải file backup: {backup_file}")
        return False
    
    original_file = backup_file[:-4]  # Loại bỏ phần mở rộng '.bak'
    
    if not os.path.exists(backup_file):
        print(f"File backup không tồn tại: {backup_file}")
        return False
    
    try:
        # Sao chép nội dung từ file backup sang file gốc
        shutil.copy2(backup_file, original_file)
        print(f"Đã khôi phục: {original_file}")
        return True
    except Exception as e:
        print(f"Lỗi khi khôi phục {original_file}: {str(e)}")
        return False

def main():
    # Tìm tất cả các file backup .bak
    backup_files = glob.glob("**/*.html.bak", recursive=True)
    
    restored_count = 0
    failed_count = 0
    
    start_time = time.time()
    
    for backup_file in backup_files:
        if restore_from_backup(backup_file):
            restored_count += 1
        else:
            failed_count += 1
    
    end_time = time.time()
    
    print(f"\nTổng kết:")
    print(f"- Thời gian thực hiện: {end_time - start_time:.2f} giây")
    print(f"- Số file đã khôi phục: {restored_count}")
    print(f"- Số file không thể khôi phục: {failed_count}")

if __name__ == "__main__":
    main() 