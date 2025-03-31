import os
import re
import shutil
from pathlib import Path
import urllib.request
import urllib.error

def create_slug(game_name):
    """Convert game name to a URL-friendly slug."""
    # Convert to lowercase
    slug = game_name.lower()
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove special characters
    slug = re.sub(r'[^\w\-]', '', slug)
    return slug

def get_available_images():
    """Get a list of available game images in the img/games directory."""
    images_dir = os.path.join("img", "games")
    if not os.path.exists(images_dir):
        print(f"Warning: Directory {images_dir} does not exist.")
        return []
    
    return [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f)) and 
            f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

def download_image(image_url, slug):
    """Download image from URL and save with slug name, adding numbers if file exists."""
    # Extract file extension from URL
    image_ext = os.path.splitext(image_url)[1].lower()
    if not image_ext or image_ext not in ['.png', '.jpg', '.jpeg', '.gif']:
        image_ext = '.png'  # Default to PNG if no valid extension
    
    # Create images directory if it doesn't exist
    images_dir = os.path.join("img", "games")
    os.makedirs(images_dir, exist_ok=True)
    
    # Create base filename from slug
    base_filename = slug + image_ext
    image_path = os.path.join(images_dir, base_filename)
    
    # Check if file exists and increment number if needed
    counter = 1
    while os.path.exists(image_path):
        base_filename = f"{slug}-{counter}{image_ext}"
        image_path = os.path.join(images_dir, base_filename)
        counter += 1
    
    try:
        # Download the image
        print(f"Downloading image from {image_url}...")
        urllib.request.urlretrieve(image_url, image_path)
        print(f"✅ Image downloaded and saved as {base_filename}")
        return base_filename
    except urllib.error.URLError as e:
        print(f"❌ Error downloading image: {e}")
        return None
    except Exception as e:
        print(f"❌ Error saving image: {e}")
        return None

