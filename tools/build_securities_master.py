#!/usr/bin/env python3
"""
Build comprehensive securities master file with sector/country mappings.
Uses known sector classifications and intelligent heuristics.
"""

import json
from typing import Dict

# GICS Sector classifications for major US securities
# Data sourced from public GICS sector classifications
KNOWN_SECTORS = {
    # Technology
    'AAPL': 'Information Technology',
    'MSFT': 'Information Technology',
    'NVDA': 'Information Technology',
    'GOOGL': 'Communication Services',
    'GOOG': 'Communication Services',
    'META': 'Communication Services',
    'TSLA': 'Consumer Discretionary',
    'AMZN': 'Consumer Discretionary',
    'AMD': 'Information Technology',
    'INTC': 'Information Technology',
    'CSCO': 'Information Technology',
    'ORCL': 'Information Technology',
    'ADBE': 'Information Technology',
    'CRM': 'Information Technology',
    'AVGO': 'Information Technology',
    'QCOM': 'Information Technology',
    'TXN': 'Information Technology',
    'AMAT': 'Information Technology',
    'LRCX': 'Information Technology',
    'KLAC': 'Information Technology',
    'MU': 'Information Technology',
    'ADI': 'Information Technology',
    'NXPI': 'Information Technology',
    'MRVL': 'Information Technology',
    'ANET': 'Information Technology',
    'PANW': 'Information Technology',
    'CRWD': 'Information Technology',
    'NOW': 'Information Technology',
    'INTU': 'Information Technology',
    'PLTR': 'Information Technology',
    'APP': 'Information Technology',
    'CDNS': 'Information Technology',
    'SNPS': 'Information Technology',
    
    # Communication Services
    'NFLX': 'Communication Services',
    'DIS': 'Communication Services',
    'CMCSA': 'Communication Services',
    'T': 'Communication Services',
    'VZ': 'Communication Services',
    'TMUS': 'Communication Services',
    'CHTR': 'Communication Services',
    'EA': 'Communication Services',
    'TTWO': 'Communication Services',
    'NTES': 'Communication Services',
    'WBD': 'Communication Services',
    'MTCH': 'Communication Services',
    'SPOT': 'Communication Services',
    'SNAP': 'Communication Services',
    'PINS': 'Communication Services',
    'XLC': 'Communication Services',
    
    # Financials
    'BRK.B': 'Financials',
    'JPM': 'Financials',
    'V': 'Financials',
    'MA': 'Financials',
    'BAC': 'Financials',
    'WFC': 'Financials',
    'GS': 'Financials',
    'MS': 'Financials',
    'C': 'Financials',
    'SCHW': 'Financials',
    'BLK': 'Financials',
    'AXP': 'Financials',
    'SPGI': 'Financials',
    'PGR': 'Financials',
    'CB': 'Financials',
    'COF': 'Financials',
    'BX': 'Financials',
    'KKR': 'Financials',
    'AIG': 'Financials',
    'MET': 'Financials',
    'PRU': 'Financials',
    'ALL': 'Financials',
    'TFC': 'Financials',
    'USB': 'Financials',
    'PNC': 'Financials',
    'CME': 'Financials',
    'MCO': 'Financials',
    'ICE': 'Financials',
    'HOOD': 'Financials',
    'SOFI': 'Financials',
    
    # Healthcare
    'LLY': 'Health Care',
    'JNJ': 'Health Care',
    'UNH': 'Health Care',
    'ABBV': 'Health Care',
    'MRK': 'Health Care',
    'TMO': 'Health Care',
    'ABT': 'Health Care',
    'PFE': 'Health Care',
    'DHR': 'Health Care',
    'AMGN': 'Health Care',
    'ISRG': 'Health Care',
    'VRTX': 'Health Care',
    'GILD': 'Health Care',
    'BSX': 'Health Care',
    'SYK': 'Health Care',
    'MDT': 'Health Care',
    'CVS': 'Health Care',
    'CI': 'Health Care',
    'HUM': 'Health Care',
    'REGN': 'Health Care',
    'BMY': 'Health Care',
    'ELV': 'Health Care',
    'ZTS': 'Health Care',
    'MCK': 'Health Care',
    'COR': 'Health Care',
    'BIIB': 'Health Care',
    'MRNA': 'Health Care',
    'IDXX': 'Health Care',
    'IQV': 'Health Care',
    'A': 'Health Care',
    
    # Consumer Discretionary
    'WMT': 'Consumer Staples',
    'COST': 'Consumer Staples',
    'PG': 'Consumer Staples',
    'KO': 'Consumer Staples',
    'PEP': 'Consumer Staples',
    'PM': 'Consumer Staples',
    'MO': 'Consumer Staples',
    'CL': 'Consumer Staples',
    'MDLZ': 'Consumer Staples',
    'KHC': 'Consumer Staples',
    'STZ': 'Consumer Staples',
    'GIS': 'Consumer Staples',
    'HSY': 'Consumer Staples',
    'KMB': 'Consumer Staples',
    'SYY': 'Consumer Staples',
    'K': 'Consumer Staples',
    'TAP': 'Consumer Staples',
    'CAG': 'Consumer Staples',
    'CPB': 'Consumer Staples',
    
    'HD': 'Consumer Discretionary',
    'MCD': 'Consumer Discretionary',
    'NKE': 'Consumer Discretionary',
    'SBUX': 'Consumer Discretionary',
    'TJX': 'Consumer Discretionary',
    'BKNG': 'Consumer Discretionary',
    'LOW': 'Consumer Discretionary',
    'TGT': 'Consumer Discretionary',
    'F': 'Consumer Discretionary',
    'GM': 'Consumer Discretionary',
    'MAR': 'Consumer Discretionary',
    'HLT': 'Consumer Discretionary',
    'YUM': 'Consumer Discretionary',
    'ORLY': 'Consumer Discretionary',
    'AZO': 'Consumer Discretionary',
    'CMG': 'Consumer Discretionary',
    'UBER': 'Consumer Discretionary',
    'ABNB': 'Consumer Discretionary',
    'DASH': 'Consumer Discretionary',
    'LULU': 'Consumer Discretionary',
    'DECK': 'Consumer Discretionary',
    'ROST': 'Consumer Discretionary',
    'DPZ': 'Consumer Discretionary',
    'DHI': 'Consumer Discretionary',
    'LEN': 'Consumer Discretionary',
    'NVR': 'Consumer Discretionary',
    'PHM': 'Consumer Discretionary',
    
    # Industrials
    'GE': 'Industrials',
    'BA': 'Industrials',
    'CAT': 'Industrials',
    'RTX': 'Industrials',
    'HON': 'Industrials',
    'UNP': 'Industrials',
    'LMT': 'Industrials',
    'DE': 'Industrials',
    'ETN': 'Industrials',
    'GEV': 'Industrials',
    'UPS': 'Industrials',
    'ADP': 'Industrials',
    'TT': 'Industrials',
    'PH': 'Industrials',
    'APH': 'Industrials',
    'GD': 'Industrials',
    'NOC': 'Industrials',
    'CSX': 'Industrials',
    'NSC': 'Industrials',
    'FDX': 'Industrials',
    'WM': 'Industrials',
    'RSG': 'Industrials',
    'EMR': 'Industrials',
    'ITW': 'Industrials',
    'MMM': 'Industrials',
    'PCAR': 'Industrials',
    'JCI': 'Industrials',
    'CARR': 'Industrials',
    'OTIS': 'Industrials',
    'FAST': 'Industrials',
    'PAYX': 'Industrials',
    'CTAS': 'Industrials',
    'CMI': 'Industrials',
    'ODFL': 'Industrials',
    'VRSK': 'Industrials',
    'CPRT': 'Industrials',
    'DAL': 'Industrials',
    'UAL': 'Industrials',
    'LUV': 'Industrials',
    'AAL': 'Industrials',
    
    # Energy
    'XOM': 'Energy',
    'CVX': 'Energy',
    'COP': 'Energy',
    'SLB': 'Energy',
    'EOG': 'Energy',
    'PXD': 'Energy',
    'MPC': 'Energy',
    'PSX': 'Energy',
    'VLO': 'Energy',
    'OXY': 'Energy',
    'HES': 'Energy',
    'KMI': 'Energy',
    'WMB': 'Energy',
    'HAL': 'Energy',
    'BKR': 'Energy',
    'FANG': 'Energy',
    'DVN': 'Energy',
    'MRO': 'Energy',
    'APA': 'Energy',
    'CTRA': 'Energy',
    
    # Materials
    'LIN': 'Materials',
    'APD': 'Materials',
    'SHW': 'Materials',
    'ECL': 'Materials',
    'FCX': 'Materials',
    'NEM': 'Materials',
    'DD': 'Materials',
    'DOW': 'Materials',
    'PPG': 'Materials',
    'NUE': 'Materials',
    'VMC': 'Materials',
    'MLM': 'Materials',
    'CTVA': 'Materials',
    'ALB': 'Materials',
    'IFF': 'Materials',
    'CE': 'Materials',
    'CF': 'Materials',
    'MOS': 'Materials',
    'BALL': 'Materials',
    'AVY': 'Materials',
    'PKG': 'Materials',
    
    # Real Estate
    'PLD': 'Real Estate',
    'AMT': 'Real Estate',
    'CCI': 'Real Estate',
    'EQIX': 'Real Estate',
    'PSA': 'Real Estate',
    'WELL': 'Real Estate',
    'SPG': 'Real Estate',
    'DLR': 'Real Estate',
    'O': 'Real Estate',
    'VICI': 'Real Estate',
    'CBRE': 'Real Estate',
    'AVB': 'Real Estate',
    'EQR': 'Real Estate',
    'VTR': 'Real Estate',
    'SBAC': 'Real Estate',
    'ARE': 'Real Estate',
    'INVH': 'Real Estate',
    'MAA': 'Real Estate',
    'EXR': 'Real Estate',
    'IRM': 'Real Estate',
    'CUBE': 'Real Estate',
    'BXP': 'Real Estate',
    'KIM': 'Real Estate',
    'REG': 'Real Estate',
    'HST': 'Real Estate',
    
    # Utilities
    'NEE': 'Utilities',
    'SO': 'Utilities',
    'DUK': 'Utilities',
    'CEG': 'Utilities',
    'SRE': 'Utilities',
    'AEP': 'Utilities',
    'VST': 'Utilities',
    'D': 'Utilities',
    'PCG': 'Utilities',
    'PEG': 'Utilities',
    'XEL': 'Utilities',
    'EXC': 'Utilities',
    'ED': 'Utilities',
    'EIX': 'Utilities',
    'ETR': 'Utilities',
    'WEC': 'Utilities',
    'DTE': 'Utilities',
    'ES': 'Utilities',
    'FE': 'Utilities',
    'AEE': 'Utilities',
    'CMS': 'Utilities',
    'CNP': 'Utilities',
    'AWK': 'Utilities',
    'PPL': 'Utilities',
}

