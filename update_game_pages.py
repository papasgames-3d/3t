import os
from bs4 import BeautifulSoup
import re

def get_game_frame_template(game_name, game_path, image_name):
    return f'''<!-- Game Frame Container -->
<div class="game-frame-container">
    <div class="game-thumbnail">
        <img src="../assets/img/img-up/{image_name}.png" alt="{game_name}" />
        <button class="play-frame-button" id="playGameButton">
            <i class="fas fa-play"></i>
            Play Game
        </button>
    </div>
    <iframe src="{game_path}" allowfullscreen id="game-frame" style="display: none;"></iframe>
    <div class="game-controls">
        <button class="control-btn" id="share-btn" title="Share">
            <i class="fas fa-share-alt"></i>
        </button>
        <button class="control-btn" id="fullscreen-btn" title="Fullscreen">
            <i class="fas fa-expand"></i>
        </button>
    </div>
    <div class="share-menu" id="share-menu">
        <button class="control-btn" id="copy-link-btn" title="Copy Link">
            <i class="fas fa-link"></i>
        </button>
        <button class="control-btn" id="facebook-btn" title="Share on Facebook">
            <i class="fab fa-facebook-f"></i>
        </button>
        <button class="control-btn" id="twitter-btn" title="Share on Twitter">
            <i class="fab fa-twitter"></i>
        </button>
        <button class="control-btn" id="pinterest-btn" title="Share on Pinterest">
            <i class="fab fa-pinterest-p"></i>
        </button>
    </div>
    <div class="game-frame-title">{game_name}</div>
</div>'''

def update_game_page(file_path):
    print(f"Updating {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Get game name from title
    title_tag = soup.find('title')
    game_name = title_tag.text.split('-')[0].strip() if title_tag else os.path.splitext(os.path.basename(file_path))[0].replace('-', ' ').title()
    
    # Get image name from file name
    image_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Find game path from existing iframe or construct it
    iframe = soup.find('iframe')
    game_path = iframe.get('src', '') if iframe else f"./game/{image_name}/index.html"
    
    # Create new game frame HTML
    new_frame_html = get_game_frame_template(game_name, game_path, image_name)
    
    # Find the main content section
    main_content = soup.find('section', class_='games-grid')
    if not main_content:
        main_content = soup.find('main', class_='main-content')
    
    if main_content:
        # Remove existing game frame if any
        old_frame = main_content.find('div', class_='game-frame-container')
        if old_frame:
            old_frame.decompose()
        
        # Remove old title if any
        old_title = main_content.find('div', class_='game-frame-title')
        if old_title:
            old_title.decompose()
        
        # Insert new frame at the beginning of main content
        new_frame_soup = BeautifulSoup(new_frame_html, 'html.parser')
        if main_content.contents:
            main_content.contents[0].insert_before(new_frame_soup)
        else:
            main_content.append(new_frame_soup)
    
    # Update script tags
    head_tag = soup.find('head')
    if head_tag:
        # Remove existing game-controls.js if present
        for script in soup.find_all('script', src=re.compile(r'game-controls\.js$')):
            script.decompose()
        
        # Add game-controls.js before closing head tag
        new_script = soup.new_tag('script', src='../assets/js/game-controls.js')
        head_tag.append(new_script)
    
    # Save the updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Updated {file_path}")

def main():
    game_dir = 'game'
    if not os.path.exists(game_dir):
        print(f"Directory {game_dir} not found!")
        return
    
    # Process all HTML files in the game directory
    for filename in os.listdir(game_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(game_dir, filename)
            update_game_page(file_path)

if __name__ == '__main__':
    main() 