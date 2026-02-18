# helpers/

Useful scripts that solve everyday problems.

[English](README.md) | [中文](README.zh.md)

---

## Scripts

### screenshot_organizer.py
Auto-organize screenshots by date.

## Usage | 使用方式

```bash
# Clone the repo
git clone https://github.com/skbobo178-cmyk/hetaiyi.git
cd hetaiyi/helpers

# Run the script
python3 screenshot_organizer.py

# Or with custom paths
python3 screenshot_organizer.py -i ~/Desktop -o ~/Pictures/Screenshots
```

## Options

| Flag | Description | 說明 |
|------|-------------|------|
| `-i, --input` | Input folder (default: ~/Desktop) | 輸入資料夾 |
| `-o, --output` | Output folder (default: ~/Pictures/Screenshots) | 輸出資料夾 |
