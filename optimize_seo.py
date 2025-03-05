import os
import re
import json
from datetime import datetime

# Danh sách trang cần tối ưu SEO
PAGES_TO_OPTIMIZE = [
    "shoot-the-duck.html",
    "mech-shooter.html", 
    "rome-simulator.html", 
    "kimono-fashion.html", 
    "physical-balls-2048.html", 
    "polygon-puzzle.html"
]

# Từ khóa SEO cho từng game
GAME_KEYWORDS = {
    "shoot-the-duck": "shoot the duck, duck hunting, shooting game, arcade shooter, browser game, free online game, duck hunt, shooting games",
    "mech-shooter": "mech shooter, robot shooting, action game, shooting game, mech combat, robot warfare, free online game, browser shooting game",
    "rome-simulator": "rome simulator, ancient rome, simulation game, history game, roman empire, city builder, free online game, browser simulation",
    "kimono-fashion": "kimono fashion, dress up game, fashion game, japanese kimono, traditional clothing, free online game, browser fashion game",
    "physical-balls-2048": "physical balls 2048, puzzle game, physics game, 2048 game, ball puzzle, free online game, browser puzzle, merge balls",
    "polygon-puzzle": "polygon puzzle, puzzle game, geometry puzzle, brain game, mind game, free online game, browser puzzle, polygon challenge"
}

# Mô tả SEO cho từng game
GAME_DESCRIPTIONS = {
    "shoot-the-duck": "Play Shoot the Duck, an exciting duck hunting game! Test your aiming skills in this classic arcade shooter. Free to play in your browser with no download required.",
    "mech-shooter": "Mech Shooter puts you in control of a powerful robot in an intense shooting action game. Battle enemies with advanced weapons in this thrilling browser game. Play for free!",
    "rome-simulator": "Experience ancient Rome in this detailed simulation game. Build and manage your Roman city, make strategic decisions, and enjoy a slice of history. Free to play online!",
    "kimono-fashion": "Design beautiful traditional Japanese outfits in Kimono Fashion. Express your creativity with colors, patterns and accessories in this relaxing fashion game.",
    "physical-balls-2048": "Combine identical balls in Physical Balls 2048, a fun physics-based puzzle game. Merge balls, reach 2048, and challenge your strategic thinking in this addictive browser game.",
    "polygon-puzzle": "Solve geometrical challenges in Polygon Puzzle, a mind-bending puzzle game. Arrange shapes, complete levels, and train your brain with increasingly difficult puzzles."
}

