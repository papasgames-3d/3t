import os
import re
import glob
from pathlib import Path
import time

def fix_wgplayer_clonenode_issue(html_file):
    """
    Sửa vấn đề với script WGPlayer gây ra lỗi 'Cannot read properties of null (reading 'cloneNode')'
    Trả về True nếu file đã được sửa, False nếu không cần sửa.
    """
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Kiểm tra xem file có script WGPlayer không
    wgplayer_pattern = r'<script type="text/javascript" async>!function\(e,t\)\{a=e\.createElement\("script"\),m=e\.getElementsByTagName\("script"\)\[0\],a\.async=1,a\.src=t,a\.fetchPriority=\'high\',m\.parentNode\.insertBefore\(a,m\)\}\(document,"https://universal\.wgplayer\.com/tag/\?lh="\+window\.location\.hostname\+"&wp="\+window\.location\.pathname\+"&ws="\+window\.location\.search\);</script>'
    
    if not re.search(wgplayer_pattern, content):
        return False  # Không có script WGPlayer
    
    # Tạo bản sao lưu trước khi sửa
    backup_path = f"{html_file}.bak-adfix-{int(time.time())}"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Sửa định dạng script WGPlayer để tránh lỗi cloneNode
    improved_wgplayer = '<script type="text/javascript">\n(function(d, u) {\n  var s = d.createElement("script");\n  s.async = true;\n  s.src = u + "?lh=" + window.location.hostname + "&wp=" + window.location.pathname + "&ws=" + window.location.search;\n  s.fetchPriority = "high";\n  var m = d.getElementsByTagName("script")[0];\n  m.parentNode.insertBefore(s, m);\n})(document, "https://universal.wgplayer.com/tag/");\n</script>'
    
    # Thay thế script WGPlayer bằng phiên bản cải tiến
    fixed_content = re.sub(wgplayer_pattern, improved_wgplayer, content, count=1)
    
    # Loại bỏ bất kỳ script WGPlayer trùng lặp nào
    fixed_content = re.sub(wgplayer_pattern, '', fixed_content)
    
    # Kiểm tra xem nội dung đã thay đổi hay chưa
    if fixed_content == content:
        return False
    
    # Ghi nội dung đã sửa vào file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    return True

def fix_double_gpt_loading(html_file):
    """
    Sửa vấn đề khi Google Publisher Tags (GPT) được tải nhiều lần
    Trả về True nếu file đã được sửa, False nếu không cần sửa.
    """
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Kiểm tra các đoạn mã liên quan đến GPT
    gpt_script_count = len(re.findall(r'googletag\.cmd\.push', content))
    
    if gpt_script_count <= 1:
        return False  # Không có vấn đề GPT trùng lặp
    
    # Kiểm tra nếu đã có bản sao lưu, nếu không thì tạo mới
    backup_path = f"{html_file}.bak-adfix-{int(time.time())}"
    if not os.path.exists(backup_path):
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Tìm và giữ lại chỉ một đoạn mã GPT
    gpt_define_pattern = r'(var\s+googletag\s*=\s*googletag\s*\|\|\s*\{\s*\};\s*googletag\.cmd\s*=\s*googletag\.cmd\s*\|\|\s*\[\s*\];.*?)(?=var\s+googletag\s*=\s*googletag|<\/script>)'
    gpt_matches = re.findall(gpt_define_pattern, content, re.DOTALL)
    
    if len(gpt_matches) > 1:
        # Giữ lại đoạn mã GPT đầu tiên và loại bỏ các đoạn khác
        fixed_content = re.sub(gpt_define_pattern, lambda m, idx=[0]: m.group() if idx[0] == 0 and not idx.__setitem__(0, 1) else '', content, flags=re.DOTALL)
        
        # Ghi nội dung đã sửa vào file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        return True
    
    return False

def main():
    # Tìm tất cả các file HTML
    html_files = glob.glob('**/*.html', recursive=True)
    
    wgplayer_fixed_count = 0
    gpt_fixed_count = 0
    skipped_count = 0
    
    for html_file in html_files:
        print(f'Đang kiểm tra: {html_file}')
        
        # Sửa vấn đề WGPlayer cloneNode
        if fix_wgplayer_clonenode_issue(html_file):
            print(f'Đã sửa WGPlayer script trong: {html_file}')
            wgplayer_fixed_count += 1
        
        # Sửa vấn đề GPT tải nhiều lần
        if fix_double_gpt_loading(html_file):
            print(f'Đã sửa GPT script trong: {html_file}')
            gpt_fixed_count += 1
        
        if not (fix_wgplayer_clonenode_issue(html_file) or fix_double_gpt_loading(html_file)):
            print(f'Không cần sửa: {html_file}')
            skipped_count += 1
    
    print(f'\nTổng kết:')
    print(f'- Đã sửa WGPlayer script: {wgplayer_fixed_count} file')
    print(f'- Đã sửa GPT script: {gpt_fixed_count} file')
    print(f'- Không cần sửa: {skipped_count} file')

if __name__ == "__main__":
    main() 