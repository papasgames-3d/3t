import os
import re

def update_menu(content):
    # Tìm vị trí menu cần thay thế
    menu_pattern = r'<ul>\s*?<li><a title="new" href="/category/new.html">NEW</a></li>.*?</ul>'
    
    # Menu mới
    new_menu = '''<ul>
                                    <li><a title="new" href="/category/new.html">NEW</a></li>
                                    <li><a title="hot games" href="/category/hot-game.html">Hot Games</a></li>
                                    <li><a title="papa games" href="/category/papa-game.html">Papa Games</a></li>
                                    <li><a title="racing" href="/category/racing.html">Racing</a></li>
                                    <li><a title="car" href="/category/car.html">Car</a></li>
                                    <li><a title="puzzle" href="/category/puzzle.html">Puzzle</a></li>
                                    <li><a href="#">More</a>
                                        <ul class="sub-menu">
                                            <li><a href="/category/sports.html">Sports</a></li>
                                            <li><a href="/category/running.html">Running</a></li>
                                            <li><a href="/category/skill.html">Skill</a></li>
                                            <li><a href="/category/stickman.html">Stickman</a></li>
                                            <li><a href="/category/adventure.html">Adventure</a></li>
                                            <li><a href="/category/shooting.html">Shooting</a></li>
                                            <li><a href="/category/fighting.html">Fighting</a></li>
                                            <li><a href="/category/2-player.html">2 Player</a></li>
                                            <li><a href="/category/multiplayer.html">Multiplayer</a></li>
                                            <li><a href="/category/action.html">Action</a></li>
                                            <li><a href="/category/3d.html">3D</a></li>
                                            <li><a href="/category/car.html">Car</a></li>
                                            <li><a href="/category/moto.html">Moto</a></li>
                                            <li><a href="/category/idle.html">Idle</a></li>
                                            <li><a href="/category/fnf.html">FNF</a></li>
                                        </ul>
                                    </li>
                                </ul>'''
    
    # Thay thế menu cũ bằng menu mới
    updated_content = re.sub(menu_pattern, new_menu, content, flags=re.DOTALL)
    return updated_content

def process_files():
    # Danh sách các thư mục cần quét
    directories = ['category', 'go']
    
    # Thêm file index.html ở thư mục gốc
    files_to_update = ['index.html']
    
    # Thêm các file từ thư mục category và go
    for directory in directories:
        for file in os.listdir(directory):
            if file.endswith('.html'):
                files_to_update.append(os.path.join(directory, file))
    
    # Xử lý từng file
    for file_path in files_to_update:
        try:
            print(f"Đang xử lý file: {file_path}")
            
            # Đọc nội dung file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Cập nhật menu
            updated_content = update_menu(content)
            
            # Ghi nội dung đã cập nhật vào file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
                
            print(f"Đã cập nhật thành công: {file_path}")
            
        except Exception as e:
            print(f"Lỗi khi xử lý file {file_path}: {str(e)}")

if __name__ == "__main__":
    process_files()