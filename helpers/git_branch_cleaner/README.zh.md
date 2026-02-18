# Git Branch Cleaner | Git 分支清理器

[English](README.md) | [中文](README.zh.md)

## 痛點

Git 分支越積越多？

執行 `git branch -a` 看到一堆不知道還在不在用的分支：
- 已合併到 main 的舊分支
- 功能完成但忘記刪除的分支
- 實驗性質但早就放棄的分支

懶得一個一個確認、刪除，但又不想亂刪怕出問題。

## 解決方案

自動找出並刪除已合併到 main/master 的舊分支。

保護原則：
- 只刪除 **已合併** 的分支
- 只刪除 **30 天前** 合併的分支
- 使用安全刪除 `-d`（不會 force delete）

## 安裝

```bash
git clone https://github.com/skbobo178-cmyk/hetaiyi.git
cd hetaiyi/helpers
```

## 使用方式

### 預覽（推薦先執行）
```bash
python3 git_branch_cleaner.py
```

### 預覽（更謹慎，只看舊的）
```bash
python3 git_branch_cleaner.py --dry-run
```

### 實際刪除
```bash
python3 git_branch_cleaner.py --delete
```

### 自訂天數
```bash
python3 git_branch_cleaner.py --days=7 --delete   # 7天前合併的
python3 git_branch_cleaner.py --days=90 --delete  # 90天前合併的
```

## 參數說明

| 參數 | 說明 | 範例 |
|------|------|------|
| `--delete` | 實際刪除分支（不加只會預覽） | `--delete` |
| `--dry-run` | 預覽模式，不會刪除任何東西 | `--dry-run` |
| `--days=N` | 只顯示 N 天前合併的分支 | `--days=7` |

## 範例

### 預覽輸出
```
$ python3 git_branch_cleaner.py

🔍 Finding merged branches...

📋 Branches merged into main/master and older than 30 days:
  - feature/login-fix (45 天前)
  - hotfix/correct-typo (60 天前)
  - refactor/api-cleanup (90 天前)

💡 Run with --delete to remove these branches
```

### 刪除輸出
```
$ python3 git_branch_cleaner.py --delete

🔍 Finding merged branches...

📋 Branches merged into main/master and older than 30 days:
  - feature/login-fix (45 天前)
  - hotfix/correct-typo (60 天前)

🗑️  Deleting 2 branches...
  ✅ 已刪除: feature/login-fix
  ✅ 已刪除: hotfix/correct-typo

✨ 完成！已刪除 2 個分支
```

## 運作原理

1. 執行 `git branch --merged` 找出已合併的分支
2. 檢查每個分支的最後提交日期
3. 篩選超過指定天數的分支
4. 預覽顯示或執行刪除

## 常見問題

### Q: 會不會誤刪未合併的分支？
A: 不會。本工具只會顯示/刪除已合併到 main 或 master 的分支。

### Q: 為什麼預設是 30 天？
A: 30 天是安全緩衝期，確保你還有機會反悔。如果立馬要刪，可以用 `--days=0`。

### Q: 可以刪除 remote 分支嗎？
A: 目前只支援刪除 local 分支。

## 需求

- Python 3.6 或更高版本
- Git CLI 已安裝
- 在 Git repository 目錄下執行

## License

MIT