# Chi tiết nội dung bài viết cho từng game
GAME_CONTENT = {
    "shoot-the-duck": {
        "description": "Shoot the Duck is a thrilling arcade-style hunting game that brings back nostalgic memories while offering modern gameplay mechanics. Aim precisely, time your shots perfectly, and see how many ducks you can hit in this addictive browser game.",
        "how_to_play": "Simply use your mouse to aim and click to shoot. Time your shots carefully as ducks fly across the screen at different speeds and patterns. Each successful hit earns you points, while missed shots will reduce your ammunition.",
        "features": [
            "Smooth and responsive shooting mechanics",
            "Progressive difficulty levels",
            "Realistic sound effects and animations",
            "Score tracking and personal best records",
            "Multiple duck types with different behaviors",
            "Bonus rounds and special targets"
        ],
        "tips": [
            "Lead your shots - aim slightly ahead of fast-moving ducks",
            "Prioritize ducks that are about to leave the screen",
            "Save ammunition for clear shots rather than rushing",
            "Look for pattern movements to predict where ducks will fly",
            "Focus on accuracy first, then speed up as you improve"
        ]
    },
    "mech-shooter": {
        "description": "Mech Shooter puts you in command of a powerful battle robot in a futuristic combat zone. Navigate through challenging environments while defeating enemy mechs with an arsenal of high-tech weapons and upgrades.",
        "how_to_play": "Use WASD or arrow keys to move your mech, mouse to aim, and left-click to fire your primary weapon. Right-click activates your special ability, while number keys let you switch between different weapons. Destroy enemy mechs and collect scrap to upgrade your arsenal.",
        "features": [
            "Multiple customizable mech designs",
            "Arsenal of futuristic weapons and gadgets",
            "Dynamic battlefields with destructible environments",
            "Progressive upgrade system",
            "Challenging enemy AI with different combat styles",
            "Epic boss battles against giant mechs"
        ],
        "tips": [
            "Keep moving to avoid enemy fire",
            "Use cover to your advantage when reloading",
            "Prioritize upgrades for your favorite weapons",
            "Different weapons work better against specific enemy types",
            "Save your special abilities for emergencies or boss fights"
        ]
    },
    "rome-simulator": {
        "description": "Rome Simulator lets you experience the glory of ancient Rome as you build and manage your own Roman city. From humble beginnings to a sprawling metropolis, make crucial decisions that will determine the fate of your citizens and your place in history.",
        "how_to_play": "Click to place buildings, roads, and amenities. Manage resources by balancing income and expenses. Keep your citizens happy by providing food, entertainment, and security. Expand your influence through trade, diplomacy, or military conquest.",
        "features": [
            "Historically accurate buildings and city layouts",
            "Complex economy system with multiple resources",
            "Population management with different social classes",
            "Military campaigns and city defense options",
            "Natural disasters and historical events",
            "Technology tree with Roman innovations"
        ],
        "tips": [
            "Start by securing basic resources like water and food",
            "Balance residential areas with commercial and civic buildings",
            "Don't expand too quickly - quality over quantity",
            "Pay attention to citizen happiness indicators",
            "Trade with neighboring regions for resources you lack"
        ]
    },
    "kimono-fashion": {
        "description": "Kimono Fashion is a creative and culturally rich dress-up game that allows you to design beautiful traditional Japanese kimono outfits. Explore authentic patterns, accessories, and styling techniques as you create stunning ensembles for different occasions.",
        "how_to_play": "Select from a variety of kimono styles, patterns, and colors. Add layers, accessories, and hairstyles to complete the look. Save your designs to a personal collection and share them online.",
        "features": [
            "Hundreds of authentic kimono patterns and fabrics",
            "Seasonal variations (spring, summer, autumn, winter designs)",
            "Traditional accessories like obi, geta, and hair ornaments",
            "Historical information about kimono traditions",
            "Photo studio to showcase your finished designs",
            "Special event outfits for festivals and ceremonies"
        ],
        "tips": [
            "Consider the season when choosing colors and patterns",
            "Learn about color combinations that complement each other",
            "Pay attention to the formality level of different kimono styles",
            "Experiment with mixing traditional and modern elements",
            "Read the historical notes to understand the cultural significance"
        ]
    },
    "physical-balls-2048": {
        "description": "Physical Balls 2048 combines the addictive gameplay of 2048 with realistic physics mechanics. Merge identical numbered balls to create higher values, strategically dropping and bouncing them to reach the elusive 2048 ball and beyond.",
        "how_to_play": "Click or tap to drop balls from the top of the screen. When two balls with the same number touch, they merge into one ball with double the value. Continue combining balls to reach higher numbers, aiming for 2048 and beyond.",
        "features": [
            "Realistic physics engine with authentic ball movements",
            "Progressive difficulty as higher-value balls require more strategy",
            "Multiple game modes including timed challenges",
            "Special power-ups and bonus items",
            "Colorful visuals with satisfying animations",
            "Global leaderboards to compete with players worldwide"
        ],
        "tips": [
            "Build a solid foundation of lower-value balls at the bottom",
            "Look for chain reaction opportunities where multiple merges happen",
            "Use the walls to control ball direction and placement",
            "Plan ahead by watching the next ball indicator",
            "Don't rush - strategic placement is more important than speed"
        ]
    },
    "polygon-puzzle": {
        "description": "Polygon Puzzle is a brain-teasing geometric challenge that tests your spatial reasoning and problem-solving skills. Arrange various polygon shapes to fill specific outlines, rotating and flipping pieces to find the perfect fit in increasingly complex puzzles.",
        "how_to_play": "Drag polygon pieces onto the puzzle area. Use right-click or specific buttons to rotate and flip pieces. All pieces must fit within the outline with no overlaps or gaps. Complete puzzles to unlock new levels with more challenging shapes.",
        "features": [
            "Hundreds of unique puzzle configurations",
            "Progressive difficulty from beginner to expert",
            "Multiple polygon types with different properties",
            "Hint system for when you get stuck",
            "Time challenge mode for experienced players",
            "Custom puzzle creator to design your own challenges"
        ],
        "tips": [
            "Start with corner and edge pieces to establish boundaries",
            "Look for unique shapes that can only fit in certain positions",
            "Don't force pieces - if it's difficult to place, try another approach",
            "Use the hint system sparingly to maintain the challenge",
            "Practice recognizing common patterns in polygon arrangements"
        ]
    }
}

