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
    "avax": "https://api.avax.network/ext/bc/C/rpc",
    "sol": "https://api.mainnet-beta.solana.com",
}

# CoinGecko API for price lookup (free, no key needed)
PRICE_API = "https://api.coingecko.com/api/v3/simple/price"

# CoinGecko IDs
CG_IDS = {
    "eth": "ethereum",
    "bsc": "binancecoin", 
    "polygon": "matic-network",
    "arbitrum": "ethereum",  # Uses ETH price
    "optimism": "ethereum",  # Uses ETH price
    "avax": "avalanche-2",
    "sol": "solana",
    "btc": "bitcoin",
}

# Cache prices for 5 minutes
_price_cache = {"prices": {}, "timestamp": 0}
CACHE_DURATION = 300  # 5 minutes

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

def get_cg_id(chain):
    """Get CoinGecko ID for a chain"""
    return CG_IDS.get(chain, chain)

def get_prices(chains):
    """Get USD prices for chains (cached)"""
    global _price_cache
    
    now = datetime.now().timestamp()
    if now - _price_cache["timestamp"] < CACHE_DURATION and _price_cache["prices"]:
        return _price_cache["prices"]
    
    # Fetch fresh prices
    ids = [get_cg_id(c) for c in chains if c != 'btc']
    ids.append('bitcoin')  # Always include BTC
    ids = list(set(ids))  # Deduplicate
    
    try:
        url = f"{PRICE_API}?ids={','.join(ids)}&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            _price_cache["prices"] = data
            _price_cache["timestamp"] = now
            return data
    except Exception as e:
        print(f"⚠️ Price fetch error: {str(e)[:50]}")
    
    return {}

def get_usd_price(chain, prices):
    """Get USD price for a chain"""
    cg_id = get_cg_id(chain)
    return prices.get(cg_id, {}).get('usd', 0)

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
    elif arg.startswith('sol') or len(arg) > 30:
        return 'sol', arg
    return 'eth', arg

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 wallet_monitor.py <address> [chain:address2] ...")
        print("Chains: eth, bsc, polygon, arbitrum, optimism, avax, sol, btc")
        print("Examples:")
        print("  python3 wallet_monitor.py 0x742d35Cc6634C0532925a3b844Bc9e7595f")
        print("  python3 wallet_monitor.py eth:0x... btc:bc1q... bsc:0x...")
        sys.exit(1)
    
    wallets = sys.argv[1:]
    
    # Parse and collect chains
    chains = []
    wallet_data = []
    for arg in wallets:
        chain, address = parse_wallet(arg)
        chains.append(chain)
        wallet_data.append((chain, address))
    
    # Fetch prices once
    prices = get_prices(set(chains))
    
    print(f"📊 Crypto Wallet Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    total_usd = 0
    
    for chain, address in wallet_data:
        if chain == 'btc':
            balance = get_btc_balance(address)
            if isinstance(balance, float):
                usd_price = prices.get('bitcoin', {}).get('usd', 0)
                usd_value = balance * usd_price
                print(f"₿  BTC {address[:8]}...{address[-6:]}: {balance:.6f} BTC  (${usd_value:,.2f})")
                total_usd += usd_value
            else:
                print(f"❌ BTC {address}: {balance}")
        elif chain == 'sol':
            # Simple SOL balance check via RPC
            try:
                payload = {
                    "jsonrpc": "2.0",
                    "method": "getBalance",
                    "params": [address],
                    "id": 1
                }
                response = requests.post(RPCS["sol"], json=payload, timeout=10)
                data = response.json()
                if 'result' in data:
                    lamports = data['result']['value']
                    balance = lamports / 1e9
                    usd_price = get_usd_price(chain, prices)
                    usd_value = balance * usd_price
                    print(f"◎  SOL {address[:8]}...{address[-4:]}: {balance:.4f} SOL  (${usd_value:,.2f})")
                    total_usd += usd_value
                else:
                    print(f"❌ SOL {address}: {data.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"❌ SOL {address}: Error - {str(e)[:30]}")
        else:
            rpc = RPCS.get(chain)
            if not rpc:
                print(f"❌ Unknown chain: {chain}")
                continue
            balance = get_eth_balance(address, rpc)
            if isinstance(balance, float):
                usd_price = get_usd_price(chain, prices)
                usd_value = balance * usd_price
                print(f"◈  {chain.upper()} {address[:6]}...{address[-4:]}: {balance:.4f} {chain.upper()}  (${usd_value:,.2f})")
                total_usd += usd_value
            else:
                print(f"❌ {chain.upper()} {address}: {balance}")
    
    print("=" * 70)
    print(f"💰 Total Portfolio Value: ${total_usd:,.2f} USD")

if __name__ == '__main__':
    main()
