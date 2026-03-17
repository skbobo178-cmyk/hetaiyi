#!/usr/bin/env python3
"""
weather-schedule-bot.py - 每天早上6點自動查詢排程地點天氣
"""

import re
import requests
from datetime import datetime, timedelta
import json

def fetch_schedule():
    """抓取排程網頁，返回今天和明天的排程地點"""
    url = "https://skyknow.cc/vendor-schedule/86919833-b290-4403-8552-158719eb34a1"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        html = response.text
        
        # 取得今天的日期資訊
        today = datetime.now()
        today_str = f"{today.year}年{today.month}月{today.day}日"
        
        # 解析排程 HTML
        schedules = []
        
        # 匹配日期和地點的模式
        # 格式: 2026年3月5日 星期四 ... 📍 地點名稱 ... ⏰ 時間
        date_pattern = r'(\d{4}年\d{1,2}月\d{1,2}日)\s*星期[一二三四五六日]'
        location_pattern = r'📍\s*([^<\n]+)'
        time_pattern = r'⏰\s*([^<\n]+)'
        
        # 找到所有日期位置
        dates = list(re.finditer(date_pattern, html))
        
        for i, date_match in enumerate(dates):
            date_str = date_match.group(1)
            start_pos = date_match.end()
            end_pos = dates[i+1].start() if i+1 < len(dates) else len(html)
            
            section = html[start_pos:end_pos]
            
            # 提取地點和時間
            loc_match = re.search(location_pattern, section)
            time_match = re.search(time_pattern, section)
            
            if loc_match:
                location = loc_match.group(1).strip()
                time_str = time_match.group(1).strip() if time_match else "時間未指定"
                
                schedules.append({
                    'date': date_str,
                    'location': location,
                    'time': time_str,
                    'is_today': date_str == today_str
                })
        
        return schedules
    
    except Exception as e:
        print(f"抓取排程失敗: {e}")
        return []

def get_location_for_weather(location_name):
    """將排程地點名稱轉換為天氣查詢用名稱"""
    location_map = {
        # 桃園地區
        '林口': 'Linkou',
        '林口仁愛': 'Linkou',
        '夢飛體育館': 'Linkou',  # 林口區南勢街
        '長庚': 'Guishan',
        '長庚管理大樓': 'Guishan',
        '大園': 'Dayuan',
        '大園大豐': 'Dayuan',
        '青埔': 'Dayuan',
        '青埔瑪格利特': 'Dayuan',
        '中茂新天地': 'Taoyuan',
        '中茂': 'Taoyuan',
        '桃園國際': 'Taoyuan',
        '桃園延平': 'Taoyuan',
        '蘆竹': 'Luzhu',
        '桃園': 'Taoyuan',
        '中壢': 'Zhongli',
        '龜山': 'Guishan',
        '龜山-文七': 'Guishan',
        '龜山楓峰': 'Guishan',
        '八德': 'Bade',
        '龍潭': 'Longtan',
        '大溪': 'Daxi',
        '復興': 'Fuxing',
        '楊梅': 'Yangmei',
        '平鎮': 'Pingzhen',

        # 新北地區
        '板橋': 'Banqiao',
        '板橋中新': 'Banqiao',
        '板橋-亞東': 'Banqiao',
        '三峽': 'Sanxia',
        '三峽路角': 'Sanxia',
        '蘆洲': 'Luzhou',
        '蘆洲-咕咕': 'Luzhou',
        '中和': 'Zhonghe',
        '中和 東森': 'Zhonghe',
        '土城': 'Tucheng',
        '新店': 'Xindian',
        '汐止': 'Xizhi',
        '淡水': 'Tamsui',
        '金山': 'Jinshan',
        '萬里': 'Wanli',
        '瑞芳': 'Ruifang',

        # 台北市
        '內湖': 'Neihu',
        '內湖葫州': 'Neihu',
        '內湖58': 'Neihu',
        '松山': 'Songshan',
        '松山南京東路': 'Songshan',
        '中正': 'Zhongzheng',
        '大同': 'Datong',
        '中山': 'Zhongshan',
        '大安': "Da'an",
        '信義': 'Xinyi',
        '士林': 'Shilin',
        '北投': 'Beitou',
        '南港': 'Nangang',
        '文山': 'Wenshan',

        # 宜蘭
        '宜蘭': 'Yilan',
        '礁溪': 'Jiaoxi',
        '羅東': 'Luodong',
        '蘇澳': 'Su\'ao',
        '頭城': 'Toucheng',

        # 基隆
        '基隆': 'Keelung',
        '七堵': 'Qidu',
        '安樂': 'Anle',
        '信義': 'Xinyi',  # 基隆市信義區
    }
    
    for key, value in location_map.items():
        if key in location_name:
            return value
    
    # 默認使用英文名稱
    return location_name

