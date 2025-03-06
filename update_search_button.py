import re
import os
import shutil
from bs4 import BeautifulSoup
import glob
import json

def backup_file(file_path):
    """Create a backup of the file before making changes."""
    backup_path = file_path + '.bak'
    shutil.copy2(file_path, backup_path)
    print(f"Created backup at {backup_path}")
    return backup_path

def update_search_functionality():
    """First, generate the HTML file list."""
    # Find all HTML files in the current directory and subdirectories
    html_files = glob.glob('**/*.html', recursive=True)
    
    # Create a list of file info
    file_info = []
    for file_path in html_files:
        # Normalize path
        normalized_path = file_path.replace('\\', '/')
        
        # Try to extract title from the HTML file
        title = extract_title_from_html(file_path)
        
        # If title extraction failed, use the filename
        if not title:
            title = os.path.basename(file_path).replace('.html', '').replace('-', ' ').title()
        
        file_info.append({
            'title': title,
            'path': normalized_path,
            'url': '/' + normalized_path
        })
    
    # Sort by title
    file_info.sort(key=lambda x: x['title'])
    
    # Create JavaScript with the file list
    js_content = f"""
// Generated HTML file list
const ALL_HTML_FILES = {json.dumps(file_info, indent=2)};
console.log("Loaded {len(file_info)} HTML files for search");
"""
    
    # Write to file
    output_file = 'html_files_list.js'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Generated list of {len(file_info)} HTML files in {output_file}")
    
    # Now update the search functionality in all HTML files
    for file_path in html_files:
        update_search_in_file(file_path)

def extract_title_from_html(file_path):
    """Extract title from an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Look for title tag
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            if title_match:
                return title_match.group(1).strip()
            
            # If no title tag, try h1
            h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content, re.IGNORECASE)
            if h1_match:
                return h1_match.group(1).strip()
    except Exception as e:
        print(f"Error extracting title from {file_path}: {e}")
    
    return None

def update_search_in_file(file_path):
    """Update the search functionality in a specific HTML file."""
    try:
        # Create backup
        backup_file(file_path)
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if the file already includes html_files_list.js
        if 'html_files_list.js' in content:
            print(f"{file_path} already includes html_files_list.js. Skipping.")
            return False
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Add link to html_files_list.js in head
        head = soup.find('head')
        if head:
            script_tag = soup.new_tag('script')
            script_tag['src'] = '/html_files_list.js'
            head.append(script_tag)
        
        # Find script containing search functionality
        search_script = soup.find('script', string=lambda s: s and 'search-button' in s)
        
        if search_script:
            # Replace the pageData initialization with code that uses ALL_HTML_FILES
            script_content = search_script.string
            
            # Replace the initPageData function
            updated_script = re.sub(
                r'async function initPageData\(\) \{.*?\}',
                '''async function initPageData() {
                // Use the pre-generated list of HTML files
                if (typeof ALL_HTML_FILES !== 'undefined') {
                    pageData = ALL_HTML_FILES;
                    console.log(`Loaded ${pageData.length} HTML files from pre-generated list`);
                    return;
                } else {
                    console.warn("ALL_HTML_FILES not found! Falling back to limited page discovery.");
                    // ... existing fallback code ...
                }
            }''',
                script_content,
                flags=re.DOTALL
            )
            
            # Update the script
            search_script.string = updated_script
            
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            
            print(f"Updated search functionality in {file_path}")
            return True
        else:
            print(f"Search script not found in {file_path}. Skipping.")
            return False
    except Exception as e:
        print(f"Error updating {file_path}: {str(e)}")
        return False

if __name__ == "__main__":
    update_search_functionality() 