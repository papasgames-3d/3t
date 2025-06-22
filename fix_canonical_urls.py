#!/usr/bin/env python3
"""
Script to fix canonical URLs and og:url meta tags across the entire website.
This script will:
1. Find all HTML files in the website
2. Fix canonical URLs to point to the correct page URLs
3. Fix og:url meta tags to point to the correct page URLs
4. Update lang attribute to "en" for English content
"""

import os
import re
import glob
from pathlib import Path

def get_correct_url(file_path):
    """Generate the correct canonical URL for a given file path."""
    # Remove the base directory path
    relative_path = file_path.replace('\\', '/')
    
    # Handle different file types
    if relative_path == 'index.html':
        return 'https://monkeymart.one/'
    elif relative_path.startswith('game/'):
        game_name = relative_path.replace('game/', '').replace('.html', '')
        return f'https://monkeymart.one/game/{game_name}.html'
    elif relative_path.startswith('note/'):
        note_name = relative_path.replace('note/', '').replace('.html', '')
        return f'https://monkeymart.one/note/{note_name}.html'
    elif relative_path.startswith('category/'):
        category_name = relative_path.replace('category/', '').replace('.html', '')
        return f'https://monkeymart.one/category/{category_name}.html'
    else:
        # For other files in root directory
        file_name = relative_path.replace('.html', '')
        return f'https://monkeymart.one/{file_name}.html'

def fix_html_file(file_path):
    """Fix canonical URLs and og:url meta tags in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix lang attribute
        content = re.sub(r'<html[^>]*lang="[^"]*"', '<html lang="en"', content)
        content = re.sub(r'<html([^>]*?)>', r'<html\1 lang="en">', content)
        
        # Get correct URL for this file
        correct_url = get_correct_url(file_path)
        
        # Fix canonical URL
        content = re.sub(
            r'<link[^>]*rel="canonical"[^>]*href="[^"]*"[^>]*>',
            f'<link href="{correct_url}" rel="canonical"/>',
            content
        )
        
        # Fix og:url meta tag
        content = re.sub(
            r'<meta[^>]*property="og:url"[^>]*content="[^"]*"[^>]*>',
            f'<meta content="{correct_url}" property="og:url"/>',
            content
        )
        
        # If content was changed, write it back
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {file_path}")
            return True
        else:
            print(f"ℹ️  No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def main():
    """Main function to process all HTML files."""
    print("🔧 Starting canonical URL fix process...")
    print("=" * 50)
    
    # Find all HTML files
    html_files = []
    
    # Root directory files
    html_files.extend(glob.glob("*.html"))
    
    # Game directory files
    html_files.extend(glob.glob("game/*.html"))
    
    # Note directory files
    html_files.extend(glob.glob("note/*.html"))
    
    # Category directory files
    html_files.extend(glob.glob("category/*.html"))
    
    print(f"📁 Found {len(html_files)} HTML files to process")
    print("=" * 50)
    
    fixed_count = 0
    total_count = len(html_files)
    
    for file_path in html_files:
        if fix_html_file(file_path):
            fixed_count += 1
    
    print("=" * 50)
    print(f"🎉 Process completed!")
    print(f"📊 Files processed: {total_count}")
    print(f"🔧 Files fixed: {fixed_count}")
    print(f"✅ Success rate: {(fixed_count/total_count)*100:.1f}%")
    
    # Show examples of fixes
    print("\n📋 Examples of URL fixes:")
    print("- index.html: https://monkeymart.one/")
    print("- game/monkey-mart.html: https://monkeymart.one/game/monkey-mart.html")
    print("- note/guide.html: https://monkeymart.one/note/guide.html")
    print("- about.html: https://monkeymart.one/about.html")

if __name__ == "__main__":
    main() 