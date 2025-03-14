import os  
import shutil  
from bs4 import BeautifulSoup  
import logging  
from datetime import datetime  
import time  
from tqdm import tqdm  
import sys  

class GameFileProcessor:  
    def __init__(self, root_directory):  
        self.root_directory = root_directory  
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  
        self.backup_dir = f'backup_{self.timestamp}'  
        self.log_file = f'modification_log_{self.timestamp}.txt'  
        self.processed_files = 0  
        self.failed_files = 0  
        self.setup_logging()  

    def setup_logging(self):  
        logging.basicConfig(  
            filename=self.log_file,  
            level=logging.INFO,  
            format='%(asctime)s - %(levelname)s - %(message)s'  
        )  

    def create_backup(self, file_path):  
        relative_path = os.path.relpath(file_path, self.root_directory)  
        backup_path = os.path.join(self.backup_dir, relative_path)  
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)  
        shutil.copy2(file_path, backup_path)  

    def modify_html_file(self, file_path):  
        try:  
            # Đọc file HTML  
            with open(file_path, 'r', encoding='utf-8') as file:  
                content = file.read()  
                soup = BeautifulSoup(content, 'html.parser')  

            # Tìm game arena  
            game_arena = soup.find('div', id='game-arena')  
            if not game_arena:  
                logging.warning(f"No game arena found in {file_path}")  
                return False  

            # Lấy game URL  
            game_url = game_arena.get('data-url')  
            if not game_url:  
                logging.warning(f"No game URL found in {file_path}")  
                return False  

            # Tạo backup trước khi modify  
            self.create_backup(file_path)  

            # Xóa splash container  
            splash_container = game_arena.find('div', class_='talpa-splash-container')  
            if splash_container:  
                splash_container.decompose()  

            # Tạo iframe mới  
            iframe = soup.new_tag('iframe')  
            iframe['src'] = game_url  
            iframe['allowfullscreen'] = ''  
            iframe['frameborder'] = '0'  
            iframe['width'] = '100%'  
            iframe['height'] = '100%'  
            iframe['scrolling'] = 'none'  

            # Cập nhật game arena  
            game_arena.clear()  
            game_arena.append(iframe)  

            # Xóa hàm playGame  
            for script in soup.find_all('script'):  
                if script.string and 'playGame' in script.string:  
                    new_script = '\n'.join([  
                        line for line in script.string.split('\n')  
                        if 'function playGame' not in line and 'playGame()' not in line  
                    ])  
                    script.string = new_script  

            # Lưu file  
            with open(file_path, 'w', encoding='utf-8') as file:  
                file.write(str(soup))  

            return True  

        except Exception as e:  
            logging.error(f"Error processing {file_path}: {str(e)}")  
            return False  

    def process_directory(self):  
        # Tìm tất cả file HTML  
        html_files = []  
        for root, _, files in os.walk(self.root_directory):  
            for file in files:  
                if file.endswith('.html'):  
                    html_files.append(os.path.join(root, file))  

        if not html_files:  
            print("Không tìm thấy file HTML nào!")  
            return  

        # Xác nhận từ người dùng  
        print(f"\nTìm thấy {len(html_files)} file HTML.")  
        print(f"Backup sẽ được lưu trong thư mục: {self.backup_dir}")  
        confirm = input("\nBạn có muốn tiếp tục không? (y/n): ")  
        if confirm.lower() != 'y':  
            print("Hủy thao tác.")  
            return  

        # Tạo thư mục backup  
        os.makedirs(self.backup_dir, exist_ok=True)  

        # Xử lý các file với progress bar  
        start_time = time.time()  
        print("\nĐang xử lý files...")  
        
        for file_path in tqdm(html_files):  
            if self.modify_html_file(file_path):  
                self.processed_files += 1  
            else:  
                self.failed_files += 1  

        # Báo cáo kết quả  
        duration = time.time() - start_time  
        self.print_report(duration)  

    def print_report(self, duration):  
        print("\n=== BÁO CÁO KẾT QUẢ ===")  
        print(f"Thời gian xử lý: {duration:.2f} giây")  
        print(f"Tổng số file đã xử lý: {self.processed_files}")  
        print(f"Số file thất bại: {self.failed_files}")  
        print(f"Backup được lưu tại: {self.backup_dir}")  
        print(f"Log file: {self.log_file}")  

def main():  
    if len(sys.argv) != 2:  
        print("Sử dụng: python script.py <đường_dẫn_thư_mục>")  
        sys.exit(1)  

    directory = sys.argv[1]  
    if not os.path.isdir(directory):  
        print("Thư mục không tồn tại!")  
        sys.exit(1)  

    processor = GameFileProcessor(directory)  
    processor.process_directory()  

if __name__ == "__main__":  
    main()  