def optimize_seo_for_game_page(game_slug):
    """Tối ưu SEO cho một trang game cụ thể"""
    file_path = os.path.join("go", game_slug)
    if not os.path.exists(file_path):
        print(f"⚠️ Không tìm thấy file: {file_path}")
        return False
    
    try:
        # Đọc nội dung file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Lấy tên game từ slug
        game_name = ' '.join(word.capitalize() for word in game_slug.replace('.html', '').split('-'))
        game_slug_without_ext = game_slug.replace('.html', '')
        
        # 1. Tối ưu tiêu đề trang
        content = re.sub(
            r'<title>.*?</title>',
            f'<title>{game_name} - Play Free Online at Monkey Mart Games</title>',
            content
        )
        
        # 2. Tối ưu thẻ meta description
        description = GAME_DESCRIPTIONS.get(game_slug_without_ext, f"Play {game_name} for free online at Monkey Mart Games. Enjoy this exciting browser game with no download required.")
        
        content = re.sub(
            r'<meta content=".*?" name="description"/>',
            f'<meta content="{description}" name="description"/>',
            content
        )
        
        # 3. Tối ưu thẻ meta keywords
        keywords = GAME_KEYWORDS.get(game_slug_without_ext, f"{game_slug_without_ext}, online game, free game, browser game")
        
        content = re.sub(
            r'<meta content=".*?" name="keywords"/>',
            f'<meta content="{keywords}" name="keywords"/>',
            content
        )
        
        # 4. Cập nhật các thẻ Open Graph
        content = re.sub(
            r'<meta content=".*?" property="og:title"/>',
            f'<meta content="{game_name} - Free Online Game" property="og:title"/>',
            content
        )
        
        content = re.sub(
            r'<meta content=".*?" property="og:description"/>',
            f'<meta content="{description}" property="og:description"/>',
            content
        )
        
        # 5. Cập nhật Schema.org
        schema_pattern = r'<script type="application/ld\+json">(.*?)</script>'
        schema_match = re.search(schema_pattern, content, re.DOTALL)
        
        if schema_match:
            schema_json = schema_match.group(1).strip()
            try:
                schema_data = json.loads(schema_json)
                
                # Cập nhật thông tin Schema
                if "@graph" in schema_data:
                    for item in schema_data["@graph"]:
                        if item.get("@type") == "VideoGame":
                            item["name"] = game_name
                            item["description"] = description
                            current_date = datetime.now().strftime("%Y-%m-%d")
                            
                            # Nếu không có trường dateModified, thêm vào
                            if "dateModified" not in item:
                                item["dateModified"] = current_date
                            else:
                                item["dateModified"] = current_date
                
                # Thay thế schema cũ bằng schema mới
                new_schema_json = json.dumps(schema_data, ensure_ascii=False, indent=2)
                content = content.replace(schema_match.group(0), f'<script type="application/ld+json">{new_schema_json}</script>')
            
            except json.JSONDecodeError:
                print(f"⚠️ Lỗi khi phân tích JSON schema trong {game_slug}")
        
        # 6. Đảm bảo có thẻ H1 với tên game
        h1_pattern = r'<h1.*?>(.*?)</h1>'
        h1_match = re.search(h1_pattern, content)
        
        if h1_match:
            # Thay thế nội dung thẻ H1 hiện có
            content = re.sub(
                h1_pattern,
                f'<h1>{game_name}</h1>',
                content
            )
        else:
            # Nếu không có thẻ H1, tìm vị trí sau thẻ header hoặc main để thêm vào
            header_end = content.find('</header>')
            if header_end != -1:
                insert_pos = header_end + 9  # Độ dài của </header>
                content = content[:insert_pos] + f'\n<h1>{game_name}</h1>' + content[insert_pos:]
        
        # 7. Đảm bảo có thẻ canonical
        canonical_pattern = r'<link href=".*?" rel="canonical"/>'
        canonical_match = re.search(canonical_pattern, content)
        
        if canonical_match:
            content = re.sub(
                canonical_pattern,
                f'<link href="https://monkeymart.one/go/{game_slug}" rel="canonical"/>',
                content
            )
        else:
            # Thêm thẻ canonical vào head nếu chưa có
            head_end = content.find('</head>')
            if head_end != -1:
                insert_pos = head_end
                content = content[:insert_pos] + f'\n<link href="https://monkeymart.one/go/{game_slug}" rel="canonical"/>' + content[insert_pos:]
        
        # 8. Tối ưu nội dung bài viết
        game_content = GAME_CONTENT.get(game_slug_without_ext)
        
        if game_content:
            # Tìm vị trí để chèn nội dung bài viết
            # Thường là sau container game hoặc trước footer
            container_end = content.find('</div>', content.find('class="game-iframe-container"'))
            footer_start = content.find('<footer')
            insert_pos = container_end + 6 if container_end != -1 else (footer_start if footer_start != -1 else -1)
            
            if insert_pos != -1:
                # Chuẩn bị nội dung bài viết phong phú
                features_html = "".join(f'<li>{feature}</li>' for feature in game_content["features"])
                tips_html = "".join(f'<li>{tip}</li>' for tip in game_content["tips"])
                
                # Sử dụng .format() thay vì f-string cho nội dung HTML dài
                rich_content_template = """
<div class="game-content-container">
    <div class="game-description">
        <h2>About {game_name}</h2>
        <p>{game_description}</p>
        
        <h2>How to Play {game_name}</h2>
        <p>{how_to_play}</p>
        
        <h2>Game Features</h2>
        <ul>
            {features_html}
        </ul>
        
        <h2>Tips and Strategies</h2>
        <ul>
            {tips_html}
        </ul>
        
        <h3>Why Play {game_name} on Monkey Mart Games?</h3>
        <p>Enjoy {game_name} completely free in your browser! No downloads, no waiting - just instant fun. Our optimized gameplay ensures a smooth experience on any device. Challenge yourself or compete with friends for the highest scores!</p>
        
        <div class="game-cta">
            <p>Ready to start playing? Jump right in and enjoy {game_name} now!</p>
        </div>
    </div>
</div>

<style>
.game-content-container {{
    max-width: 800px;
    margin: 30px auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    font-family: Arial, sans-serif;
}}

.game-description h2 {{
    color: #333;
    border-bottom: 2px solid #ddd;
    padding-bottom: 8px;
    margin-top: 25px;
}}

.game-description h3 {{
    color: #555;
    margin-top: 20px;
}}

.game-description p {{
    line-height: 1.6;
    color: #444;
    margin-bottom: 16px;
}}

.game-description ul {{
    padding-left: 18px;
    margin-bottom: 20px;
}}

.game-description li {{
    margin-bottom: 8px;
    line-height: 1.4;
}}

.game-cta {{
    background-color: #f0f0f0;
    padding: 15px;
    border-radius: 5px;
    text-align: center;
    margin-top: 30px;
}}

.game-cta p {{
    font-weight: bold;
    font-size: 18px;
    color: #333;
}}

@media (max-width: 767px) {{
    .game-content-container {{
        padding: 15px;
        margin: 20px auto;
    }}
    
    .game-description h2 {{
        font-size: 20px;
    }}
    
    .game-description p, .game-description li {{
        font-size: 14px;
    }}
}}
</style>
"""
                rich_content = rich_content_template.format(
                    game_name=game_name,
                    game_description=game_content["description"],
                    how_to_play=game_content["how_to_play"],
                    features_html=features_html,
                    tips_html=tips_html
                )
                # Chèn nội dung bài viết vào trang
                content = content[:insert_pos] + rich_content + content[insert_pos:]
                
                # Thêm schema FAQ nếu chưa có
                if '"@type": "FAQPage"' not in content:
                    faq_schema = create_faq_schema(game_name, game_content["tips"])
                    script_tag_pos = content.rfind('</script>')
                    if script_tag_pos != -1:
                        content = content[:script_tag_pos+9] + faq_schema + content[script_tag_pos+9:]
            else:
                print(f"⚠️ Không tìm thấy vị trí phù hợp để chèn nội dung bài viết trong {game_slug}")
        else:
            print(f"⚠️ Không có nội dung bài viết được định nghĩa cho {game_slug}")
        
        # 9. Ghi nội dung đã cập nhật vào file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ Đã tối ưu SEO cho {game_slug}")
        return True
        
    except Exception as e:
        print(f"⚠️ Lỗi khi tối ưu SEO cho {game_slug}: {str(e)}")
        return False

