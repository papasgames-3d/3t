import os
import re

def fix_image_paths(directory='./category'):
    """Sửa đường dẫn ảnh trong các trang category"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. Thay thế hoặc loại bỏ thẻ base href
                base_pattern = r'<base\s+href="https://monkeymart.one">'
                content = re.sub(base_pattern, '<base href="/">', content)
                
                # 2. Sửa đường dẫn ảnh tương đối
                img_pattern = r'data-src="([^/].*?img/.*?)"'
                content = re.sub(img_pattern, r'data-src="/\1"', content)
                
                # 3. Thêm script lazyload nếu chưa có
                if '</body>' in content and 'lazysizes.min.js' not in content:
                    lazyload_script = '''
<script>
document.addEventListener("DOMContentLoaded", function() {
    // Kiểm tra xem lazysizes đã được tải chưa
    if (typeof lazySizes === 'undefined') {
        // Nếu chưa, tạo và tải script
        var lazyScript = document.createElement('script');
        lazyScript.src = 'https://cdn.jsdelivr.net/npm/lazysizes@5.3/lazysizes.min.js';
        lazyScript.integrity = 'sha256-PZEg+mIdptYTwWmLcBTsa99GIDZujyt7VHBZ9Lb2Jys=';
        lazyScript.crossOrigin = 'anonymous';
        document.body.appendChild(lazyScript);
    }
    
    // Fallback cho ảnh nếu lazy loading không hoạt động
    setTimeout(function() {
        document.querySelectorAll('img.lazyload').forEach(function(img) {
            if (img.src.includes('data:image/gif') && img.dataset.src) {
                img.src = img.dataset.src;
            }
        });
    }, 3000);
});
</script>
'''
                    content = content.replace('</body>', lazyload_script + '\n</body>')
                
                # Lưu lại file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Đã sửa file: {file_path}")

if __name__ == "__main__":
    fix_image_paths()
    print("Hoàn tất! Đã sửa đường dẫn ảnh cho các trang category.")