import os
import re
import glob
from pathlib import Path
import time
from bs4 import BeautifulSoup

def fix_form_labels(html_file):
    """
    Kiểm tra và sửa các thẻ input không có label liên kết 
    trong form bằng cách thêm thuộc tính id cho input và thuộc tính for cho label
    hoặc thêm label mới nếu không có.
    """
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        inputs = soup.find_all(['input', 'textarea', 'select'])
        
        modified = False
        
        for i, input_tag in enumerate(inputs):
            # Bỏ qua input hidden, submit, button và input đã có id với label tương ứng
            if input_tag.get('type') in ['hidden', 'submit', 'button', 'image']:
                continue
                
            input_id = input_tag.get('id')
            
            # Nếu input không có id, tạo id mới
            if not input_id:
                input_id = f"input_{i}_{int(time.time())}"
                input_tag['id'] = input_id
                modified = True
            
            # Kiểm tra xem có label nào liên kết với input này không
            label = soup.find('label', attrs={'for': input_id})
            
            if not label:
                # Kiểm tra xem input có nằm trong label không
                parent_label = input_tag.find_parent('label')
                if not parent_label:
                    # Không có label nào liên kết, tạo một label mới
                    if input_tag.get('placeholder'):
                        label_text = input_tag['placeholder']
                    elif input_tag.get('name'):
                        label_text = input_tag['name'].replace('_', ' ').title()
                    else:
                        label_text = f"Label for {input_id}"
                    
                    new_label = soup.new_tag('label')
                    new_label['for'] = input_id
                    new_label.string = label_text
                    
                    # Thêm label trước input
                    input_tag.insert_before(new_label)
                    modified = True
        
        if modified:
            # Tạo file backup
            backup_file = f"{html_file}.bak"
            if not os.path.exists(backup_file):
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Ghi nội dung đã sửa
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            print(f"Đã sửa form accessibility trong: {html_file}")
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
        if fix_form_labels(html_file):
            fixed_files_count += 1
    
    print(f"\nTổng kết:")
    print(f"- Đã kiểm tra: {len(html_files)} file HTML")
    print(f"- Đã sửa: {fixed_files_count} file")
    print(f"- Không cần sửa: {len(html_files) - fixed_files_count} file")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nHoàn thành trong {time.time() - start_time:.2f} giây") 