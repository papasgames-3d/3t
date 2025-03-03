#!/bin/bash

# This script removes the Play Now button and playGame() function from all HTML files in the go directory
# It directly embeds the iframe in each game page

echo "Removing Play Now buttons from all game pages..."

# Find all HTML files in the go directory
find go -name "*.html" | while read file; do
  echo "Processing $file..."
  
  # Get the game URL from the data-url attribute
  game_url=$(grep -o 'data-url="[^"]*"' "$file" | head -1 | cut -d'"' -f2)
  
  # Get the game title
  game_title=$(grep -o '<h1 class="section-title">[^<]*</h1>' "$file" | head -1 | sed 's/<h1 class="section-title">\(.*\)<\/h1>/\1/')
  
  if [ -z "$game_url" ]; then
    echo "Warning: No game URL found in $file, skipping..."
    continue
  fi
  
  echo "Game URL: $game_url"
  echo "Game Title: $game_title"
  
  # Remove the talpa-splash-container and replace it with an iframe
  sed -i '/<div class="talpa-splash-container/,/<\/div><\/div><\/div>/c\
\t\t\t\t\t\t<iframe title="'"$game_title"'" src="'"$game_url"'" allowfullscreen frameborder="0" width="100%" height="100%" scrolling="none"></iframe>' "$file"
  
  # Remove the playGame() function
  sed -i '/function playGame()/,/}/d' "$file"
  
  echo "Updated $file"
done

echo "All files have been updated!" 