def clone_game_page(game_name, frame_url, image_name):
    """Clone 1v1-lol.html and modify it for a new game."""
    # Create slug from game name
    slug = create_slug(game_name)
    
    # Define source and target paths
    source_path = os.path.join("go", "1v1-lol.html")
    target_path = os.path.join("go", f"{slug}.html")
    
    if not os.path.exists(source_path):
        print(f"Error: Source template {source_path} not found.")
        return False
    
    # Create go directory if it doesn't exist
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    # Check if target already exists
    if os.path.exists(target_path):
        print(f"Warning: Game page {target_path} already exists. Skipping clone.")
        return False
    
    try:
        # Read the template
        with open(source_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update game title
        content = re.sub(r'<title>.*?</title>', f'<title>{game_name} | Monkey Mart Games</title>', content)
        
        # Update iframe URL (both data-url and src attributes)
        content = re.sub(r'<div data-url="[^"]*"', f'<div data-url="{frame_url}"', content)
        content = re.sub(r'<iframe[^>]*src="[^"]*"', f'<iframe allowfullscreen="" frameborder="0" height="100%" id="game-iframe" scrolling="none" src="{frame_url}"', content)
        
        # Update h1 title
        content = re.sub(r'<h1 class="section-title">.*?</h1>', f'<h1 class="section-title">{game_name}</h1>', content)
        
        # Update meta description
        content = re.sub(
            r'<meta content=".*?" name="description"/>',
            f'<meta content="Play {game_name}, an exciting online game at Monkey Mart Games. Have fun with this free browser game!" name="description"/>',
            content
        )
        
        # Update Open Graph meta tags
        content = re.sub(
            r'<meta property="og:title" content=".*?">',
            f'<meta property="og:title" content="{game_name} | Monkey Mart Games">',
            content
        )
        
        content = re.sub(
            r'<meta property="og:description" content=".*?">',
            f'<meta property="og:description" content="Play {game_name} online for free! Enjoy this exciting game with friends.">',
            content
        )
        
        content = re.sub(
            r'<meta property="og:image" content=".*?">',
            f'<meta property="og:image" content="https://monkeymart.one/img/games/{image_name}">',
            content
        )
        
        # Update Twitter meta tags
        content = re.sub(
            r'<meta property="twitter:title" content=".*?">',
            f'<meta property="twitter:title" content="{game_name} | Monkey Mart Games">',
            content
        )
        
        content = re.sub(
            r'<meta property="twitter:description" content=".*?">',
            f'<meta property="twitter:description" content="Play {game_name} online for free! Enjoy this exciting game with friends.">',
            content
        )
        
        content = re.sub(
            r'<meta property="twitter:image" content=".*?">',
            f'<meta property="twitter:image" content="https://monkeymart.one/img/games/{image_name}">',
            content
        )
        
        # Update canonical URL
        content = re.sub(
            r'<meta property="og:url" content=".*?">',
            f'<meta property="og:url" content="https://monkeymart.one/go/{slug}.html">',
            content
        )
        
        # Update sharing text
        content = re.sub(
            r"const text = encodeURIComponent\('.*?'\);",
            f"const text = encodeURIComponent('Play {game_name} - an awesome online game!');",
            content
        )
        
        content = re.sub(
            r"const description = encodeURIComponent\('.*?'\);",
            f"const description = encodeURIComponent('{game_name} - Play this exciting game online for free!');",
            content
        )
        
        # Write the modified content to the new file
        with open(target_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ Successfully created game page: {target_path}")
        return True
    
    except Exception as e:
        print(f"❌ Error creating game page: {str(e)}")
        return False

def add_game_to_homepage(game_name, slug, image_name):
    """Add the game to the homepage."""
    homepage_path = "index.html"
    
    if not os.path.exists(homepage_path):
        print(f"Error: Homepage {homepage_path} not found.")
        return False
    
    try:
        # Read the homepage
        with open(homepage_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the Popular Games section
        game_section_pattern = r'<div class="row ltn__tab-product-slider-one-active--- slick-arrow-1">'
        match = re.search(game_section_pattern, content)
        
        if not match:
            print("Error: Couldn't find the game section in the homepage.")
            return False
        
        # Create the new game HTML using the template
        new_game_html = f'''
<!-- {game_name} -->
<div class="col-lg-2 col-md-4 col-sm-6 col-6">
<a title="{game_name}" href="/go/{slug}.html">
<div class="product-img">
<img class="lazyload" alt="{game_name}" src="/img/games/{image_name}">
<div class="product-badge">
</div>
</div>
<div class="ltn__product-item ltn__product-item-3 text-left">
</div>
</a>
</div>'''
        
        # Insert the new game HTML after the game section tag
        position = match.end()
        updated_content = content[:position] + new_game_html + content[position:]
        
        # Write the updated content back to the homepage
        with open(homepage_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print(f"✅ Successfully added {game_name} to homepage")
        return True
    
    except Exception as e:
        print(f"❌ Error adding game to homepage: {str(e)}")
        return False

def add_game_to_category(game_name, slug, image_name, category_path):
    """Add the game to a category page."""
    if not os.path.exists(category_path):
        print(f"Error: Category page {category_path} not found.")
        return False
    
    try:
        # Read the category page
        with open(category_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the game section
        game_section_pattern = r'<div class="row ltn__tab-product-slider-one-active--- slick-arrow-1">'
        match = re.search(game_section_pattern, content)
        
        if not match:
            print(f"Error: Couldn't find the game section in {category_path}.")
            return False
        
        # Create the new game HTML
        new_game_html = f'''
<!-- ltn__product-item -->
<div class="col-lg-2 col-md-4 col-sm-6 col-6">
<a title="{game_name}" href="/go/{slug}.html">
<div class="product-img">
<img class="lazyload" alt="{game_name}" src="/img/games/{image_name}">
<div class="product-badge">
<span class="badge-new">New</span>
</div>
</div>
<div class="ltn__product-item ltn__product-item-3 text-left">
</div>
</a>
</div>'''
        
        # Insert the new game HTML after the game section tag
        position = match.end()
        updated_content = content[:position] + new_game_html + content[position:]
        
        # Write the updated content back to the category page
        with open(category_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print(f"✅ Successfully added {game_name} to {os.path.basename(category_path)}")
        return True
    
    except Exception as e:
        print(f"❌ Error adding game to category page: {str(e)}")
        return False

def get_available_categories():
    """Get a list of available category pages."""
    category_dir = "category"
    if not os.path.exists(category_dir):
        print(f"Warning: Directory {category_dir} does not exist.")
        return []
    
    return [f for f in os.listdir(category_dir) if os.path.isfile(os.path.join(category_dir, f)) and f.endswith('.html')]

def main():
    """Main function to add a new game."""
    print("=" * 50)
    print("GAME ADDER")
    print("=" * 50)
    
    # Get game name
    game_name = input("Enter game name: ").strip()
    if not game_name:
        print("Error: Game name cannot be empty.")
        return
    
    # Get frame URL
    frame_url = input("Enter iframe URL: ").strip()
    if not frame_url:
        print("Error: Frame URL cannot be empty.")
        return
    
    # Create slug from game name
    slug = create_slug(game_name)
    
    # Get image URL and download it
    image_url = input("Enter image URL: ").strip()
    if not image_url:
        print("Error: Image URL cannot be empty.")
        return
    
    # Download and save the image with slug-based filename
    image_name = download_image(image_url, slug)
    if not image_name:
        print("Failed to download image. Please check the URL and try again.")
        return
    
    # Clone the game page
    if clone_game_page(game_name, frame_url, image_name):
        # Add to homepage
        add_game_to_homepage(game_name, slug, image_name)
        
        # Display available categories
        available_categories = get_available_categories()
        if available_categories:
            print("\nAvailable categories:")
            for i, cat in enumerate(available_categories, 1):
                print(f"{i}. {cat}")
            
            # Get category selections
            try:
                selections = input("\nEnter the numbers of categories to add the game to (comma-separated, e.g., 1,3,5): ").strip()
                selected_indices = [int(idx.strip()) for idx in selections.split(",") if idx.strip().isdigit()]
                
                for idx in selected_indices:
                    if 1 <= idx <= len(available_categories):
                        category_path = os.path.join("category", available_categories[idx - 1])
                        add_game_to_category(game_name, slug, image_name, category_path)
                    else:
                        print(f"Invalid category selection: {idx}")
            except ValueError:
                print("Invalid input for categories.")
        else:
            print("No category pages found.")
        
        print("\n" + "=" * 50)
        print(f"Game {game_name} has been successfully added!")
        print("=" * 50)
    else:
        print("Failed to add the game.")

if __name__ == "__main__":
    main() 