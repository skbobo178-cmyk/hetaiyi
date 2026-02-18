# URL Cleaner | 網址追蹤清除器

[English](README.md) | [中文](README.zh.md)

## 痛點 | Problem

每次從網站複製網址時，都會帶上一堆追蹤參數：

```
https://amazon.com/product?utm_source=twitter&gclid=abc123&fbclid=xyz789&utm_medium=social
```

這些 `utm_`, `gclid`, `fbclid` 等參數：
- 長達 50+ 字元
- 追蹤用戶行為
- 讓網址看起來很醜
- 影響網址分享

## 解決方案 | Solution

移除 URL 中的追蹤參數，只保留乾淨的網址。

## 安裝 | Installation

```bash
# Clone repo
git clone https://github.com/skbobo178-cmyk/hetaiyi.git
cd hetaiyi/helpers

# 直接執行
python3 url_cleaner.py "https://example.com?utm_source=twitter"
```

## 使用方式 | Usage

### 命令列輸入
```bash
python3 url_cleaner.py "https://amazon.com/product?utm_source=twitter&gclid=abc"
# 輸出: https://amazon.com/product
```

### 從剪貼簿讀取
```bash
python3 url_cleaner.py --clipboard
```

### 處理檔案
```bash
python3 url_cleaner.py -f urls.txt
python3 url_cleaner.py -f urls.txt -o clean_urls.txt
```

### 輸出到剪貼簿
```bash
python3 url_cleaner.py "https://example.com?utm_source=twitter" -o
```

## 支援的參數 | Supported Parameters

移除 30+ 追蹤參數：
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`
- `gclid` (Google)
- `fbclid` (Facebook)
- `tcclid` (TikTok)
- `msclkid` (Microsoft)
- `irclid` (Instagram)
- `mc_cid`, `mc_eid` (Mailchimp)
- `_ga`, `_gl` (Google Analytics)
- 還有更多...

## 範例 | Examples

```bash
# 基本用法
$ python3 url_cleaner.py "https://shop.google.com/product?utm_source=newsletter"
https://shop.google.com/product

# 多個參數
$ python3 url_cleaner.py "https://youtube.com/watch?v=abc123&utm_source=share&fbclid=xyz"
https://youtube.com/watch?v=abc123

# 批次處理
$ python3 url_cleaner.py -f urls.txt
```

## 需求 | Requirements

- Python 3.7+
- 無需額外依賴 (標準庫)

## License

MIT
