#! /usr/bin/env python3

import tldextract
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict

def banner():
    print(r"""
              __           ___  __        __  ___ 
        |  | |__) |    \_/  |  |__)  /\  /  `  |  
        \__/ |  \ |___ / \  |  |  \ /~~\ \__,  |  
        """)

def init():
    return tldextract.extract

def GetDomain(url: str):
    if not url:
        return
    
    # Initialize tldextract
    ext = init()
    domain = ext(url)
    return domain.fqdn or None

def GetApexDomain(url: str):
    # Initialize tldextract
    if not url:
        return
    ext = init()
    domain = ext(url)
    return domain.registered_domain or None

def process_urls(urls, domain=False, apex=False):
    """Process a list of URLs and extract domains based on the flags."""
    results = []
    
    with ThreadPoolExecutor() as executor:
        
        if domain:
            results = list(executor.map(GetDomain, urls))
        
        elif apex:
            results = list(executor.map(GetApexDomain, urls))
    
    return [result for result in results if result]  # Filter out None values

def read_from_stdin():
    """Read input from stdin (e.g., piped input)."""
    return [line.strip() for line in sys.stdin.readlines() if line.strip()]

def main():
    parser = argparse.ArgumentParser(description='Extract domain information from URLs.')
    parser.add_argument('-u', '--url', type=str, help='Single URL to extract domain from', metavar='')
    parser.add_argument('-f', '--file', type=str, help='File containing URLs to extract domains from', metavar='')
    parser.add_argument('--domain', action='store_true', help='Extract fully qualified domain names (FQDN)')
    parser.add_argument('--apex', action='store_true', help='Extract apex (registered) domains')
    parser.add_argument('--uniq', action='store_true', help='Only output unique domains')
    parser.add_argument('--silent', action='store_true', help='silent mode')
    args = parser.parse_args()

    # Determine the source of URLs
    urls = []
    if args.url:
        urls.append(args.url)
    
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                urls = [line.strip() for line in f.readlines() if line.strip()]
        
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin if no URL or file is provided
        urls = read_from_stdin()

    # Validate that at least one flag is set
    if not args.domain and not args.apex:
        print("Error: At least one of --fqdn or --apex must be specified.", file=sys.stderr)
        sys.exit(1)

    # Process URLs concurrently
    results = process_urls(urls, domain=args.domain, apex=args.apex)

    # Output unique domains if requested
    if args.uniq:
        results = list(OrderedDict.fromkeys(results))
    
    # Print banner
    if not args.silent:
        banner()
    
    # Print results
    for result in results:
        print(result)

if __name__ == '__main__':
    main()