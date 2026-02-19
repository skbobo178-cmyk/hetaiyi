#!/usr/bin/env python3
"""
Screenshot Organizer - Auto-renames and organizes screenshots
Usage: python3 screenshot_organizer.py [directory]
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def organize_screenshots(directory='.'):
    """Organize screenshots by date and app"""
    directory = Path(directory)
    
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist")
        return
    
    # Screenshots usually have these patterns
    patterns = ['Screenshot', 'Screen Shot', 'screenshot', '截圖']
    
    count = 0
    for item in directory.iterdir():
        if item.is_file():
            name = item.name
            
            # Check if it's a screenshot
            if any(p in name for p in patterns):
                # Extract date from filename
                # Format: Screenshot 2026-02-19 at 10.04.05 AM.png
                try:
                    # Try to parse the date
                    parts = name.split()
                    if 'at' in parts:
                        date_part = parts[1] + ' ' + parts[2] + ' ' + parts[3]
                        dt = datetime.strptime(date_part, '%Y-%m-%d %H.%M.%S %p')
                        
                        # Create folder by date
                        folder = directory / f"Screenshots_{dt.strftime('%Y-%m')}"
                        folder.mkdir(exist_ok=True)
                        
                        # New name with date prefix
                        new_name = f"{dt.strftime('%Y%m%d_%H%M%S')}_{item.name}"
                        new_path = folder / new_name
                        
                        item.rename(new_path)
                        print(f"✓ {item.name} → {folder.name}/{new_name}")
                        count += 1
                except Exception as e:
                    # Just move to unsorted
                    folder = directory / "Screenshots_Unsorted"
                    folder.mkdir(exist_ok=True)
                    new_path = folder / item.name
                    item.rename(new_path)
                    print(f"? {item.name} → {folder.name}/ (unsorted)")
    
    print(f"\n✅ Done! Organized {count} screenshots")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    organize_screenshots(target)
