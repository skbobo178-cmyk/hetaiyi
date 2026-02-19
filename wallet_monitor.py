#!/usr/bin/env python3
"""
Crypto Wallet Monitor - Track multiple wallet balances
Usage: python3 wallet_monitor.py <wallet_address> [address2] ...
"""

import requests
import sys
from datetime import datetime

# Ethereum RPC (free tier)
ETH_RPC = "https://eth.llamarpc.com"

def get_eth_balance(address):
    """Get ETH balance for an address"""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    try:
        response = requests.post(ETH_RPC, json=payload, timeout=10)
        data = response.json()
        if 'result' in data:
            # Convert wei to ETH
            wei = int(data['result'], 16)
            return wei / 1e18
    except Exception as e:
        return f"Error: {e}"
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 wallet_monitor.py <wallet_address> [address2] ...")
        print("Example: python3 wallet_monitor.py 0x742d35Cc6634C0532925a3b844Bc9e7595f")
        sys.exit(1)
    
    wallets = sys.argv[1:]
    
    print(f"📊 Crypto Wallet Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    total = 0
    for wallet in wallets:
        balance = get_eth_balance(wallet)
        if isinstance(balance, float):
            print(f"💰 {wallet[:6]}...{wallet[-4:]}: {balance:.4f} ETH")
            total += balance
        else:
            print(f"❌ {wallet}: {balance}")
    
    if total > 0:
        print("=" * 60)
        print(f"💵 Total: {total:.4f} ETH")

if __name__ == '__main__':
    main()
