// AI Image Generation API Server
// 支援 Qwen (阿里雲) 和 JiMeng (火山引擎) 圖片生成
// 
// 請設置環境變量:
//   export DASHSCOPE_API_KEY="your-key"
//   export VOLC_ACCESS_KEY="your-key"
//   export VOLC_SECRET_KEY="your-secret"

const express = require('express');
const cors = require('cors');
const https = require('https');
const http = require('http');

const app = express();
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// API Keys 配置 - 從環境變量讀取
const CONFIG = {
    dashscope: {
        apiKey: process.env.DASHSCOPE_API_KEY || '',
        baseUrl: 'https://dashscope.aliyuncs.com'
    },
    volcengine: {
        accessKey: process.env.VOLC_ACCESS_KEY || '',
        secretKey: process.env.VOLC_SECRET_KEY || '',
        endpoint: 'https://visual.volcengineapi.com'
    }
};

// Qwen 圖片生成
async function generateWithQwen(prompt, size = '1024*1024') {
    if (!CONFIG.dashscope.apiKey) {
        throw new Error('請設置 DASHSCOPE_API_KEY 環境變量');
    }
    
    return new Promise((resolve, reject) => {
        const data = JSON.stringify({
            model: 'qwen-image-plus',
            input: { prompt },
            parameters: { size }
        });
        
        const options = {
            hostname: 'dashscope.aliyuncs.com',
            path: '/api/v1/services/aigc/multimodal-generation/generation',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${CONFIG.dashscope.apiKey}`,
                'X-DashScope-Async': 'disable'
            }
        };
        
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    const result = JSON.parse(body);
                    if (result.output && result.output.image_url) {
                        resolve({ success: true, imageUrl: result.output.image_url });
                    } else if (result.code) {
                        reject(new Error(result.message || 'Qwen API Error'));
                    } else {
                        reject(new Error('Unknown error from Qwen'));
                    }
                } catch (e) {
                    reject(e);
                }
            });
        });
        
        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

// JiMeng 圖片生成
async function generateWithJiMeng(prompt, imageSize = '1024x1024') {
    if (!CONFIG.volcengine.accessKey || !CONFIG.volcengine.secretKey) {
        throw new Error('請設置 VOLC_ACCESS_KEY 和 VOLC_SECRET_KEY 環境變量');
    }
    
    const timestamp = new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
    
    const form = {
        req_key: 'jimeng_t2i_v40',
        prompt,
        image_size: imageSize,
        callback_url: ''
    };
    
    return new Promise((resolve, reject) => {
        const data = JSON.stringify(form);
        
        const options = {
            hostname: 'visual.volcengineapi.com',
            path: '/api/v3/visual/cv_sync2_async_submit_task',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Date': timestamp
            }
        };
        
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    const result = JSON.parse(body);
                    if (result.code === 0 && result.data && result.data.task_id) {
                        resolve({ success: true, taskId: result.data.task_id, pending: true });
                    } else {
                        reject(new Error(result.message || 'JiMeng API Error'));
                    }
                } catch (e) {
                    reject(e);
                }
            });
        });
        
        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

// API 路由
app.post('/api/generate-image', async (req, res) => {
    const { prompt, model, size } = req.body;
    
    if (!prompt) {
        return res.json({ success: false, error: 'Missing prompt' });
    }
    
    try {
        if (model === 'qwen') {
            const result = await generateWithQwen(prompt, size);
            res.json(result);
        } else if (model === 'jimeng') {
            const result = await generateWithJiMeng(prompt, size.replace('*', 'x'));
            res.json(result);
        } else {
            res.json({ success: false, error: 'Unknown model' });
        }
    } catch (err) {
        res.json({ success: false, error: err.message });
    }
});

app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`🎨 AI Image API running on port ${PORT}`);
    console.log(`   請設置環境變量:`);
    console.log(`   export DASHSCOPE_API_KEY="your-key"`);
    console.log(`   export VOLC_ACCESS_KEY="your-key"`);
    console.log(`   export VOLC_SECRET_KEY="your-secret"`);
});