def fetch_weather(location_en):
    """使用 Open-Meteo API 查詢天氣"""
    
    # 地點座標對應表 (緯度, 經度)
    coords = {
        # 桃園市
        'Linkou': (25.08, 121.37),     # 林口區
        'Guishan': (25.02, 121.35),   # 龜山區
        'Dayuan': (25.06, 121.20),    # 大園區
        'Taoyuan': (24.99, 121.30),   # 桃園區
        'Luzhu': (25.08, 121.28),    # 蘆竹區
        'Zhongli': (24.97, 121.22),  # 中壢區
        'Bade': (24.93, 121.27),     # 八德區
        'Longtan': (24.88, 121.21),  # 龍潭區
        'Daxi': (24.93, 121.29),     # 大溪區
        'Fuxing': (24.82, 121.37),   # 復興區
        'Yangmei': (24.92, 121.15),  # 楊梅區
        'Pingzhen': (24.95, 121.25), # 平鎮區

        # 新北市
        'Banqiao': (25.01, 121.47),  # 板橋區
        'Sanxia': (24.88, 121.38),   # 三峽區
        'Luzhou': (25.08, 121.48),  # 蘆洲區
        'Zhonghe': (25.00, 121.52), # 中和區
        'Tucheng': (24.97, 121.52), # 土城區
        'Xindian': (24.98, 121.52), # 新店區
        'Xizhi': (25.06, 121.66),   # 汐止區
        'Tamsui': (25.17, 121.46),  # 淡水區
        'Jinshan': (25.23, 121.64), # 金山區
        'Wanli': (25.18, 121.65),   # 萬里區
        'Ruifang': (25.10, 121.85), # 瑞芳區

        # 台北市
        'Neihu': (25.08, 121.58),    # 內湖區
        'Songshan': (25.05, 121.55), # 松山區
        'Zhongzheng': (25.04, 121.52), # 中正區
        'Datong': (25.06, 121.51),   # 大同區
        'Zhongshan': (25.08, 121.52), # 中山區
        'Da\'an': (25.03, 121.55),  # 大安區
        'Xinyi': (25.04, 121.57),   # 信義區
        'Shilin': (25.10, 121.52),  # 士林區
        'Beitou': (25.14, 121.50),  # 北投區
        'Nangang': (25.05, 121.62), # 南港區
        'Wenshan': (25.00, 121.57), # 文山區

        # 宜蘭縣
        'Yilan': (24.75, 121.75),    # 宜蘭市
        'Jiaoxi': (24.69, 121.78),  # 礁溪鄉
        'Luodong': (24.68, 121.77), # 羅東鎮
        'Su\'ao': (24.62, 121.87),  # 蘇澳鎮
        'Toucheng': (24.83, 121.87), # 頭城鎮

        # 基隆市
        'Keelung': (25.13, 121.74),  # 基隆市區
        'Qidu': (25.10, 121.70),    # 七堵區
        'Anle': (25.14, 121.73),    # 安樂區
    }
    
    if location_en not in coords:
        return None
    
    lat, lon = coords[location_en]
    
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&hourly=temperature_2m,precipitation_probability,weathercode"
            f"&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum"
            f"&timezone=Asia/Taipei&forecast_days=1"
        )
        
        response = requests.get(url, timeout=30)
        data = response.json()
        
        # 解析天氣代碼
        def get_weather_desc(code):
            weather_codes = {
                0: '☀️ 晴朗',
                1: '🌤️ 大部晴朗',
                2: '⛅ 多雲',
                3: '☁️ 陰天',
                45: '🌫️ 霧',
                48: '🌫️ 霧凇',
                51: '🌦️ 毛毛雨',
                53: '🌦️ 中度毛毛雨',
                55: '🌧️ 密集毛毛雨',
                61: '🌧️ 小雨',
                63: '🌧️ 中雨',
                65: '🌧️ 大雨',
                80: '🌦️ 陣雨',
                81: '🌧️ 中度陣雨',
                82: '🌧️ 強陣雨',
                95: '⛈️ 雷雨',
                96: '⛈️ 雷雨伴冰雹',
                99: '⛈️ 強雷雨伴冰雹',
            }
            return weather_codes.get(code, f'🌡️ 天氣代碼 {code}')
        
        daily = data.get('daily', {})
        hourly = data.get('hourly', {})
        
        # 取得白天時段 (08:00-20:00) 的降雨機率
        precip_probs = hourly.get('precipitation_probability', [])
        times = hourly.get('time', [])
        
        day_precip = []
        for i, t in enumerate(times):
            hour = int(t.split('T')[1].split(':')[0])
            if 8 <= hour <= 20 and i < len(precip_probs):
                day_precip.append(precip_probs[i])
        
        max_precip = max(day_precip) if day_precip else 0
        avg_precip = sum(day_precip) / len(day_precip) if day_precip else 0
        
        weather_code = daily.get('weathercode', [0])[0]
        
        return {
            'description': get_weather_desc(weather_code),
            'temp_max': daily.get('temperature_2m_max', [None])[0],
            'temp_min': daily.get('temperature_2m_min', [None])[0],
            'precipitation': daily.get('precipitation_sum', [0])[0],
            'rain_chance_max': max_precip,
            'rain_chance_avg': round(avg_precip, 1),
        }
        
    except Exception as e:
        print(f"查詢天氣失敗: {e}")
        return None

