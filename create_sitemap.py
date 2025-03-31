import os
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def get_all_html_files(directory):
    """Get all HTML files in a directory and its subdirectories."""
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def create_sitemap():
    """Create sitemap.xml from all HTML files."""
    # Create root element
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Base URL
    base_url = 'https://monkeymart.one'
    
    # Add main pages
    main_pages = [
        'index.html',
        'about.html',
        'contact.html',
        'privacy-policy.html',
        'terms-of-service.html'
    ]
    
    for page in main_pages:
        if os.path.exists(page):
            url = ET.SubElement(urlset, 'url')
            loc = ET.SubElement(url, 'loc')
            loc.text = f'{base_url}/{page}'
            lastmod = ET.SubElement(url, 'lastmod')
            lastmod.text = datetime.now().strftime('%Y-%m-%d')
            changefreq = ET.SubElement(url, 'changefreq')
            changefreq.text = 'daily'
            priority = ET.SubElement(url, 'priority')
            priority.text = '1.0'
    
    # Add category pages
    category_dir = 'category'
    if os.path.exists(category_dir):
        category_files = get_all_html_files(category_dir)
        for file in category_files:
            url = ET.SubElement(urlset, 'url')
            loc = ET.SubElement(url, 'loc')
            # Convert file path to URL path
            url_path = file.replace('\\', '/').replace('./', '')
            loc.text = f'{base_url}/{url_path}'
            lastmod = ET.SubElement(url, 'lastmod')
            lastmod.text = datetime.now().strftime('%Y-%m-%d')
            changefreq = ET.SubElement(url, 'changefreq')
            changefreq.text = 'weekly'
            priority = ET.SubElement(url, 'priority')
            priority.text = '0.8'
    
    # Add game pages from go directory
    game_dir = 'go'
    if os.path.exists(game_dir):
        game_files = get_all_html_files(game_dir)
        for file in game_files:
            url = ET.SubElement(urlset, 'url')
            loc = ET.SubElement(url, 'loc')
            # Convert file path to URL path
            url_path = file.replace('\\', '/').replace('./', '')
            loc.text = f'{base_url}/{url_path}'
            lastmod = ET.SubElement(url, 'lastmod')
            lastmod.text = datetime.now().strftime('%Y-%m-%d')
            changefreq = ET.SubElement(url, 'changefreq')
            changefreq.text = 'weekly'
            priority = ET.SubElement(url, 'priority')
            priority.text = '0.9'
    
    # Add game pages from game directory
    game_dir = 'game'
    if os.path.exists(game_dir):
        game_files = get_all_html_files(game_dir)
        for file in game_files:
            url = ET.SubElement(urlset, 'url')
            loc = ET.SubElement(url, 'loc')
            # Convert file path to URL path
            url_path = file.replace('\\', '/').replace('./', '')
            loc.text = f'{base_url}/{url_path}'
            lastmod = ET.SubElement(url, 'lastmod')
            lastmod.text = datetime.now().strftime('%Y-%m-%d')
            changefreq = ET.SubElement(url, 'changefreq')
            changefreq.text = 'weekly'
            priority = ET.SubElement(url, 'priority')
            priority.text = '0.9'
    
    # Create XML tree with proper formatting
    xmlstr = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="  ")
    
    # Write to file
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xmlstr)
    
    print("✅ Sitemap.xml has been created successfully!")

if __name__ == "__main__":
    create_sitemap() 