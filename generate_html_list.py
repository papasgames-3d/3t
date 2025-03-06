import os
import glob
import json

def generate_html_file_list(output_file='html_files_list.js'):
    """Generate a JavaScript file containing a list of all HTML files."""
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
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Generated list of {len(file_info)} HTML files in {output_file}")
    return file_info

def extract_title_from_html(file_path):
    """Extract title from an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Look for title tag
            import re
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

if __name__ == "__main__":
    generate_html_file_list() 