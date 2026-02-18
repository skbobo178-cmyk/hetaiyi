# Git Branch Cleaner | Git 分支清理器

[English](README.md) | [中文](README.zh.md)

## 痛點 | Problem

Git 分支越積越多？
- 已合併到 main 的分支佔用空間
- `git branch -a` 列出一大串不知道要不要刪的分支
- 懶得一個一個確認、刪除

## 解決方案 | Solution

自動找出並刪除已合併到 main/master 的舊分支。

## 安裝 | Installation

```bash
git clone https://github.com/skbobo178-cmyk/hetaiyi.git
cd hetaiyi/helpers
```

## 使用方式 | Usage

### 預覽即將刪除的分支
```bash
python3 git_branch_cleaner.py
```

### 預覽（更謹慎版）- 只顯示 30 天前的分支
```bash
python3 git_branch_cleaner.py --dry-run
```

### 刪除合併過的分支
```bash
python3 git_branch_cleaner.py --delete
```

### 自訂天數（預設 30 天）
```bash
python3 git_branch_cleaner.py --days=7 --delete   # 7天前的
python3 git_branch_cleaner.py --days=90 --delete # 90天前的
```

## 參數說明 | Options

| 參數 | 說明 |
|------|------|
| `--delete` | 實際刪除分支（不加這選項只會預覽） |
| `--dry-run` | 預覽模式，不會刪除任何東西 |
| `--days=N` | 只顯示/刪除 N 天前合併的分支 |

## 範例 | Examples

```bash
# 預覽
$ python3 git_branch_cleaner.py

📋 Branches merged into main/master and older than 30 days:
  - feature/login-fix (45 days old)
  - hotfix/correct-typo (60 days old)
  - refactor/api-cleanup (90 days old)

💡 Run with --delete to remove these branches

# 刪除
$ python3 git_branch_cleaner.py --delete

🔍 Finding merged branches...

📋 Branches merged into main/master and older than 30 days:
  - feature/login-fix (45 days old)
  - hotfix/correct-typo (60 days old)

🗑️  Deleting 2 branches...
  ✅ Deleted: feature/login-fix
  ✅ Deleted: hotfix/correct-typo

✨ Done! Deleted 2 branches
```

## 運作原理 | How It Works

1. 找出已合併到 `main` 或 `master` 的分支
2. 檢查每個分支的最後提交日期
3. 篩選超過指定天數的分支
4. 顯示預覽或刪除

## 需求 | Requirements

- Python 3.6+
- Git CLI 已安裝
- 在 Git repository 目錄下執行

## 注意事項 | Notes

- 預設只顯示/刪除 **30 天前** 合併的分支（保護最近的和未合併的）
- 只會刪除 `git branch -d` (安全刪除)
- 不會刪除目前所在的分支

## License

MIT
