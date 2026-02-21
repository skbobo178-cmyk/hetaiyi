# Troubleshooting Guide

This guide helps you resolve common issues with Hunter AI Content Factory.

## Installation Issues

### Python not found

**Problem**: `python: command not found`

**Solution**: 
- The `run.sh`/`run.bat` script will automatically download Python
- Or install Python 3.12+ manually from https://python.org

### uv not found

**Problem**: `uv: command not found`

**Solution**:
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### Dependency installation fails

**Problem**: `pip install -r requirements.txt` fails

**Solution**:
```bash
# Try using uv instead
uv sync

# Or create a virtual environment first
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## API Configuration Issues

### Gemini API Key invalid

**Problem**: `Error: API key not valid` or `401 Unauthorized`

**Solution**:
1. Get a new API key from https://aistudio.google.com/apikey
2. Make sure the key has Gemini API access
3. Update `config.yaml` with the new key

### Gemini quota exceeded

**Problem**: `Error: Quota exceeded` or `429 Too Many Requests`

**Solution**:
- Wait for quota to reset (usually daily)
- Use Gemini 2.0 Flash (has higher quota than Pro)
- Check Google AI Studio for quota details

## Data Collection Issues

### GitHub API returns 403

**Problem**: Cannot fetch GitHub trending

**Solution**:
1. Create a GitHub Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Generate new token (classic)
   - Select `repo` scope
2. Add to `config.yaml`:
```yaml
github:
  token: "ghp_your_token_here"
```

### Twitter/X采集失败

**Problem**: Cannot fetch Twitter data

**Solution**:
1. Update Twitter cookies:
   - Open Twitter in browser
   - Press F12 → Application → Cookies
   - Copy cookies to `data/cookies.json`
2. Or use browser automation mode

### 小红书采集失败

**Problem**: Cannot fetch Xiaohongshu data

**Solution**:
1. Get Xiaohongshu cookies from browser
2. Add to `config.yaml`:
```yaml
xiaohongshu:
  cookies: "your-cookies-string"
```

### Reddit/HackerNews not working

**Problem**: Cannot fetch from these platforms

**Solution**:
- These usually don't require authentication
- Check your internet connection
- Try again later if rate limited

## Content Generation Issues

### AI output is too generic

**Problem**: Generated content feels "AI-like" and lacks personality

**Solution**:
- Adjust the tone in `config.yaml`:
```yaml
account:
  tone: "更口语化、更有观点"
```
- Use the "de-AI" feature in the template settings

### Content is duplicated

**Problem**: Similar content being generated

**Solution**:
- The system uses ChromaDB for semantic deduplication
- Clear the vector database: `rm -rf data/chroma/`
- Adjust similarity threshold in config

### Generation takes too long

**Problem**: Content generation is slow

**Solution**:
- Use `gemini-2.0-flash` model (faster than Pro)
- Reduce the number of sources to scan
- Use `--dry-run` to test quickly

## Publishing Issues

### PushPlus notification not received

**Problem**: WeChat notification not coming through

**Solution**:
1. Check config:
```yaml
pushplus:
  token: "your-token"
  enabled: true
```
2. Get token from http://www.pushplus.plus
3. Scan QR code to bind WeChat
4. Ensure "PushPlus 推送加"公众号 is followed

### 公众号没有收到文章

**Problem**: Articles not appearing in WeChat Official Account

**Explanation**: 
- PushPlus sends to **personal WeChat chat**, not WeChat Official Account
- Check: WeChat → "PushPlus 推送加"公众号 → Chat window

**Solution**:
1. Copy generated article from `output/` directory
2. Manually publish to your WeChat Official Account
3. Or set up WeChat Official Account API integration

## Performance Issues

### High memory usage

**Problem**: System running out of memory

**Solution**:
- Close other applications
- Reduce batch size in config
- Use smaller models (gemini-2.0-flash instead of pro)

### Disk space full

**Problem**: No space left on device

**Solution**:
```bash
# Clear old outputs
rm -rf output/*

# Clear cache
rm -rf data/cache/*
rm -rf data/chroma/*
```

## Getting Help

If you still have issues:

1. Check existing GitHub Issues: https://github.com/Pangu-Immortal/hunter-ai-content-factory/issues
2. Join QQ group: 794834282
3. Create a new Issue with:
   - Error message
   - Config (remove sensitive info)
   - Steps to reproduce
   - System info (OS, Python version)
