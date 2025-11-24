#!/usr/bin/env python3
"""
Extract all unique securities from holdings files to build securities master.
"""

import json
import glob
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set

def extract_unique_securities() -> Dict:
    """Extract all unique securities from holdings files."""
    
    securities = {}  # ticker -> {name, countries_seen, sectors_seen, count}
    
    holdings_files = sorted(glob.glob('data/holdings_json/*.json'))
    
    print(f"Analyzing {len(holdings_files)} holdings files...")
    
    for filepath in holdings_files:
        fund_ticker = Path(filepath).stem
        
        with open(filepath, 'r') as f:
            holdings = json.load(f)
        
        for holding in holdings:
            ticker = str(holding.get('ticker', '')).strip()
            name = str(holding.get('name', '')).strip()
            sector = str(holding.get('sector', 'Unknown')).strip()
            country = str(holding.get('country', 'Unknown')).strip()
            
            if not ticker:
                continue
            
            if ticker not in securities:
                securities[ticker] = {
                    'name': name,
                    'countries_seen': set(),
                    'sectors_seen': set(),
                    'found_in_funds': [],
                    'count': 0
                }
            
            securities[ticker]['countries_seen'].add(country)
            securities[ticker]['sectors_seen'].add(sector)
            securities[ticker]['found_in_funds'].append(fund_ticker)
            securities[ticker]['count'] += 1
            
            # Use the longest name seen (usually most complete)
            if len(name) > len(securities[ticker]['name']):
                securities[ticker]['name'] = name
    
    print(f"\nFound {len(securities)} unique securities")
    
    # Convert sets to lists for JSON serialization
    for ticker, data in securities.items():
        data['countries_seen'] = sorted(list(data['countries_seen']))
        data['sectors_seen'] = sorted(list(data['sectors_seen']))
    
    return securities

def analyze_coverage(securities: Dict):
    """Analyze sector/country coverage."""
    
    total = len(securities)
    
    # Count securities with known sectors
    unknown_sectors = sum(1 for s in securities.values() 
                         if s['sectors_seen'] == ['Unknown'])
    
    unknown_countries = sum(1 for s in securities.values() 
                           if s['countries_seen'] == ['Unknown'])
    
    print(f"\n{'='*70}")
    print("COVERAGE ANALYSIS")
    print(f"{'='*70}")
    print(f"Total unique securities: {total:,}")
    print(f"Securities with unknown sector: {unknown_sectors:,} ({100*unknown_sectors/total:.1f}%)")
    print(f"Securities with unknown country: {unknown_countries:,} ({100*unknown_countries/total:.1f}%)")
    
    # Find most common securities
    sorted_securities = sorted(securities.items(), 
                             key=lambda x: x[1]['count'], 
                             reverse=True)
    
    print(f"\n{'='*70}")
    print("TOP 20 MOST COMMON SECURITIES")
    print(f"{'='*70}")
    print(f"{'Ticker':<10} {'Name':<40} {'Funds':<5}")
    print("-" * 70)
    
    for ticker, data in sorted_securities[:20]:
        print(f"{ticker:<10} {data['name'][:40]:<40} {data['count']:<5}")
    
    # Show sector distribution
    sector_counts = defaultdict(int)
    for data in securities.values():
        for sector in data['sectors_seen']:
            sector_counts[sector] += 1
    
    print(f"\n{'='*70}")
    print("SECTOR DISTRIBUTION")
    print(f"{'='*70}")
    for sector, count in sorted(sector_counts.items(), key=lambda x: -x[1]):
        print(f"{sector:<30} {count:>6,} securities")
    
    # Show country distribution
    country_counts = defaultdict(int)
    for data in securities.values():
        for country in data['countries_seen']:
            country_counts[country] += 1
    
    print(f"\n{'='*70}")
    print("COUNTRY DISTRIBUTION (Top 20)")
    print(f"{'='*70}")
    for country, count in sorted(country_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"{country:<30} {count:>6,} securities")

def main():
    """Main entry point."""
    securities = extract_unique_securities()
    analyze_coverage(securities)
    
    # Save to file
    output_file = 'data/securities_extracted.json'
    with open(output_file, 'w') as f:
        json.dump(securities, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"Saved extracted securities to {output_file}")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    main()