# Country mappings for non-US securities
KNOWN_COUNTRIES = {
    # Already well-represented in the data
    # We'll rely on existing country data from holdings
}

def normalize_sector(sector: str) -> str:
    """Normalize sector names to GICS standard 11 sectors."""
    sector = sector.strip()
    
    # Already GICS compliant
    gics_sectors = [
        'Information Technology',
        'Health Care',
        'Financials',
        'Consumer Discretionary',
        'Industrials',
        'Consumer Staples',
        'Energy',
        'Utilities',
        'Real Estate',
        'Materials',
        'Communication Services'
    ]
    
    if sector in gics_sectors:
        return sector
    
    # Map variations
    sector_map = {
        'Communication': 'Communication Services',
        'Technology': 'Information Technology',
        'Healthcare': 'Health Care',
        'Consumer Cyclical': 'Consumer Discretionary',
        'Consumer Defensive': 'Consumer Staples',
        'Basic Materials': 'Materials',
        'Financial Services': 'Financials',
        'Financial': 'Financials',
        'Real Estate Investment Trusts (REITs)': 'Real Estate',
        'REIT': 'Real Estate',
    }
    
    return sector_map.get(sector, sector)

def build_securities_master() -> Dict:
    """Build complete securities master from extracted data + known sectors."""
    
    # Load extracted securities
    with open('data/securities_extracted.json', 'r') as f:
        extracted = json.load(f)
    
    master = {}
    enriched_count = 0
    
    print(f"Building securities master from {len(extracted)} securities...")
    
    for ticker, data in extracted.items():
        # Skip invalid tickers
        if ticker in ['nan', '-', ''] or ticker == 'None':
            continue
        
        # Determine sector
        if ticker in KNOWN_SECTORS:
            sector = KNOWN_SECTORS[ticker]
            enriched_count += 1
        else:
            # Use sector from data if not 'Unknown'
            sectors_seen = data['sectors_seen']
            if len(sectors_seen) == 1 and sectors_seen[0] == 'Unknown':
                sector = 'Unknown'
            else:
                # Use first non-Unknown sector
                valid_sectors = [s for s in sectors_seen if s not in ['Unknown', 'nan', '-', '']]
                sector = normalize_sector(valid_sectors[0]) if valid_sectors else 'Unknown'
        
        # Determine country
        countries_seen = data['countries_seen']
        if len(countries_seen) == 1:
            country = countries_seen[0]
        else:
            # Prefer non-Unknown country
            valid_countries = [c for c in countries_seen if c not in ['Unknown', 'nan', '-', '']]
            country = valid_countries[0] if valid_countries else 'Unknown'
        
        master[ticker] = {
            'name': data['name'],
            'sector': sector,
            'country': country,
            'source': 'known_mapping' if ticker in KNOWN_SECTORS else 'extracted'
        }
    
    print(f"Enriched {enriched_count} securities with known sector mappings")
    print(f"Total securities in master: {len(master)}")
    
    # Calculate coverage
    unknown_sectors = sum(1 for s in master.values() if s['sector'] == 'Unknown')
    coverage = 100 * (len(master) - unknown_sectors) / len(master)
    
    print(f"Sector coverage: {coverage:.1f}%")
    
    return master

def main():
    """Main entry point."""
    master = build_securities_master()
    
    # Save to file
    output_file = 'data/securities_master.json'
    with open(output_file, 'w') as f:
        json.dump(master, f, indent=2, sort_keys=True)
    
    print(f"\nSaved securities master to {output_file}")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()
