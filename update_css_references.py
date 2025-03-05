import os
import re
import time

def update_css_references(file_path):
    """Replace multiple CSS references with a single reference to combined-styles.css"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Define the CSS files to look for
        css_files = ['layout.css', 'category-pages.css', 'game-pages.css']
        
        # Check if any of these CSS files are referenced
        css_references_found = False
        for css_file in css_files:
            if f'href="/css/{css_file}"' in content or f'href="css/{css_file}"' in content:
                css_references_found = True
                break
        
        if not css_references_found:
            return False
        
        # Define pattern to match the CSS link tags
        patterns = [
            r'<link[^>]*href="/css/layout.css"[^>]*>',
            r'<link[^>]*href="/css/category-pages.css"[^>]*>',
            r'<link[^>]*href="/css/game-pages.css"[^>]*>',
            r'<link[^>]*href="css/layout.css"[^>]*>',
            r'<link[^>]*href="css/category-pages.css"[^>]*>',
            r'<link[^>]*href="css/game-pages.css"[^>]*>'
        ]
        
        # Keep track of modifications
        modified = False
        
        # Replace the first occurrence with combined-styles.css and remove the rest
        first_replaced = False
        for pattern in patterns:
            matches = list(re.finditer(pattern, content))
            if matches:
                modified = True
                if not first_replaced:
                    # Replace first instance with combined-styles.css
                    replacement = '<link rel="stylesheet" href="/css/combined-styles.css">'
                    content = re.sub(pattern, replacement, content, count=1)
                    first_replaced = True
                else:
                    # Remove all other instances
                    for match in matches:
                        content = content.replace(match.group(0), '')
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def process_directory(directory='.'):
    """Process all HTML files in the directory and subdirectories"""
    start_time = time.time()
    count_total = 0
    count_modified = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                count_total += 1
                if update_css_references(file_path):
                    count_modified += 1
                    print(f"✅ Updated: {file_path}")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print("\n" + "="*50)
    print(f"CSS reference update complete!")
    print(f"- Total HTML files checked: {count_total}")
    print(f"- Files modified: {count_modified}")
    print(f"- Execution time: {execution_time:.2f} seconds")
    print("="*50)

if __name__ == "__main__":
    print("="*50)
    print("CSS References Updater")
    print("="*50)
    print("This script will replace references to layout.css, category-pages.css,")
    print("and game-pages.css with a single reference to combined-styles.css.")
    print("This will improve page loading time and reduce HTTP requests.")
    print("\nProcessing files...")
    
    process_directory() 