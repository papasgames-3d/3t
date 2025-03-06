import os
import datetime
from xml.dom import minidom
import re
from urllib.parse import urljoin
import glob

def generate_sitemap(domain_url='https://monkeymart.one/', output_file='sitemap.xml'):
    """
    Generate a sitemap for the entire website.
    
    Args:
        domain_url: The base URL of the website
        output_file: The output sitemap file name
    """
    # Ensure domain URL ends with a slash
    if not domain_url.endswith('/'):
        domain_url += '/'
    
    # Create the sitemap document
    doc = minidom.getDOMImplementation().createDocument(None, 'urlset', None)
    root = doc.documentElement
    root.setAttribute('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Get current date in the format required for sitemap
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Counter for tracking pages
    page_count = 0
    
    # Priority settings based on page type
    priority_settings = {
        'index.html': '1.0',          # Homepage
        'category': '0.8',            # Category pages
        'go/': '0.7',                 # Game pages
        'default': '0.5'              # Other pages
    }
    
    # Find all HTML files in the current directory and subdirectories
    html_files = []
    
    # Add index.html first (if it exists)
    if os.path.exists('index.html'):
        html_files.append('index.html')
    
    # Find all other HTML files
    for file_path in glob.glob('**/*.html', recursive=True):
        if file_path != 'index.html':  # Skip index.html as we've already added it
            html_files.append(file_path)
    
    # Find all HTML files in the 'go' directory specifically (game pages)
    go_files = glob.glob('go/*.html')
    
    # Process all HTML files
    for file_path in html_files:
        # Skip certain files that shouldn't be in the sitemap
        if 'error' in file_path.lower() or '404' in file_path:
            continue
            
        # Convert file path to URL
        file_path = file_path.replace('\\', '/')  # Normalize path separators
        
        # Set appropriate URL
        url = urljoin(domain_url, file_path)
        
        # Determine priority based on page type
        priority = priority_settings['default']
        if file_path == 'index.html':
            priority = priority_settings['index.html']
            # Homepage URL should be the domain root
            url = domain_url
        elif 'category' in file_path:
            priority = priority_settings['category']
        elif file_path.startswith('go/'):
            priority = priority_settings['go/']
        
        # Determine change frequency based on page type
        if file_path == 'index.html':
            changefreq = 'daily'
        elif 'category' in file_path:
            changefreq = 'weekly'
        else:
            changefreq = 'monthly'
        
        # Create URL entry
        url_element = doc.createElement('url')
        
        # Add location
        loc = doc.createElement('loc')
        loc_text = doc.createTextNode(url)
        loc.appendChild(loc_text)
        url_element.appendChild(loc)
        
        # Add last modified date
        lastmod = doc.createElement('lastmod')
        lastmod_text = doc.createTextNode(today)
        lastmod.appendChild(lastmod_text)
        url_element.appendChild(lastmod)
        
        # Add change frequency
        freq = doc.createElement('changefreq')
        freq_text = doc.createTextNode(changefreq)
        freq.appendChild(freq_text)
        url_element.appendChild(freq)
        
        # Add priority
        pri = doc.createElement('priority')
        pri_text = doc.createTextNode(priority)
        pri.appendChild(pri_text)
        url_element.appendChild(pri)
        
        # Add URL to root
        root.appendChild(url_element)
        page_count += 1
    
    # Write the sitemap to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(doc.toprettyxml(indent='  ', encoding='UTF-8').decode('utf-8'))
    
    print(f"Sitemap generated successfully at {output_file}")
    print(f"Total pages in sitemap: {page_count}")

if __name__ == "__main__":
    # Ask for domain confirmation
    print("Generating sitemap for your website...")
    default_domain = "https://monkeymart.one/"
    domain = input(f"Enter your domain (default: {default_domain}): ") or default_domain
    
    # Generate the sitemap
    generate_sitemap(domain)
    
    print("\nDon't forget:")
    print("1. Check sitemap.xml to ensure it's correct")
    print("2. Add the sitemap path to your robots.txt:")
    print("   Sitemap: https://monkeymart.one/sitemap.xml")
    print("3. Submit your sitemap to Google Search Console to speed up indexing") 