def create_faq_schema(game_name, tips):
    """Tạo schema FAQPage dựa trên các tips"""
    questions = [
        f"How do I play {game_name}?",
        f"What are the best strategies for {game_name}?",
        f"Is {game_name} free to play?",
        f"Can I play {game_name} on mobile?",
        f"Why should I play {game_name} on Monkey Mart Games?"
    ]
    
    answers = [
        f"You can play {game_name} directly in your browser. Just click the game area to start and follow the on-screen instructions. No downloads required!",
        ", ".join(tips[:3]) + ".",
        f"Yes! {game_name} is completely free to play on Monkey Mart Games.",
        f"Absolutely! {game_name} is optimized for both desktop and mobile devices.",
        f"Monkey Mart Games offers {game_name} with no ads interrupting gameplay, fast loading times, and a smooth playing experience."
    ]
    
    faq_items = []
    for i in range(len(questions)):
        faq_items.append(
            {
                "@type": "Question",
                "name": questions[i],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answers[i]
                }
            }
        )
    
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_items
    }
    
    schema_json = json.dumps(faq_schema, ensure_ascii=False, indent=2)
    return f'\n<script type="application/ld+json">{schema_json}</script>\n'

def main():
    """Hàm chính để tối ưu SEO cho danh sách trang game"""
    print("\n===== CÔNG CỤ TỐI ƯU SEO CHO GAME =====")
    
    success_count = 0
    fail_count = 0
    
    for page in PAGES_TO_OPTIMIZE:
        print(f"\n[ĐANG TỐI ƯU SEO CHO: {page}]")
        if optimize_seo_for_game_page(page):
            success_count += 1
        else:
            fail_count += 1
    
    print("\n===== KẾT QUẢ TỐI ƯU SEO =====")
    print(f"✅ Đã tối ưu thành công: {success_count} trang")
    if fail_count > 0:
        print(f"⚠️ Thất bại: {fail_count} trang")
    
    print("\n===== HOÀN THÀNH =====")

if __name__ == "__main__":
    main() 