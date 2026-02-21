#!/usr/bin/env python3
"""
Crypto Wallet Monitor - Track multiple wallet balances across chains
Usage: python3 wallet_monitor.py <address> [chain:address2] ...
Examples: 
  python3 wallet_monitor.py 0x742d35Cc6634C0532925a3b844Bc9e7595f
  python3 wallet_monitor.py eth:0x742d35Cc6634C0532925a3b844Bc9e7595f btc:bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
"""

import requests
import sys
from datetime import datetime
import json

# RPC endpoints (free tier)
RPCS = {
    "eth": "https://eth.llamarpc.com",
    "bsc": "https://bsc-dataseed.binance.org",
    "polygon": "https://polygon-rpc.com",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
    "optimism": "https://mainnet.optimism.io",
}

def get_eth_balance(address, rpc):
    """Get ETH/ERC20 balance via RPC"""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    try:
        response = requests.post(rpc, json=payload, timeout=10)
        data = response.json()
        if 'result' in data:
            wei = int(data['result'], 16)
            return wei / 1e18
    except Exception as e:
        return f"Error: {str(e)[:30]}"
    return None

def get_btc_balance(address):
    """Get BTC balance via blockchain API"""
    try:
        url = f"https://blockstream.info/api/address/{address}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('chain_stats', {}).get('funded_txo_sum', 0) / 1e8
    except Exception as e:
        return f"Error: {str(e)[:30]}"
    return None

def parse_wallet(arg):
    """Parse wallet argument into (chain, address)"""
    if ':' in arg:
        parts = arg.split(':', 1)
        return parts[0].lower(), parts[1]
    # Auto-detect by prefix
    if arg.startswith('0x'):
        return 'eth', arg
    elif arg.startswith('bc1') or len(arg) in [26, 34]:
        return 'btc', arg
    return 'eth', arg

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 wallet_monitor.py <address> [chain:address2] ...")
        print("Chains: eth, bsc, polygon, arbitrum, optimism, btc")
        print("Examples:")
        print("  python3 wallet_monitor.py 0x742d35Cc6634C0532925a3b844Bc9e7595f")
        print("  python3 wallet_monitor.py eth:0x... btc:bc1q... bsc:0x...")
        sys.exit(1)
    
    wallets = sys.argv[1:]
    
    print(f"📊 Crypto Wallet Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    total_eth = 0
    total_btc = 0
    
    for arg in wallets:
        chain, address = parse_wallet(arg)
        
        if chain == 'btc':
            balance = get_btc_balance(address)
            if isinstance(balance, float):
                print(f"₿  {address[:8]}...{address[-6:]}: {balance:.6f} BTC")
                total_btc += balance
            else:
                print(f"❌ BTC {address}: {balance}")
        else:
            rpc = RPCS.get(chain)
            if not rpc:
                print(f"❌ Unknown chain: {chain}")
                continue
            balance = get_eth_balance(address, rpc)
            if isinstance(balance, float):
                print(f"◈  {chain.upper()} {address[:6]}...{address[-4:]}: {balance:.4f} {chain.upper()}")
                total_eth += balance
            else:
                print(f"❌ {chain.upper()} {address}: {balance}")
    
    print("=" * 60)
    if total_eth > 0:
        print(f"💵 Total ETH-like: {total_eth:.4f}")
    if total_btc > 0:
        print(f"₿  Total BTC: {total_btc:.6f}")

if __name__ == '__main__':
    main()
