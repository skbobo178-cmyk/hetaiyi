#!/usr/bin/env python3
"""
File Organizer - Automatically organizes files by type
Usage: python3 file_organizer.py [directory]
"""

import os
import sys
from pathlib import Path

# File type mappings
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.c', '.cpp', '.go', '.rs', '.ts'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'Data': ['.json', '.xml', '.csv', '.yaml', '.yml', '.sql'],
}

def get_category(ext):
    """Get category for a file extension"""
    ext = ext.lower()
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return 'Others'

def organize_files(directory):
    """Organize files in directory by type"""
    directory = Path(directory)
    
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist")
        return
    
    # Counters
    moved = 0
    errors = 0
    
    for item in directory.iterdir():
        if item.is_file():
            ext = item.suffix
            category = get_category(ext)
            
            # Create category folder
            category_dir = directory / category
            category_dir.mkdir(exist_ok=True)
            
            # Move file
            try:
                new_path = category_dir / item.name
                # Handle name conflicts
                if new_path.exists():
                    base = item.stem
                    counter = 1
                    while new_path.exists():
                        new_path = category_dir / f"{base}_{counter}{ext}"
                        counter += 1
                
                item.rename(new_path)
                print(f"✓ {item.name} → {category}/")
                moved += 1
            except Exception as e:
                print(f"✗ Error moving {item.name}: {e}")
                errors += 1
    
    print(f"\n✅ Done! Moved {moved} files" + (f", {errors} errors" if errors else ""))

if __name__ == '__main__':
    target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    organize_files(target_dir)
