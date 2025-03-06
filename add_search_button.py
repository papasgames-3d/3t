import re
import os
import shutil
from bs4 import BeautifulSoup
import glob

def backup_file(file_path):
    """Create a backup of the file before making changes."""
    backup_path = file_path + '.bak'
    shutil.copy2(file_path, backup_path)
    print(f"Created backup at {backup_path}")
    return backup_path

def add_search_functionality(file_path):
    """Add search button to header next to dark mode button and implement search functionality."""
    try:
        # Create backup
        backup_file(file_path)
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 1. Find the dark mode button in the header
        dark_mode_button = soup.select_one('.darkmode-button, .dark-mode-toggle, [id*="dark"], [class*="dark"]')
        
        if not dark_mode_button:
            # Try to find header or nav element
            header = soup.select_one('header, .header, nav, .nav')
            if header:
                dark_mode_button = header
            else:
                print(f"Header element not found in {file_path}. Cannot add search button.")
                return False
        
        # Check if search button already exists
        existing_search = soup.select_one('#search-button, .search-button')
        if existing_search:
            print(f"Search button already exists in {file_path}. Skipping.")
            return False
        
        # 2. Create search button HTML
        search_button_html = '''
        <div class="search-container">
            <button id="search-button" class="search-button" aria-label="Search">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
            </button>
            <div id="search-modal" class="search-modal">
                <div class="search-modal-content">
                    <span class="search-close">&times;</span>
                    <h2>Search</h2>
                    <input type="text" id="search-input" placeholder="Enter search keywords...">
                    <div class="search-tabs">
                        <button class="search-tab active" data-tab="games">Games</button>
                        <button class="search-tab" data-tab="pages">All Pages</button>
                    </div>
                    <div id="search-results"></div>
                </div>
            </div>
        </div>
        '''
        
        # 3. Add search button next to dark mode button
        if dark_mode_button.name == 'header' or dark_mode_button.name == 'nav':
            # If we're working with a header/nav element, add to the end
            dark_mode_button.append(BeautifulSoup(search_button_html, 'html.parser'))
        else:
            # Insert after the dark mode button
            dark_mode_button.insert_after(BeautifulSoup(search_button_html, 'html.parser'))
        
        # 4. Add CSS for search button and modal
        search_css = '''
        <style>
        /* Search Button and Modal Styles */
        .search-container {
            position: relative;
            display: inline-block;
            margin-left: 10px;
        }
        
        .search-button {
            background: transparent;
            border: none;
            cursor: pointer;
            padding: 5px;
            display: flex;
            align-items: center;
            color: inherit;
        }
        
        .search-button:hover {
            opacity: 0.8;
        }
        
        .search-modal {
            display: none;
            position: fixed;
            z-index: 9999;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            overflow: auto;
        }
        
        .search-modal-content {
            background-color: var(--bg-color, #fff);
            color: var(--text-color, #333);
            margin: 10% auto;
            padding: 20px;
            border-radius: 8px;
            width: 80%;
            max-width: 600px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            position: relative;
        }
        
        .search-close {
            color: var(--text-color, #333);
            position: absolute;
            top: 10px;
            right: 20px;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        
        .search-tabs {
            display: flex;
            border-bottom: 1px solid #ddd;
            margin-bottom: 15px;
            margin-top: 15px;
        }
        
        .search-tab {
            background: none;
            border: none;
            padding: 8px 15px;
            cursor: pointer;
            font-size: 16px;
            color: var(--text-color, #333);
            opacity: 0.7;
        }
        
        .search-tab.active {
            opacity: 1;
            font-weight: bold;
            border-bottom: 2px solid var(--accent-color, #0066cc);
        }
        
        #search-input {
            width: 100%;
            padding: 12px;
            margin: 15px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
            background-color: var(--input-bg, #fff);
            color: var(--input-color, #333);
        }
        
        #search-results {
            max-height: 50vh;
            overflow-y: auto;
            margin-top: 15px;
        }
        
        .search-result-item {
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 4px;
            background-color: var(--item-bg, #f9f9f9);
            transition: background-color 0.2s;
        }
        
        .search-result-item:hover {
            background-color: var(--item-hover, #eaeaea);
        }
        
        .search-result-item a {
            color: var(--link-color, #0066cc);
            text-decoration: none;
            font-weight: 500;
            display: block;
        }
        
        .search-result-item .file-path {
            font-size: 12px;
            color: #666;
            margin-top: 3px;
        }
        
        .search-category {
            font-weight: bold;
            margin: 10px 0;
            padding: 5px;
            border-bottom: 1px solid #eee;
        }
        
        /* Dark mode compatibility */
        [data-theme="dark"] .search-modal-content {
            background-color: #222;
            color: #eee;
        }
        
        [data-theme="dark"] .search-tab {
            color: #eee;
        }
        
        [data-theme="dark"] #search-input {
            background-color: #333;
            color: #eee;
            border-color: #444;
        }
        
        [data-theme="dark"] .search-result-item {
            background-color: #333;
        }
        
        [data-theme="dark"] .search-result-item:hover {
            background-color: #444;
        }
        
        [data-theme="dark"] .search-result-item a {
            color: #4da6ff;
        }
        
        [data-theme="dark"] .search-close {
            color: #eee;
        }
        
        [data-theme="dark"] .search-result-item .file-path {
            color: #aaa;
        }
        
        [data-theme="dark"] .search-category {
            border-bottom-color: #444;
        }
        
        @media (max-width: 768px) {
            .search-modal-content {
                width: 95%;
                margin: 15% auto;
            }
        }
        </style>
        '''
        
        # Check if CSS already exists
        existing_search_css = soup.find('style', string=lambda x: x and 'search-container' in x)
        if not existing_search_css:
            # Add CSS to head
            head = soup.find('head')
            if head:
                head.append(BeautifulSoup(search_css, 'html.parser'))
        
        # 5. Add JavaScript for search functionality
        search_js = '''
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Get elements
            const searchButton = document.getElementById('search-button');
            const searchModal = document.getElementById('search-modal');
            const searchClose = document.querySelector('.search-close');
            const searchInput = document.getElementById('search-input');
            const searchResults = document.getElementById('search-results');
            const searchTabs = document.querySelectorAll('.search-tab');
            
            // Game title and URL mapping
            let gameData = [];
            // All HTML pages data
            let pageData = [];
            // Current active tab
            let activeTab = 'games';
            
            // Function to get page title from HTML content
            function extractTitleFromHtml(html) {
                const titleMatch = html.match(/<title[^>]*>([^<]+)<\\/title>/i);
                if (titleMatch && titleMatch[1]) {
                    return titleMatch[1].trim();
                }
                return null;
            }
            
            // Function to initialize game data
            async function initGameData() {
                if (gameData.length > 0) return; // Already initialized
                
                try {
                    // First, try to get data from any existing list items (for homepage)
                    const gameElements = document.querySelectorAll('.game-item, .game, [class*="game"]');
                    if (gameElements.length > 0) {
                        gameElements.forEach(element => {
                            const link = element.querySelector('a');
                            const titleElement = element.querySelector('h2, h3, h4, .title, [class*="title"]');
                            
                            if (link && titleElement) {
                                const url = link.getAttribute('href');
                                const title = titleElement.textContent.trim();
                                if (url && title) {
                                    gameData.push({ title, url });
                                }
                            }
                        });
                    }
                    
                    // If we found games on the current page
                    if (gameData.length > 0) {
                        console.log(`Found ${gameData.length} games on the current page.`);
                        return;
                    }
                    
                    // If not, try to fetch game data from the homepage
                    const response = await fetch('/index.html');
                    const text = await response.text();
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(text, 'text/html');
                    
                    const homepageGames = doc.querySelectorAll('.game-item, .game, [class*="game"]');
                    homepageGames.forEach(element => {
                        const link = element.querySelector('a');
                        const titleElement = element.querySelector('h2, h3, h4, .title, [class*="title"]');
                        
                        if (link && titleElement) {
                            const url = link.getAttribute('href');
                            const title = titleElement.textContent.trim();
                            if (url && title) {
                                gameData.push({ title, url });
                            }
                        }
                    });
                    
                    console.log(`Fetched ${gameData.length} games from homepage.`);
                } catch (error) {
                    console.error('Error initializing game data:', error);
                }
            }
            
            // Function to initialize all HTML pages data
            async function initPageData() {
                if (pageData.length > 0) return; // Already initialized
                
                try {
                    // Use a simple sitemap or known directory structure
                    // This is a simplified approach - in a real-world scenario, 
                    // you might want to use a proper sitemap.xml or server-side API
                    
                    // Common directories where HTML files might be located
                    const directories = ['/', '/go/', '/category/'];
                    
                    // Add the current page
                    const currentPath = window.location.pathname;
                    const currentTitle = document.title;
                    
                    pageData.push({
                        title: currentTitle,
                        url: currentPath,
                        path: currentPath
                    });
                    
                    // First try to fetch sitemap.xml if it exists
                    try {
                        const sitemapResponse = await fetch('/sitemap.xml');
                        if (sitemapResponse.ok) {
                            const sitemapText = await sitemapResponse.text();
                            const parser = new DOMParser();
                            const sitemapDoc = parser.parseFromString(sitemapText, 'text/xml');
                            
                            const locations = sitemapDoc.querySelectorAll('loc');
                            for (const loc of locations) {
                                const url = loc.textContent.trim();
                                if (url.endsWith('.html') || url.endsWith('/')) {
                                    // Extract the path from the URL
                                    const urlObj = new URL(url);
                                    const path = urlObj.pathname;
                                    
                                    // Skip duplicates
                                    if (!pageData.some(page => page.path === path)) {
                                        pageData.push({
                                            title: path.split('/').pop().replace('.html', '').replace(/-/g, ' '),
                                            url: path,
                                            path: path
                                        });
                                    }
                                }
                            }
                            
                            if (pageData.length > 1) {
                                console.log(`Loaded ${pageData.length} pages from sitemap.`);
                                
                                // Fetch titles for each page
                                for (const page of pageData) {
                                    if (page.path === currentPath) continue; // Skip current page
                                    try {
                                        const pageResponse = await fetch(page.url);
                                        const pageText = await pageResponse.text();
                                        const pageTitle = extractTitleFromHtml(pageText);
                                        if (pageTitle) {
                                            page.title = pageTitle;
                                        }
                                    } catch (error) {
                                        console.warn(`Could not fetch title for ${page.url}`);
                                    }
                                }
                                
                                return; // We already loaded pages from sitemap
                            }
                        }
                    } catch (error) {
                        console.warn('Could not load sitemap:', error);
                    }
                    
                    // If sitemap didn't work, try to fetch from known directories
                    for (const dir of directories) {
                        try {
                            const response = await fetch(dir);
                            if (!response.ok) continue;
                            
                            const text = await response.text();
                            const parser = new DOMParser();
                            const doc = parser.parseFromString(text, 'text/html');
                            
                            // Try to extract links
                            const links = doc.querySelectorAll('a[href]');
                            for (const link of links) {
                                const href = link.getAttribute('href');
                                if (href && (href.endsWith('.html') || href.endsWith('/'))) {
                                    // Skip external links
                                    if (href.startsWith('http') && !href.includes(window.location.hostname)) {
                                        continue;
                                    }
                                    
                                    // Convert to absolute path if needed
                                    let path = href;
                                    if (href.startsWith('/')) {
                                        path = href;
                                    } else if (!href.startsWith('http')) {
                                        path = dir + href;
                                    } else {
                                        const urlObj = new URL(href);
                                        path = urlObj.pathname;
                                    }
                                    
                                    // Clean up path
                                    path = path.replace(/\\/+/g, '/');
                                    
                                    // Skip duplicates
                                    if (!pageData.some(page => page.path === path)) {
                                        // Get title from link text or path
                                        const title = link.textContent.trim() || path.split('/').pop().replace('.html', '').replace(/-/g, ' ');
                                        
                                        pageData.push({
                                            title: title,
                                            url: path,
                                            path: path
                                        });
                                    }
                                }
                            }
                        } catch (error) {
                            console.warn(`Error fetching directory ${dir}:`, error);
                        }
                    }
                    
                    console.log(`Found ${pageData.length} HTML pages.`);
                    
                    // If we still don't have many pages, add some common ones
                    if (pageData.length < 5) {
                        const commonPages = [
                            { title: 'Homepage', url: '/', path: '/' },
                            { title: 'Games', url: '/go/', path: '/go/' },
                            { title: 'Categories', url: '/category/', path: '/category/' }
                        ];
                        
                        for (const page of commonPages) {
                            if (!pageData.some(p => p.path === page.path)) {
                                pageData.push(page);
                            }
                        }
                    }
                    
                    // Sort pages by title
                    pageData.sort((a, b) => a.title.localeCompare(b.title));
                    
                } catch (error) {
                    console.error('Error initializing page data:', error);
                }
            }
            
            // Function to perform search
            function performSearch(query) {
                // Clear previous results
                searchResults.innerHTML = '';
                
                if (activeTab === 'games') {
                    searchGames(query);
                } else {
                    searchPages(query);
                }
            }
            
            // Function to search games
            function searchGames(query) {
                if (!query.trim()) {
                    // Show all games if no query
                    displayAllGames();
                    return;
                }
                
                query = query.toLowerCase();
                const results = gameData.filter(game => 
                    game.title.toLowerCase().includes(query)
                );
                
                if (results.length === 0) {
                    searchResults.innerHTML = '<div class="no-results">No results found.</div>';
                    return;
                }
                
                // Sort results by relevance
                results.sort((a, b) => {
                    const aStartsWith = a.title.toLowerCase().startsWith(query);
                    const bStartsWith = b.title.toLowerCase().startsWith(query);
                    
                    if (aStartsWith && !bStartsWith) return -1;
                    if (!aStartsWith && bStartsWith) return 1;
                    return a.title.localeCompare(b.title);
                });
                
                // Display results
                searchResults.innerHTML = '<div class="search-category">Games</div>';
                results.forEach(game => {
                    const resultItem = document.createElement('div');
                    resultItem.className = 'search-result-item';
                    
                    const link = document.createElement('a');
                    link.href = game.url;
                    link.textContent = game.title;
                    
                    resultItem.appendChild(link);
                    searchResults.appendChild(resultItem);
                });
            }
            
            // Function to search pages
            function searchPages(query) {
                if (!query.trim()) {
                    // Show all pages if no query
                    displayAllPages();
                    return;
                }
                
                query = query.toLowerCase();
                const results = pageData.filter(page => 
                    page.title.toLowerCase().includes(query) || 
                    page.path.toLowerCase().includes(query)
                );
                
                if (results.length === 0) {
                    searchResults.innerHTML = '<div class="no-results">No results found.</div>';
                    return;
                }
                
                // Sort results by relevance
                results.sort((a, b) => {
                    const aTitle = a.title.toLowerCase();
                    const bTitle = b.title.toLowerCase();
                    const aPath = a.path.toLowerCase();
                    const bPath = b.path.toLowerCase();
                    
                    const aTitleStarts = aTitle.startsWith(query);
                    const bTitleStarts = bTitle.startsWith(query);
                    const aPathStarts = aPath.startsWith(query);
                    const bPathStarts = bPath.startsWith(query);
                    
                    if (aTitleStarts && !bTitleStarts) return -1;
                    if (!aTitleStarts && bTitleStarts) return 1;
                    if (aPathStarts && !bPathStarts) return -1;
                    if (!aPathStarts && bPathStarts) return 1;
                    
                    return aTitle.localeCompare(bTitle);
                });
                
                // Display results
                searchResults.innerHTML = '<div class="search-category">Pages</div>';
                results.forEach(page => {
                    const resultItem = document.createElement('div');
                    resultItem.className = 'search-result-item';
                    
                    const link = document.createElement('a');
                    link.href = page.url;
                    link.textContent = page.title;
                    
                    const filePath = document.createElement('div');
                    filePath.className = 'file-path';
                    filePath.textContent = page.path;
                    
                    resultItem.appendChild(link);
                    resultItem.appendChild(filePath);
                    searchResults.appendChild(resultItem);
                });
            }
            
            // Function to display all games
            function displayAllGames() {
                searchResults.innerHTML = '<div class="search-category">All Games</div>';
                
                // Sort games alphabetically
                const sortedGames = [...gameData].sort((a, b) => 
                    a.title.localeCompare(b.title)
                );
                
                sortedGames.forEach(game => {
                    const resultItem = document.createElement('div');
                    resultItem.className = 'search-result-item';
                    
                    const link = document.createElement('a');
                    link.href = game.url;
                    link.textContent = game.title;
                    
                    resultItem.appendChild(link);
                    searchResults.appendChild(resultItem);
                });
                
                if (sortedGames.length === 0) {
                    searchResults.innerHTML = '<div class="no-results">No games found. Try the "All Pages" tab.</div>';
                }
            }
            
            // Function to display all HTML pages
            function displayAllPages() {
                searchResults.innerHTML = '<div class="search-category">All Pages</div>';
                
                // Group pages by directory
                const pagesByDir = {};
                pageData.forEach(page => {
                    const path = page.path;
                    const dirPath = path.substring(0, path.lastIndexOf('/') + 1) || '/';
                    
                    if (!pagesByDir[dirPath]) {
                        pagesByDir[dirPath] = [];
                    }
                    
                    pagesByDir[dirPath].push(page);
                });
                
                // Sort directories
                const sortedDirs = Object.keys(pagesByDir).sort();
                
                // Display pages grouped by directory
                sortedDirs.forEach(dir => {
                    // Add directory header
                    const dirHeader = document.createElement('div');
                    dirHeader.className = 'search-result-item';
                    dirHeader.innerHTML = `<strong>${dir}</strong>`;
                    searchResults.appendChild(dirHeader);
                    
                    // Sort pages in this directory
                    const sortedPages = pagesByDir[dir].sort((a, b) => 
                        a.title.localeCompare(b.title)
                    );
                    
                    // Add pages
                    sortedPages.forEach(page => {
                        const resultItem = document.createElement('div');
                        resultItem.className = 'search-result-item';
                        
                        const link = document.createElement('a');
                        link.href = page.url;
                        link.textContent = page.title;
                        
                        const filePath = document.createElement('div');
                        filePath.className = 'file-path';
                        filePath.textContent = page.path;
                        
                        resultItem.appendChild(link);
                        resultItem.appendChild(filePath);
                        searchResults.appendChild(resultItem);
                    });
                });
                
                if (Object.keys(pagesByDir).length === 0) {
                    searchResults.innerHTML = '<div class="no-results">No pages found.</div>';
                }
            }
            
            // Handle tab switching
            searchTabs.forEach(tab => {
                tab.addEventListener('click', function() {
                    // Remove active class from all tabs
                    searchTabs.forEach(t => t.classList.remove('active'));
                    // Add active class to clicked tab
                    this.classList.add('active');
                    
                    // Update active tab
                    activeTab = this.dataset.tab;
                    
                    // Clear search input
                    searchInput.value = '';
                    
                    // Reinitialize data if needed
                    if (activeTab === 'games' && gameData.length === 0) {
                        initGameData().then(() => displayAllGames());
                    } else if (activeTab === 'pages' && pageData.length === 0) {
                        initPageData().then(() => displayAllPages());
                    } else {
                        // Show appropriate results
                        if (activeTab === 'games') {
                            displayAllGames();
                        } else {
                            displayAllPages();
                        }
                    }
                });
            });
            
            // Open search modal
            searchButton.addEventListener('click', function() {
                searchModal.style.display = 'block';
                searchInput.focus();
                
                // Initialize data for current tab
                if (activeTab === 'games') {
                    if (gameData.length === 0) {
                        initGameData().then(() => displayAllGames());
                    } else {
                        displayAllGames();
                    }
                } else {
                    if (pageData.length === 0) {
                        initPageData().then(() => displayAllPages());
                    } else {
                        displayAllPages();
                    }
                }
            });
            
            // Close search modal
            searchClose.addEventListener('click', function() {
                searchModal.style.display = 'none';
            });
            
            // Close modal when clicking outside
            window.addEventListener('click', function(event) {
                if (event.target === searchModal) {
                    searchModal.style.display = 'none';
                }
            });
            
            // Handle search input
            searchInput.addEventListener('input', function() {
                performSearch(this.value);
            });
            
            // Close with ESC key
            document.addEventListener('keydown', function(event) {
                if (event.key === 'Escape' && searchModal.style.display === 'block') {
                    searchModal.style.display = 'none';
                }
            });
            
            // Initialize game data on page load
            initGameData();
        });
        </script>
        '''
        
        # Check if JavaScript already exists
        existing_search_js = soup.find('script', string=lambda x: x and 'search-button' in x)
        if not existing_search_js:
            # Add JavaScript before the closing body tag
            body = soup.find('body')
            if body:
                body.append(BeautifulSoup(search_js, 'html.parser'))
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        
        print(f"Search functionality added to {file_path}")
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def process_all_html_files():
    """Process all HTML files in the current directory and subdirectories."""
    # Get all HTML files in the current directory and subdirectories
    html_files = glob.glob('**/*.html', recursive=True)
    
    # Stats
    successful = 0
    failed = 0
    skipped = 0
    
    print(f"Found {len(html_files)} HTML files to process")
    
    # Process each file
    for file_path in html_files:
        print(f"\nProcessing {file_path}...")
        result = add_search_functionality(file_path)
        
        if result is True:
            successful += 1
        elif result is False:
            skipped += 1
        else:
            failed += 1
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Total HTML files: {len(html_files)}")
    print(f"Successfully processed: {successful}")
    print(f"Skipped (search already exists or no header): {skipped}")
    print(f"Failed: {failed}")
    print("Search button has been added to all applicable HTML files.")

if __name__ == "__main__":
    process_all_html_files() 