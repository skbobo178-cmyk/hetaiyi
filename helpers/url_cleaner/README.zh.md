# URL Cleaner | 網址追蹤清除器

[English](README.md) | [中文](README.zh.md)

## 痛點

每次從網站（Amazon、YouTube、Google 等）複製網址時，都會帶上一堆追蹤參數。

例如：
```
https://amazon.com/product?utm_source=twitter&gclid=abc123&fbclid=xyz789&utm_medium=social
```

這些 `utm_`, `gclid`, `fbclid` 等參數：
- 長達 50+ 字元，非常冗長
- 用於追蹤用戶從哪個管道來
- 讓乾淨的網址變得又長又醜
- 有些參數還會過期

## 解決方案

自動移除 URL 中的追蹤參數，還原乾淨的網址。

## 安裝

```bash
# Clone 專案
git clone https://github.com/skbobo178-cmyk/hetaiyi.git
cd hetaiyi/helpers

# 直接執行
python3 url_cleaner.py "https://example.com?utm_source=twitter"
```

## 使用方式

### 命令列輸入
```bash
python3 url_cleaner.py "https://amazon.com/product?utm_source=twitter&gclid=abc"
# 輸出: https://amazon.com/product
```

### 從剪貼簿讀取（Mac）
```bash
python3 url_cleaner.py --clipboard
```

### 處理檔案
```bash
# 輸入檔案
python3 url_cleaner.py -f urls.txt

# 輸出到新檔案
python3 url_cleaner.py -f urls.txt -o clean_urls.txt
```

### 輸出到剪貼簿
```bash
python3 url_cleaner.py "https://example.com?utm_source=twitter" -o
```

## 支援的參數

移除 30+ 種追蹤參數：

| 參數 | 來源 |
|------|------|
| utm_source, utm_medium, utm_campaign, utm_term, utm_content | Google Analytics |
| gclid | Google Ads |
| fbclid | Facebook |
| tcclid | TikTok |
| msclkid | Microsoft |
| irclid | Instagram |
| mc_cid, mc_eid | Mailchimp |
| _ga, _gl | Google Analytics |
| ref, ref_ | 各種網站 |

## 範例

```bash
# 基本用法
$ python3 url_cleaner.py "https://shop.google.com/product?utm_source=newsletter"
https://shop.google.com/product

# 多個參數
$ python3 url_cleaner.py "https://youtube.com/watch?v=abc123&utm_source=share&fbclid=xyz"
https://youtube.com/watch?v=abc123

# 批次處理
$ python3 url_cleaner.py -f urls.txt
Processing 3 URLs...
https://amazon.com/product → https://amazon.com/product
https://youtube.com/watch?v=xyz → https://youtube.com/watch?v=xyz
https://example.com?utm_source=twitter → https://example.com
```

## 常見問題

### Q: 會不會不小心移除重要的參數？
A: 不會。本工具只移除已知的追蹤參數，不會影響網址的正常功能。

### Q: 需要安裝額外的 Python 套件嗎？
A: 不需要。只需 Python 3.7+，使用標準庫。

### Q: 支援中文網址嗎？
A: 支援。工具會自動處理 URL 編碼。

## 需求

- Python 3.7 或更高版本
- 無需額外依賴

## License

MIT
