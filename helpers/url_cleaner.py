#!/usr/bin/env python3
"""
URL Cleaner - Remove tracking parameters from URLs

Removes common tracking parameters like:
- utm_source, utm_medium, utm_campaign, utm_term, utm_content
- gclid (Google Ads)
- fbclid (Facebook)
- tcclid (TikTok)
- msclkid (Microsoft)
- _ga, _gl (Google Analytics)
- ref, referrer
- and many more...

Usage:
    python url_cleaner.py "https://example.com/page?utm_source=twitter&gclid=abc123"
    python url_cleaner.py -f urls.txt          # Clean URLs from file
    python url_cleaner.py --clipboard          # Clean URL from clipboard
    python url_cleaner.py --input "https://..." # Clean and copy to clipboard
"""

import sys
import re
import argparse
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Common tracking parameters to remove
TRACKING_PARAMS = {
    # Google Analytics & Ads
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'utm_id', 'utm_source_platform', 'utm_creative_format', 'utm_marketing_tactic',
    '_ga', '_gl', 'gclid', 'gclsrc', 'dclid', 'gad_source',
    
    # Facebook
    'fbclid', 'fb_action_ids', 'fb_action_types', 'fb_source', 'fb_ref',
    
    # TikTok
    'tcclid', 'ttclid',
    
    # Microsoft/Bing
    'msclkid', 'mc_cid', 'mc_eid',
    
    # Twitter
    'twclid',
    
    # Other common trackers
    'ref', 'referrer', 'reference', 'source', 'affiliate', 'aff_id',
    'partner_id', 'campaign_id', 'click_id', 'oly_enc_id', 'oly_anon_id',
    '__s', '_hsenc', '_hsmi', 'mkt_tok',
    
    # Amazon
    'tag', 'linkCode', 'ascref',
    
    # Generic
    'id', 'uid', 'user_id',  # Too aggressive, commented out
}

# Additional patterns for more aggressive cleaning
TRACKING_PATTERNS = [
    r'^utm_',           # Any utm_ prefix
    r'^oly_',           # Optimizely
    r'^__',             # Double underscore (often analytics)
]


def is_tracking_param(key: str) -> bool:
    """Check if a parameter is a tracking parameter."""
    key_lower = key.lower()
    
    # Direct match
    if key_lower in TRACKING_PARAMS:
        return True
    
    # Pattern match
    for pattern in TRACKING_PATTERNS:
        if re.match(pattern, key_lower):
            return True
    
    return False


def clean_url(url: str) -> str:
    """Remove tracking parameters from a URL."""
    try:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        
        # Filter out tracking parameters
        clean_params = {
            k: v for k, v in query_params.items() 
            if not is_tracking_param(k)
        }
        
        # Rebuild URL
        new_query = urlencode(clean_params, doseq=True)
        clean_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))
        
        return clean_url
    except Exception as e:
        return url  # Return original if parsing fails


def read_from_clipboard() -> str:
    """Read URL from clipboard (macOS)."""
    import subprocess
    try:
        return subprocess.check_output(
            ['pbpaste'], text=True
        ).strip()
    except Exception:
        return None


def write_to_clipboard(text: str) -> bool:
    """Write text to clipboard (macOS)."""
    import subprocess
    try:
        process = subprocess.Popen(
            ['pbcopy'], stdin=subprocess.PIPE
        )
        process.communicate(text.encode('utf-8'))
        return True
    except Exception:
        return False


def read_from_file(filepath: str) -> list:
    """Read URLs from a file (one per line)."""
    try:
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(
        description='Remove tracking parameters from URLs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'url', 
        nargs='?', 
        help='URL to clean'
    )
    parser.add_argument(
        '-f', '--file',
        help='Read URLs from file (one per line)'
    )
    parser.add_argument(
        '-c', '--clipboard',
        action='store_true',
        help='Read URL from clipboard and clean it'
    )
    parser.add_argument(
        '-o', '--output-clipboard',
        action='store_true',
        help='Copy cleaned URL to clipboard'
    )
    parser.add_argument(
        '-i', '--input',
        help='Clean URL and output result (alias for positional arg)'
    )
    
    args = parser.parse_args()
    
    urls = []
    
    # Determine source of URLs
    if args.clipboard:
        url = read_from_clipboard()
        if url:
            urls = [url]
        else:
            print("Error: Could not read from clipboard")
            return 1
    elif args.file:
        urls = read_from_file(args.file)
    elif args.input:
        urls = [args.input]
    elif args.url:
        urls = [args.url]
    else:
        parser.print_help()
        return 0
    
    # Process URLs
    cleaned_urls = []
    for url in urls:
        cleaned = clean_url(url)
        cleaned_urls.append(cleaned)
        print(cleaned)
    
    # Copy to clipboard if requested
    if args.output_clipboard and cleaned_urls:
        # If multiple URLs, join with newlines
        text = '\n'.join(cleaned_urls)
        if write_to_clipboard(text):
            print("\n✓ Copied to clipboard", file=sys.stderr)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
