import os  
import shutil  

def restore_from_backup():  
    # Get the directory containing HTML files  
    directory = input("Enter the directory path containing HTML files: ")  
    
    # Verify directory exists  
    if not os.path.exists(directory):  
        print("Directory does not exist!")  
        return  
        
    backup_dir = os.path.join(directory, 'backup_before_update')  
    
    # Check if backup directory exists  
    if not os.path.exists(backup_dir):  
        print("Backup directory not found!")  
        return  
        
    # Restore files from backup  
    try:  
        print("Restoring files from backup...")  
        restored_count = 0  
        for filename in os.listdir(backup_dir):  
            if filename.endswith('.html'):  
                source = os.path.join(backup_dir, filename)  
                dest = os.path.join(directory, filename)  
                shutil.copy2(source, dest)  
                restored_count += 1  
                print(f"Restored: {filename}")  
        
        print(f"\nRestore complete! {restored_count} files restored.")  
        
    except Exception as e:  
        print(f"Error during restore: {str(e)}")  

if __name__ == "__main__":  
    restore_from_backup()  