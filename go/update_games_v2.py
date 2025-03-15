import os  
from bs4 import BeautifulSoup  
import re  

def process_html_file(file_path):  
    try:  
        # Read the HTML file  
        with open(file_path, 'r', encoding='utf-8') as file:  
            content = file.read()  

        # Parse HTML  
        soup = BeautifulSoup(content, 'html.parser')  

        # Find all iframes and update them  
        iframes = soup.find_all('iframe')  
        for iframe in iframes:  
            # Add required attributes to iframe  
            iframe['id'] = 'game-iframe'  
            iframe['allowfullscreen'] = ''  
            iframe['frameborder'] = '0'  
            iframe['width'] = '100%'  
            iframe['height'] = '100%'  
            iframe['scrolling'] = 'none'  

        # Remove any existing fullscreen scripts  
        for script in soup.find_all('script'):  
            if 'openFullscreen' in str(script):  
                script.decompose()  

        # Add our new fullscreen script at the end of body  
        new_script = soup.new_tag('script')  
        new_script.string = """  
        function openFullscreen() {  
            try {  
                const iframe = document.getElementById('game-iframe');  
                if (!iframe) {  
                    console.error('Iframe not found');  
                    return;  
                }  
                
                if (document.fullscreenElement) {  
                    document.exitFullscreen();  
                } else {  
                    if (iframe.requestFullscreen) {  
                        iframe.requestFullscreen();  
                    } else if (iframe.webkitRequestFullscreen) {  
                        iframe.webkitRequestFullscreen();  
                    } else if (iframe.msRequestFullscreen) {  
                        iframe.msRequestFullscreen();  
                    } else if (iframe.mozRequestFullScreen) {  
                        iframe.mozRequestFullScreen();  
                    }  
                }  
            } catch (error) {  
                console.error('Error toggling fullscreen:', error);  
            }  
        }  
        """  
        
        # Find body tag and append script  
        body = soup.find('body')  
        if body:  
            body.append(new_script)  

        # Update the fullscreen button  
        fullscreen_btn = soup.find('a', {'id': 'fullscreen-btn'})  
        if fullscreen_btn:  
            fullscreen_btn['href'] = 'javascript:void(0);'  
            fullscreen_btn['onclick'] = 'openFullscreen()'  

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