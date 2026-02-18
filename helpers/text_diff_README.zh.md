# 文本差异比较工具

比较两个文本并以颜色显示差异。

## 问题

比较文本或代码时，很难看出有什么变化。终端的 diff 工具很复杂，在线工具需要复制粘贴。

## 解决方案

一个简单的 Python 脚本，比较两个文本并以颜色显示差异：

```bash
python3 text_diff.py "你好世界" "你好Python"
```

输出显示添加（绿色）、删除（红色）和相似度百分比。

## 安装

```bash
# 克隆或下载
git clone https://github.com/skbobo178-cmyk/hetaiyi.git
cd hetaiyi/helpers

# 可选：安装 colorama 以获得彩色输出
pip install colorama
```

## 使用方法

### 比较两个字符串
```bash
python3 text_diff.py "你好世界" "你好Python"
```

### 比较文件
```bash
python3 text_diff.py -f 旧版本.txt -f2 新版本.txt
```

### 交互模式
```bash
python3 text_diff.py --interactive
```

### 简单差异显示相似度
```bash
python3 text_diff.py -s "文本1" "文本2"
```

## 选项

- `-f, --file1`: 第一个文件路径
- `-f2, --file2`: 第二个文件路径
- `-i, --interactive`: 交互式输入模式
- `-s, --simple`: 简单差异显示相似度百分比
- `-c, --context`: 上下文差异格式
- `-u, --unified`: 统一差异格式（默认）

## 要求

- Python 3.6+
- colorama（可选，用于彩色输出）

## 示例输出

```
============================================================
TEXT DIFFERENCES
============================================================
- 你好世界
+ 你好Python

============================================================
相似度: 57.1%
============================================================
```

## English

[English version](text_diff_README.md)

文本差异比较工具 - 比较两个文本并以颜色显示差异。
