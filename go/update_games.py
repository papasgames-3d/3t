import os  
from bs4 import BeautifulSoup  
import re  

# HTML template for the game wrapper and controls  
GAME_WRAPPER_TEMPLATE = """  
<section class="game-wrapper" id="game">  
    <div class="game-container">  
        <div id="game-arena">  
            {iframe_tag}  
        </div>  
    </div>  
    <div id="game-controls">  
        <a class="func-btn" href="javascript:void(0);" onclick="openFullscreen()" id="fullscreen-btn" title="Full Screen">  
            <svg class="bi bi-arrows-fullscreen" fill="currentColor" height="23" viewbox="0 0 16 16" width="23" xmlns="http://www.w3.org/2000/svg">  
                <path d="M5.828 10.172a.5.5 0 0 0-.707 0l-4.096 4.096V11.5a.5.5 0 0 0-1 0v3.975a.5.5 0 0 0 .5.5H4.5a.5.5 0 0 0 0-1H1.732l4.096-4.096a.5.5 0 0 0 0-.707m4.344 0a.5.5 0 0 1 .707 0l4.096 4.096V11.5a.5.5 0 1 1 1 0v3.975a.5.5 0 0 1-.5.5H11.5a.5.5 0 0 1 0-1h2.768l-4.096-4.096a.5.5 0 0 1 0-.707m0-4.344a.5.5 0 0 0 .707 0l4.096-4.096V4.5a.5.5 0 1 0 1 0V.525a.5.5 0 0 0-.5-.5H11.5a.5.5 0 0 0 0 1h2.768l-4.096 4.096a.5.5 0 0 0 0 .707m-4.344 0a.5.5 0 0 1-.707 0L1.025 1.732V4.5a.5.5 0 0 1-1 0V.525a.5.5 0 0 1 .5-.5H4.5a.5.5 0 0 1 0 1H1.732l4.096 4.096a.5.5 0 0 1 0 .707" fill-rule="evenodd"></path>  
            </svg>  
        </a>  
    </div>  
</section>  
"""  

FULLSCREEN_SCRIPT = """  
<script>  
function openFullscreen() {  
    try {  
        const iframe = document.getElementById('game-iframe');  
        if (!iframe) {  
            console.error('Iframe not found');  
            return;  
        }  

        if (iframe.requestFullscreen) {  
            iframe.requestFullscreen();  
        } else if (iframe.webkitRequestFullscreen) { /* Safari */  
            iframe.webkitRequestFullscreen();  
        } else if (iframe.msRequestFullscreen) { /* IE11 */  
            iframe.msRequestFullscreen();  
        } else if (iframe.mozRequestFullScreen) { /* Firefox */  
            iframe.mozRequestFullScreen();  
        }  
    } catch (error) {  
        console.error('Error entering fullscreen:', error);  
    }  
}  
</script>  
"""  

def process_html_file(file_path):  
    try:  
        # Read the HTML file  
        with open(file_path, 'r', encoding='utf-8') as file:  
            content = file.read()  

        # Parse HTML  
        soup = BeautifulSoup(content, 'html.parser')  

        # Find the iframe  
        iframe = soup.find('iframe')  
        if not iframe:  
            print(f"No iframe found in {file_path}")  
            return False  

        # Add required attributes to iframe  
        iframe['id'] = 'game-iframe'  
        iframe['allowfullscreen'] = ''  
        iframe['frameborder'] = '0'  
        iframe['width'] = '100%'  
        iframe['height'] = '100%'  
        iframe['scrolling'] = 'none'  

        # Create new game wrapper with the iframe  
        new_wrapper = BeautifulSoup(GAME_WRAPPER_TEMPLATE.format(  
            iframe_tag=str(iframe)  
        ), 'html.parser')  

        # Replace old iframe or wrapper with new one  
        old_wrapper = soup.find('section', {'class': 'game-wrapper'})  
        if old_wrapper:  
            old_wrapper.replace_with(new_wrapper)  
        else:  
            iframe.replace_with(new_wrapper)  

        # Add fullscreen script if not present  
        if 'openFullscreen' not in content:  
            body = soup.find('body')  
            if body:  
                script_tag = BeautifulSoup(FULLSCREEN_SCRIPT, 'html.parser')  
                body.append(script_tag)  

        # Save the modified HTML  
        with open(file_path, 'w', encoding='utf-8') as file:  
            file.write(str(soup))  

        print(f"Successfully updated {file_path}")  
        return True  

    except Exception as e:  
        print(f"Error processing {file_path}: {str(e)}")  
        return False  

def update_all_games(directory):  
    # Count statistics  
    total_files = 0  
    successful_updates = 0  
    failed_updates = 0  

    # Process all HTML files in the directory  
    for filename in os.listdir(directory):  
        if filename.endswith('.html'):  
            total_files += 1  
            file_path = os.path.join(directory, filename)  
            
            if process_html_file(file_path):  
                successful_updates += 1  
            else:  
                failed_updates += 1  

    # Print summary  
    print("\nUpdate Summary:")  
    print(f"Total HTML files processed: {total_files}")  
    print(f"Successfully updated: {successful_updates}")  
    print(f"Failed to update: {failed_updates}")  

if __name__ == "__main__":  
    # Get the directory containing HTML files  
    directory = input("Enter the directory path containing HTML files: ")  
    
    # Verify directory exists  
    if not os.path.exists(directory):  
        print("Directory does not exist!")  
    else:  
        # Create backup folder  
        backup_dir = os.path.join(directory, 'backup_before_update')  
        if not os.path.exists(backup_dir):  
            os.makedirs(backup_dir)  
            
        # Backup original files  
        print("Creating backups...")  
        for filename in os.listdir(directory):  
            if filename.endswith('.html'):  
                source = os.path.join(directory, filename)  
                dest = os.path.join(backup_dir, filename)  
                with open(source, 'r', encoding='utf-8') as src, open(dest, 'w', encoding='utf-8') as dst:  
                    dst.write(src.read())  
        
        # Run the update  
        print("Starting update process...")  
        update_all_games(directory)  