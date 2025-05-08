# Modern Template System

This readme explains the templating system created to update the design of all game pages.

## Overview

The system consists of a modern interface template (index3.html) and several PowerShell scripts to apply this template to all game HTML files while preserving the unique content of each game page.

## Files

- **index3.html** - The modern interface template with a cleaner design, responsive layout, and game sidebar
- **modern-style.css** - External CSS file for the modern design
- **apply-template.ps1** - Script to apply the template to all game HTML files
- **backup-games.ps1** - Script to create a complete backup before making changes
- **restore-backup.ps1** - Script to restore from a complete backup directory
- **restore-from-backups.ps1** - Script to restore from individual .backup files

## Usage Instructions

### Before Making Any Changes

Always create a backup first:

```powershell
.\backup-games.ps1
```

This will create a timestamped backup directory (e.g., backup_20250508_144444) containing all your game files.

### Testing with a Single File

To test the template on a single game file:

1. Manually apply the template to a single file (as we did with 1v1-lol-offline.html)
2. Check if it works correctly in the browser

### Applying to All Files

Once you're satisfied with the test, apply the template to all files:

```powershell
.\apply-template.ps1
```

This script will:
1. Create .backup files for each HTML file in the game directory
2. Extract important information from each file (title, iframe source, etc.)
3. Apply the new template while preserving that content

### Restoring from Backup

If something goes wrong, you can restore:

1. From a complete backup directory:
```powershell
.\restore-backup.ps1
```

2. From individual .backup files:
```powershell
.\restore-from-backups.ps1
```

## Template Features

- Responsive design that works on mobile and desktop
- Cleaner, more modern flat design
- Game recommendations sidebar with 12 games
- Perfectly square game images (using aspect-ratio: 1/1)
- Improved typography and spacing
- External CSS for easier maintenance

## Customization

To modify the template, edit:

- **modern-style.css** for styling changes
- **apply-template.ps1** for layout/content structure changes
- **index3.html** for reference 