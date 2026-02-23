#!/usr/bin/env python3
"""
Crypto Price Tracker - Real-time prices + alerts
Usage: python3 crypto_price.py [coin1,coin2,...]
Examples:
  python3 crypto_price.py btc,eth,sol
  python3 crypto_price.py btc,eth,sol,avax,dogecoin
"""

import requests
import sys
import os
from datetime import datetime

# CoinGecko API
CG_API = "https://api.coingecko.com/api/v3"

# Popular coins
DEFAULT_COINS = ["bitcoin", "ethereum", "solana", "binancecoin", "avalanche-2", "cardano", "dogecoin", "ripple"]

def get_prices(coin_ids):
    """Fetch current prices"""
    try:
        ids = ",".join(coin_ids)
        url = f"{CG_API}/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"❌ Error: {e}")
    return {}

def format_num(n):
    """Format number with commas"""
    if n >= 1000:
        return f"{n:,.2f}"
    elif n >= 1:
        return f"{n:.2f}"
    elif n >= 0.01:
        return f"{n:.4f}"
    else:
        return f"{n:.6f}"

def get_emoji(change):
    """Get emoji for price change"""
    if change > 5:
        return "🚀"
    elif change > 2:
        return "📈"
    elif change > 0:
        return "↗️"
    elif change > -2:
        return "↘️"
    elif change > -5:
        return "📉"
    else:
        return "💸"

def main():
    # Parse coins from args or use defaults
    if len(sys.argv) > 1:
        coins = [c.strip().lower() for c in sys.argv[1].split(",")]
    else:
        coins = DEFAULT_COINS
    
    prices = get_prices(coins)
    
    if not prices:
        print("❌ Failed to fetch prices")
        sys.exit(1)
    
    # Sort by market cap (just use the order)
    print(f"💹 Crypto Prices - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 55)
    print(f"{'Coin':<12} {'Price (USD)':>14} {'24h':>10} {'Trend'}")
    print("-" * 55)
    
    for coin in coins:
        if coin in prices:
            data = prices[coin]
            price = data.get("usd", 0)
            change = data.get("usd_24h_change", 0)
            emoji = get_emoji(change)
            # Pretty name
            name = coin.title().replace("-", " ")[:12]
            print(f"{name:<12} ${format_num(price):>13} {change:>+9.2f}% {emoji}")
        else:
            print(f"{coin:<12} NOT FOUND")
    
    print("=" * 55)

if __name__ == "__main__":
    main()
