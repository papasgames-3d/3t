import os
import re
import glob
from bs4 import BeautifulSoup

def check_and_fix_noindex(file_path):
    """Kiểm tra và xóa thẻ noindex nếu có"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Kiểm tra bằng regex trước
        noindex_pattern = re.compile(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\'].*?noindex.*?["\']', re.IGNORECASE)
        match = noindex_pattern.search(content)
        
        if match:
            print(f"✅ Tìm thấy thẻ noindex trong {file_path} bằng regex")
            # Xóa thẻ noindex bằng regex
            content = noindex_pattern.sub('', content)
            print(f"  ↳ Đã xóa thẻ noindex")
            
            # Ghi lại nội dung đã sửa
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        else:
            # Kiểm tra kỹ hơn bằng BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            meta_robots = soup.find('meta', attrs={'name': 'robots'})
            
            if meta_robots and 'noindex' in meta_robots.get('content', '').lower():
                print(f"✅ Tìm thấy thẻ noindex trong {file_path} bằng BeautifulSoup")
                meta_robots.extract()  # Xóa thẻ
                
                # Ghi lại nội dung đã sửa
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
                print(f"  ↳ Đã xóa thẻ noindex")
                return True
            
            # Kiểm tra HTTP-EQUIV
            meta_equiv = soup.find('meta', attrs={'http-equiv': 'robots'})
            if meta_equiv and 'noindex' in meta_equiv.get('content', '').lower():
                print(f"✅ Tìm thấy thẻ http-equiv robots noindex trong {file_path}")
                meta_equiv.extract()  # Xóa thẻ
                
                # Ghi lại nội dung đã sửa
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
                print(f"  ↳ Đã xóa thẻ http-equiv robots")
                return True
                
            # Kiểm tra X-Robots-Tag trong header hoặc meta http-equiv
            header_tag = soup.find('meta', attrs={'http-equiv': 'X-Robots-Tag'})
            if header_tag and 'noindex' in header_tag.get('content', '').lower():
                print(f"✅ Tìm thấy thẻ X-Robots-Tag noindex trong {file_path}")
                header_tag.extract()  # Xóa thẻ
                
                # Ghi lại nội dung đã sửa
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
                print(f"  ↳ Đã xóa thẻ X-Robots-Tag")
                return True
            
            # Kiểm tra canonical URL
            canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
            if canonical_tag:
                canonical_url = canonical_tag.get('href', '')
                if not canonical_url.startswith(('https://monkeymart.one', 'http://monkeymart.one', '/')):
                    print(f"⚠️ Canonical URL không chính xác: {canonical_url} trong {file_path}")
                    # Cập nhật canonical URL
                    game_path = os.path.basename(file_path)
                    correct_url = f"https://monkeymart.one/go/{game_path}"
                    canonical_tag['href'] = correct_url
                    
                    # Ghi lại nội dung đã sửa
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(str(soup))
                    print(f"  ↳ Đã sửa canonical URL thành: {correct_url}")
                    return True
            else:
                print(f"⚠️ Không tìm thấy thẻ canonical trong {file_path}")
                # Thêm thẻ canonical
                head_tag = soup.find('head')
                if head_tag:
                    game_path = os.path.basename(file_path)
                    new_canonical = soup.new_tag('link', rel='canonical', href=f"https://monkeymart.one/go/{game_path}")
                    head_tag.append(new_canonical)
                    
                    # Ghi lại nội dung đã sửa
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(str(soup))
                    print(f"  ↳ Đã thêm thẻ canonical: https://monkeymart.one/go/{game_path}")
                    return True
            
            # Kiểm tra và thêm thẻ index rõ ràng nếu chưa có
            if not meta_robots:
                head_tag = soup.find('head')
                if head_tag:
                    new_robots = soup.new_tag('meta', attrs={'name': 'robots', 'content': 'index, follow'})
                    head_tag.append(new_robots)
                    
                    # Ghi lại nội dung đã sửa
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(str(soup))
                    print(f"✅ Đã thêm thẻ meta robots rõ ràng trong {file_path}")
                    return True
            
            print(f"ℹ️ Không tìm thấy vấn đề noindex trong {file_path}")
            return False
    
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra {file_path}: {str(e)}")
        return False

def main():
    """Hàm chính để kiểm tra và xóa thẻ noindex trong các trang game"""
    print("\n===== CÔNG CỤ KIỂM TRA VÀ XÓA THẺ NOINDEX =====")
    
    # Danh sách các trang cần kiểm tra
    target_files = [
        "go/shoot-the-duck.html",
        "go/mech-shooter.html",
        "go/rome-simulator.html",
        "go/kimono-fashion.html",
        "go/physical-balls-2048.html",
        "go/polygon-puzzle.html"
    ]
    
    # Kiểm tra tất cả các trang trong thư mục go/
    all_game_files = glob.glob('go/*.html')
    
    print(f"Tìm thấy {len(all_game_files)} trang game tổng cộng.")
    print(f"Đang kiểm tra chi tiết {len(target_files)} trang được chỉ định...")
    
    fixed_count = 0
    
    # Kiểm tra các trang cụ thể trước
    for file_path in target_files:
        if os.path.exists(file_path):
            print(f"\n[ĐANG KIỂM TRA: {file_path}]")
            if check_and_fix_noindex(file_path):
                fixed_count += 1
        else:
            print(f"❌ Không tìm thấy file: {file_path}")
    
    # Kiểm tra thêm các trang khác
    print("\nĐang kiểm tra thêm các trang game khác...")
    for file_path in all_game_files:
        if file_path not in target_files:
            if check_and_fix_noindex(file_path):
                fixed_count += 1
    
    # Kiểm tra trang chủ
    print("\n[ĐANG KIỂM TRA: index.html]")
    if check_and_fix_noindex('index.html'):
        fixed_count += 1
    
    print("\n===== KẾT QUẢ KIỂM TRA =====")
    print(f"✅ Đã sửa: {fixed_count} trang")
    print(f"ℹ️ Tổng số trang đã kiểm tra: {len(target_files) + len(all_game_files) - len(set(target_files).intersection(all_game_files)) + 1}")
    
    print("\n===== HOÀN THÀNH =====")
    print("Lưu ý: Sau khi sửa các trang, hãy gửi lại sitemap cho Google và sử dụng Google Search Console để yêu cầu Google lập chỉ mục lại các trang.")

if __name__ == "__main__":
    main() 