# Text Diff Checker

Compare two texts and visualize differences with color-coded output.

## Problem

When comparing text or code, it's hard to see what changed. Terminal diff tools are complex, and online tools require copying/pasting.

## Solution

A simple Python script that compares two texts and shows differences with colors:

```bash
python3 text_diff.py "Hello World" "Hello Python"
```

Output shows additions (green), deletions (red), and similarity percentage.

## Installation

```bash
# Clone or download
git clone https://github.com/skbobo178-cmyk/hetaiyi.git
cd hetaiyi/helpers

# Optional: Install colorama for colored output
pip install colorama
```

## Usage

### Compare two strings
```bash
python3 text_diff.py "Hello World" "Hello Python"
```

### Compare files
```bash
python3 text_diff.py -f old_version.txt -f2 new_version.txt
```

### Interactive mode
```bash
python3 text_diff.py --interactive
```

### Simple diff with similarity
```bash
python3 text_diff.py -s "text1" "text2"
```

## Options

- `-f, --file1`: First file path
- `-f2, --file2`: Second file path  
- `-i, --interactive`: Interactive input mode
- `-s, --simple`: Simple diff with similarity percentage
- `-c, --context`: Context diff format
- `-u, --unified`: Unified diff format (default)

## Requirements

- Python 3.6+
- colorama (optional, for colored output)

## Example Output

```
============================================================
TEXT DIFFERENCES
============================================================
- Hello World
+ Hello Python

============================================================
Similarity: 57.1%
============================================================
```

## 中文 (Chinese)

[中文版](README.zh.md)

文本差异比较工具 - 比较两个文本并以颜色显示差异。
