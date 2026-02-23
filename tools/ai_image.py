#!/usr/bin/env python3
"""
AI Image Generator - Qwen + JiMeng
簡單易用的 AI 圖片生成工具

使用方式:
  export DASHSCOPE_API_KEY="your-key-here"
  export VOLC_ACCESS_KEY="your-key-here"
  export VOLC_SECRET_KEY="your-secret-here"
  python ai_image.py "A cute cat"
"""

import json
import urllib.request
import urllib.parse
import ssl
import sys
import os

# API 配置 - 請設置環境變量
# export DASHSCOPE_API_KEY="your-key"
# export VOLC_ACCESS_KEY="your-key"  
# export VOLC_SECRET_KEY="your-secret"

DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY', '')
VOLC_ACCESS_KEY = os.environ.get('VOLC_ACCESS_KEY', '')
VOLC_SECRET_KEY = os.environ.get('VOLC_SECRET_KEY', '')

def generate_qwen(prompt, size='1024*1024'):
    """使用阿里雲 Qwen 生成圖片"""
    if not DASHSCOPE_API_KEY:
        raise Exception("請設置 DASHSCOPE_API_KEY 環境變量")
    
    url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'
    
    data = {
        'model': 'qwen-image-plus',
        'input': {'prompt': prompt},
        'parameters': {'size': size}
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DASHSCOPE_API_KEY}',
            'X-DashScope-Async': 'disable'
        },
        method='POST'
    )
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    with urllib.request.urlopen(req, context=ctx) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        if 'output' in result and 'image_url' in result['output']:
            return result['output']['image_url']
        elif 'code' in result:
            raise Exception(f"API Error: {result.get('message', result['code'])}")
        else:
            raise Exception("Unknown error")

def generate_jimeng(prompt, image_size='1024x1024'):
    """使用火山引擎 JiMeng 生成圖片"""
    if not VOLC_ACCESS_KEY or not VOLC_SECRET_KEY:
        raise Exception("請設置 VOLC_ACCESS_KEY 和 VOLC_SECRET_KEY 環境變量")
    
    from volcengine.visual.VisualService import VisualService
    
    visual_service = VisualService()
    visual_service.set_ak(VOLC_ACCESS_KEY)
    visual_service.set_sk(VOLC_SECRET_KEY)
    
    form = {
        'req_key': 'jimeng_t2i_v40',
        'prompt': prompt,
        'image_size': image_size
    }
    
    resp = visual_service.cv_json_api('CVSync2AsyncSubmitTask', form)
    
    if resp.get('code') == 0:
        return resp
    else:
        raise Exception(f"API Error: {resp.get('message', 'Unknown')}")

def download_image(url, filename='output.png'):
    """下載圖片"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    with urllib.request.urlopen(url, context=ctx) as response:
        with open(filename, 'wb') as f:
            f.write(response.read())
    return filename

def main():
    if len(sys.argv) < 2:
        print("用法: python ai_image.py <prompt> [size]")
        print("例如: python ai_image.py 'A cute cat' 1024*1024")
        print("\n請先設置環境變量:")
        print("  export DASHSCOPE_API_KEY='your-key'")
        print("  export VOLC_ACCESS_KEY='your-key'")
        print("  export VOLC_SECRET_KEY='your-secret'")
        sys.exit(1)
    
    prompt = sys.argv[1]
    size = sys.argv[2] if len(sys.argv) > 2 else '1024*1024'
    
    print(f"🎨 正在生成圖片...")
    print(f"   描述: {prompt}")
    print(f"   尺寸: {size}")
    
    try:
        # 嘗試 Qwen
        print("\n使用 Qwen Image Plus...")
        image_url = generate_qwen(prompt, size)
        filename = download_image(image_url, 'ai_output.png')
        print(f"\n✅ 成功！圖片已保存: {filename}")
        print(f"   URL: {image_url}")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == '__main__':
    main()
