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
        
        /* Dark mode compatibility */
        [data-theme="dark"] .search-modal-content {
            background-color: #222;
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
            
            // Game title and URL mapping
            let gameData = [];
            
            // Function to initialize game data
            async function initGameData() {
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
            
            // Function to perform search
            function performSearch(query) {
                // Clear previous results
                searchResults.innerHTML = '';
                
                if (!query.trim()) {
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
            
            // Open search modal
            searchButton.addEventListener('click', function() {
                searchModal.style.display = 'block';
                searchInput.focus();
                
                // Initialize game data if not already done
                if (gameData.length === 0) {
                    initGameData();
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