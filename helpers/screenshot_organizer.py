#!/usr/bin/env python3
"""
Screenshot Organizer - 自動整理截圖
按日期分類移動截圖到資料夾
"""

import os
import shutil
from datetime import datetime
from pathlib import Path


def organize_screenshots(screenshots_dir: str, output_dir: str):
    """
    將截圖按日期整理到不同資料夾
    
    Args:
        screenshots_dir: 截圖所在資料夾 (e.g., ~/Desktop)
        output_dir: 輸出資料夾 (e.g., ~/Pictures/Screenshots)
    """
    screenshots_path = Path(screenshots_dir).expanduser()
    output_path = Path(output_dir).expanduser()
    
    # 支援的圖片格式
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    
    # 常見截圖檔名模式
    screenshot_patterns = ['screenshot', 'screen shot', '截圖', 'capture', 'snip', 'shot']
    
    organized_count = 0
    
    for file in screenshots_path.iterdir():
        if file.is_file():
            # 檢查副檔名
            if file.suffix.lower() not in image_extensions:
                continue
            
            # 檢查是否為截圖（檔名包含相關關鍵詞或 modification time）
            filename_lower = file.name.lower()
            is_screenshot = any(pattern in filename_lower for pattern in screenshot_patterns)
            
            # 也檢查檔案修改時間（今天的也當作截圖）
            if not is_screenshot:
                # 嘗試獲取檔案時間
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                if mtime.date() == datetime.now().date():
                    is_screenshot = True
            
            if is_screenshot:
                # 獲取日期
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                date_folder = mtime.strftime("%Y-%m-%d")
                
                # 建立日期資料夾
                target_folder = output_path / date_folder
                target_folder.mkdir(parents=True, exist_ok=True)
                
                # 移動檔案
                target_path = target_folder / file.name
                shutil.move(str(file), str(target_path))
                
                print(f"📁 {file.name} → {date_folder}/")
                organized_count += 1
    
    print(f"\n✅ 完成！已整理 {organized_count} 個檔案")
    return organized_count


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="自動整理截圖")
    parser.add_argument("--input", "-i", default="~/Desktop", help="截圖資料夾")
    parser.add_argument("--output", "-o", default="~/Pictures/Screenshots", help="輸出資料夾")
    
    args = parser.parse_args()
    
    organize_screenshots(args.input, args.output)
