# Getting Started Guide

This guide will walk you through setting up and running the Hunter AI Content Factory.

## Prerequisites

- Python 3.12 or higher
- Gemini API Key (get it from [Google AI Studio](https://aistudio.google.com/apikey))
- Optional: GitHub Token, Twitter Cookies, Xiaohongshu Cookies, PushPlus Token

## Installation

### Option 1: Quick Start (Recommended for Beginners)

```bash
# Clone the repository
git clone https://github.com/Pangu-Immortal/hunter-ai-content-factory.git
cd hunter-ai-content-factory

# Run the setup script (auto-installs Python + dependencies)
# Mac/Linux
bash run.sh

# Windows
run.bat
```

### Option 2: Manual Setup

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

## Configuration

### Step 1: Copy the config file

```bash
cp config.example.yaml config.yaml
```

### Step 2: Edit config.yaml

Add your Gemini API Key:

```yaml
gemini:
  api_key: "your-gemini-api-key-here"
  model: "gemini-2.0-flash"
```

### Step 3: (Optional) Add more configurations

For full features, add:

```yaml
# GitHub - for trending projects
github:
  token: "ghp_your_token"

# Twitter - for real-time trends
twitter:
  cookies_path: "data/cookies.json"

# Xiaohongshu - for lifestyle content
xiaohongshu:
  cookies: "your-cookies"

# PushPlus - for notifications
pushplus:
  token: "your-token"
  enabled: true
```

## Running the Application

### Web UI Mode (Recommended)

```bash
uv run python app.py
```

Then open your browser to `http://localhost:7860`

### CLI Mode

```bash
# GitHub trending → Article
uv run hunter run -t github

# Pain point analysis
uv run hunter run -t pain

# News aggregation
uv run hunter run -t news

# Xiaohongshu content
uv run hunter run -t xhs

# Auto mode (all platforms)
uv run hunter run -t auto

# Dry run (test without publishing)
uv run hunter run --dry-run
```

## Content Templates

| Template | Data Source | Output | Best For |
|----------|-------------|--------|----------|
| `github` | GitHub Trending | Long-form article | Tech bloggers |
| `pain` | Twitter + Reddit | Diagnosis report | Product managers |
| `news` | 5 platforms | News digest | Tech media |
| `xhs` | Xiaohongshu | Lifestyle article | Lifestyle bloggers |
| `auto` | All platforms | AI life hacks | Content creators |

## Troubleshooting

### Common Issues

1. **GitHub API returns 403**
   - Solution: Add GitHub token to increase rate limit (60→5000 requests/hour)

2. **Twitter/X采集失败**
   - Solution: Update cookies in `data/cookies.json`

3. **PushPlus notification not received**
   - Solution: Check token in config.yaml, ensure `enabled: true`

4. **公众号没有收到文章**
   - Note: PushPlus sends to personal WeChat, not WeChat Official Account: We
   - CheckChat → "PushPlus 推送加"公众号 → 聊天窗口
   - Manual publish: Copy from `output/` directory

## Next Steps

- Read [Workflow Guide](workflow_guide.md) to understand the 6-step content generation process
- Check [Style Guide](style_guide.md) for content quality standards
- Join our QQ group: 794834282 for support

## Support

- GitHub Issues: Report bugs and feature requests
- QQ Group: 794834282
- Star us on GitHub: https://github.com/Pangu-Immortal/hunter-ai-content-factory
