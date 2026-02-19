#!/usr/bin/env python3
"""
Crypto Price Alert - Monitor prices and send alerts
Usage: python3 price_alert.py --coin bitcoin --above 70000 --below 60000
"""

import requests
import sys
import time
import argparse
from datetime import datetime

COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_price(coin_id):
    """Get current price for a coin"""
    url = f"{COINGECKO_API}/simple/price"
    params = {
        'ids': coin_id,
        'vs_currencies': 'usd'
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        return data.get(coin_id, {}).get('usd')
    except Exception as e:
        print(f"Error: {e}")
        return None

def check_alerts(coin_id, above, below):
    """Check price and send alert if conditions met"""
    price = get_price(coin_id)
    if price is None:
        return
    
    print(f"📊 {coin_id}: ${price:,.2f} ({datetime.now().strftime('%H:%M:%S')})")
    
    if above and price >= above:
        print(f"🚀 ALERT: {coin_id} is ABOVE ${above:,.2f}! Current: ${price:,.2f}")
    
    if below and price <= below:
        print(f"📉 ALERT: {coin_id} is BELOW ${below:,.2f}! Current: ${price:,.2f}")

def main():
    parser = argparse.ArgumentParser(description='Crypto Price Alert')
    parser.add_argument('--coin', default='bitcoin', help='Coin ID (e.g., bitcoin, ethereum)')
    parser.add_argument('--above', type=float, help='Alert when price goes above')
    parser.add_argument('--below', type=float, help='Alert when price goes below')
    parser.add_argument('--interval', type=int, default=60, help='Check interval in seconds')
    parser.add_argument('--watch', action='store_true', help='Keep watching continuously')
    
    args = parser.parse_args()
    
    if args.watch:
        print(f"👀 Watching {args.coin}... Press Ctrl+C to stop")
        try:
            while True:
                check_alerts(args.coin, args.above, args.below)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n👋 Stopped")
    else:
        check_alerts(args.coin, args.above, args.below)

if __name__ == '__main__':
    main()
