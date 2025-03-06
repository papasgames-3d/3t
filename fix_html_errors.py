import re
import os
import shutil

def backup_file(file_path):
    """Create a backup of the file before making changes."""
    backup_path = file_path + '.bak'
    shutil.copy2(file_path, backup_path)
    print(f"Created backup at {backup_path}")
    return backup_path

def fix_html_errors(file_path='index.html'):
    """Fix HTML errors in the index.html file."""
    # Create a backup first
    backup_file(file_path)
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix the improperly closed meta tags
    # Replace </meta></meta></meta> with proper structure
    fixed_content = re.sub(
        r'</meta></meta></meta><meta content="Lax" name="cookie-same-site"/><meta content="same-site" http-equiv="Cross-Origin-Resource-Policy"/><meta content="index, follow" name="robots"/></head>',
        r'<meta content="Lax" name="cookie-same-site"/>\n<meta content="same-site" http-equiv="Cross-Origin-Resource-Policy"/>\n<meta content="index, follow" name="robots"/>\n</head>',
        content
    )
    
    # Check if any replacements were made
    if fixed_content == content:
        print("No HTML errors found that match the expected pattern.")
        # Try to find and fix any similar patterns
        fixed_content = re.sub(
            r'</meta>\s*</meta>\s*</meta>',
            '',
            content
        )
        # Add proper spacing to meta tags
        fixed_content = re.sub(
            r'(<meta[^>]+/>)(<meta)',
            r'\1\n\2',
            fixed_content
        )
    
    # Write the fixed content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(fixed_content)
    
    print(f"Fixed HTML errors in {file_path}")
    print(f"HTML syntax has been fixed. The canonical tag remains unchanged as monkeymart.one is your domain.")

if __name__ == "__main__":
    fix_html_errors() 