def generate_weather_report(schedules):
    """生成天氣報告"""
    today = datetime.now()
    today_str = f"{today.month}/{today.day}"
    
    # 篩選今天的排程
    today_schedules = [s for s in schedules if s['is_today']]
    
    if not today_schedules:
        return f"📅 **{today_str} 排程天氣預報**\n\n今天沒有排程哦！休息一天～ ☕"
    
    report_lines = [f"📅 **{today_str} 排程天氣預報**\n"]
    
    for sched in today_schedules:
        location = sched['location']
        time_str = sched['time']
        
        # 查詢天氣
        weather_loc = get_location_for_weather(location)
        weather = fetch_weather(weather_loc)
        
        report_lines.append(f"📍 **{location}**")
        report_lines.append(f"⏰ {time_str}")
        
        if weather:
            report_lines.append(f"{weather['description']}")
            report_lines.append(f"🌡️ 氣溫: {weather['temp_min']:.0f}°C ~ {weather['temp_max']:.0f}°C")
            
            # 降雨建議
            if weather['rain_chance_max'] >= 70:
                report_lines.append(f"☔ **降雨機率高 ({weather['rain_chance_max']:.0f}%) - 記得帶傘！**")
            elif weather['rain_chance_max'] >= 40:
                report_lines.append(f"🌦️ 降雨機率中等 ({weather['rain_chance_max']:.0f}%) - 建議帶傘備用")
            elif weather['rain_chance_max'] >= 20:
                report_lines.append(f"☁️ 降雨機率低 ({weather['rain_chance_max']:.0f}%)")
            else:
                report_lines.append(f"☀️ 降雨機率極低 ({weather['rain_chance_max']:.0f}%)")
            
            if weather['precipitation'] > 0:
                report_lines.append(f"💧 預計雨量: {weather['precipitation']:.1f}mm")
        else:
            report_lines.append("❓ 天氣資料暫時無法取得")
        
        report_lines.append("")  # 空行分隔
    
    # 添加結尾
    report_lines.append("---")
    report_lines.append("🦕 GIGI 恐龍雞蛋糕祝你今天擺攤順利！")
    
    return "\n".join(report_lines)

def main():
    """主程序"""
    print(f"[{datetime.now()}] 開始執行排程天氣查詢...")
    
    # 抓取排程
    schedules = fetch_schedule()
    print(f"抓到 {len(schedules)} 筆排程資料")
    
    # 生成報告
    report = generate_weather_report(schedules)
    
    # 輸出報告 (會被 cron 送到 OpenClaw 處理)
    print(report)
    
    return report

if __name__ == "__main__":
    main()
