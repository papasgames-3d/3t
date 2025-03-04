import os
import re
import glob
from pathlib import Path
import time

def fix_css_import_rules(css_file):
    """
    Sửa lỗi @import trong file CSS bằng cách đảm bảo tất cả các quy tắc @import
    nằm ở đầu file CSS, trước bất kỳ khai báo style nào khác.
    """
    try:
        with open(css_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Kiểm tra xem có bất kỳ quy tắc @import nào không ở đầu file
        import_rules = re.findall(r'@import\s+[^;]+;', content)
        
        # Nếu không có quy tắc @import hoặc chúng đã ở đầu file, không cần thay đổi
        if not import_rules or all(content.find(rule) < content.find('{') for rule in import_rules):
            return False
        
        # Tạo file backup
        backup_file = f"{css_file}.bak"
        if not os.path.exists(backup_file):
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Xóa tất cả các quy tắc @import hiện có
        for rule in import_rules:
            content = content.replace(rule, '')
        
        # Thêm tất cả các quy tắc @import vào đầu file
        import_block = '\n'.join(import_rules) + '\n'
        content = import_block + content
        
        # Ghi file đã được sửa
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Đã sửa quy tắc @import trong: {css_file}")
        return True
    
    except Exception as e:
        print(f"Lỗi khi xử lý file {css_file}: {str(e)}")
        return False

def main():
    # Tìm tất cả các file CSS
    css_files = glob.glob("**/*.css", recursive=True)
    css_files += glob.glob("css/**/*.css", recursive=True)
    css_files += glob.glob("styles/**/*.css", recursive=True)
    
    # Loại bỏ các file trùng lặp
    css_files = list(set(css_files))
    
    print(f"Tìm thấy {len(css_files)} file CSS để kiểm tra")
    
    fixed_files_count = 0
    
    # Duyệt qua từng file và sửa nếu cần
    for css_file in css_files:
        if fix_css_import_rules(css_file):
            fixed_files_count += 1
    
    print(f"\nTổng kết:")
    print(f"- Đã kiểm tra: {len(css_files)} file CSS")
    print(f"- Đã sửa: {fixed_files_count} file")
    print(f"- Không cần sửa: {len(css_files) - fixed_files_count} file")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nHoàn thành trong {time.time() - start_time:.2f} giây") 