# helpers/

解決日常問題的實用腳本。

[English](README.md) | [中文](README.zh.md)

---

## 腳本

### screenshot_organizer.py
自動按日期整理截圖。

## 使用方式 | Usage

```bash
# 複製專案
git clone https://github.com/skbobo178-cmyk/hetaiyi.git
cd hetaiyi/helpers

# 執行腳本
python3 screenshot_organizer.py

# 自訂路徑
python3 screenshot_organizer.py -i ~/Desktop -o ~/Pictures/Screenshots
```

## 選項 | Options

| 參數 | 說明 | Description |
|------|------|-------------|
| `-i, --input` | 輸入資料夾 (預設: ~/Desktop) | Input folder |
| `-o, --output` | 輸出資料夾 (預設: ~/Pictures/Screenshots) | Output folder |
