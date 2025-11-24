#!/usr/bin/env python3
"""
Enhanced holdings processor with sector/country enrichment.
Uses securities master file to enrich holdings data.
"""

import os
import pandas as pd
import json
import glob
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
INPUT_DIR = 'data/holdings_files'
OUTPUT_DIR = 'data/holdings_json'
OUTPUT_JS_DIR = 'data/holdings_js'
METADATA_DIR = 'data/fund_metadata'
SECURITIES_MASTER_FILE = 'data/securities_master.json'

# Create output directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_JS_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

class SecuritiesEnricher:
    """Enriches securities data using master file."""
    
    def __init__(self, master_file: str):
        """Load securities master file."""
        self.master = {}
        if os.path.exists(master_file):
            with open(master_file, 'r') as f:
                self.master = json.load(f)
            print(f"Loaded {len(self.master)} securities from master file")
        else:
            print(f"WARNING: Securities master file not found at {master_file}")
    
    def enrich(self, ticker: str, name: str, sector: str, country: str) -> tuple:
        """
        Enrich security data using master file.
        Returns: (enriched_sector, enriched_country)
        """
        ticker = str(ticker).strip().upper()
        
        if ticker in self.master:
            master_data = self.master[ticker]
            
            # Use master data if current is Unknown
            if sector == 'Unknown' or sector == 'nan' or not sector:
                sector = master_data.get('sector', 'Unknown')
            
            if country == 'Unknown' or country == 'nan' or not country:
                country = master_data.get('country', 'Unknown')
        
        return (sector, country)


def is_valid_ticker(ticker: str) -> bool:
    """Validate ticker symbol."""
    if not ticker or ticker in ['nan', 'None', 'none']:
        return False
    
    # Skip very long strings (likely copyright notices)
    if len(ticker) > 50:
        return False
    
    # Skip if contains keywords indicating it's not a ticker
    keywords = ['copyright', 'blackrock', 'ishares', 'carefully consider']
    if any(kw in ticker.lower() for kw in keywords):
        return False
    
    return True


def normalize_field(value: str, default: str = 'Unknown') -> str:
    """Normalize sector/country field values."""
    value = str(value).strip()
    if value in ['-', 'nan', 'None', 'none', '']:
        return default
    
    # Normalize sector names to GICS standard
    sector_map = {
        'Communication': 'Communication Services',
        'Communication Services': 'Communication Services',
        'Information Technology': 'Information Technology',
        'Health Care': 'Health Care',
        'Financials': 'Financials',
        'Consumer Discretionary': 'Consumer Discretionary',
        'Industrials': 'Industrials',
        'Consumer Staples': 'Consumer Staples',
        'Energy': 'Energy',
        'Utilities': 'Utilities',
        'Real Estate': 'Real Estate',
        'Materials': 'Materials',
    }
    
    return sector_map.get(value, value)


def process_ishares_csv(filepath: str, enricher: SecuritiesEnricher) -> Optional[List[Dict]]:
    """Process iShares CSV format with enrichment."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        header_row = 0
        for i, line in enumerate(lines):
            if line.startswith('Ticker') or line.startswith('Symbol'):
                header_row = i
                break
        
        df = pd.read_csv(filepath, skiprows=header_row)
        
        # Handle weight column precedence
        weight_col = None
        for col in ['Weight (%)', 'Market Weight', 'Notional Weight', 'Weight']:
            if col in df.columns:
                weight_col = col
                break
        
        if weight_col:
            df = df.rename(columns={weight_col: 'weight'})
        
        # Map other columns
        col_map = {
            'Ticker': 'ticker',
            'Symbol': 'ticker',
            'Name': 'name',
            'Sector': 'sector',
            'Location': 'country',
            'Asset Class': 'asset_class'
        }
        
        df = df.rename(columns=col_map)
        
        # Filter for required columns
        required_cols = ['ticker', 'name', 'weight']
        if not all(col in df.columns for col in required_cols):
            print(f"Skipping {filepath}: Missing required columns")
            return None
        
        # Clean data
        df['weight'] = pd.to_numeric(df['weight'], errors='coerce').fillna(0)
        
        # Handle missing sectors/countries
        if 'sector' not in df.columns:
            df['sector'] = 'Unknown'
        if 'country' not in df.columns:
            df['country'] = 'Unknown'
        
        # Enrich data
        enriched_holdings = []
        for _, row in df.iterrows():
            ticker = str(row['ticker']).strip().upper()
            name = str(row['name']).strip()
            sector = normalize_field(row.get('sector', 'Unknown'))
            country = normalize_field(row.get('country', 'Unknown'))
            weight = float(row['weight'])
            
            if not is_valid_ticker(ticker):
                continue
            
            # Enrich using master file
            sector, country = enricher.enrich(ticker, name, sector, country)
            
            enriched_holdings.append({
                'ticker': ticker,
                'name': name,
                'sector': sector,
                'country': country,
                'weight': weight
            })
        
        return enriched_holdings
        
    except Exception as e:
        print(f"Error processing iShares file {filepath}: {e}")
        return None


def process_statestreet_xlsx(filepath: str, enricher: SecuritiesEnricher) -> Optional[List[Dict]]:
    """Process State Street XLSX format with enrichment."""
    try:
        df = pd.read_excel(filepath)
        
        # Find header row
        header_row = -1
        for i, row in df.iterrows():
            row_str = row.astype(str).str.lower().tolist()
            if 'ticker' in row_str or 'symbol' in row_str:
                header_row = i
                break
        
        if header_row != -1:
            df = pd.read_excel(filepath, skiprows=header_row + 1)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        col_map = {
            'Ticker': 'ticker',
            'Symbol': 'ticker',
            'Name': 'name',
            'Sector': 'sector',
            'Weight': 'weight',
            '% of Fund': 'weight',
            'Location': 'country',
            'Country': 'country'
        }
        
        df = df.rename(columns=col_map)
        
        # Filter
        required_cols = ['ticker', 'name', 'weight']
        if not all(col in df.columns for col in required_cols):
            if 'ticker' not in df.columns and 'Identifier' in df.columns:
                df['ticker'] = df['Identifier']
            
            if 'weight' not in df.columns:
                print(f"Skipping {filepath}: Missing weight column")
                return None
        
        # Clean data
        df['weight'] = pd.to_numeric(df['weight'], errors='coerce').fillna(0)
        
        # SSGA weights might be decimal (0.05) or percent (5.0)
        if df['weight'].max() < 1.05 and df['weight'].max() > 0:
            df['weight'] = df['weight'] * 100
        
        if 'sector' not in df.columns:
            df['sector'] = 'Unknown'
        if 'country' not in df.columns:
            df['country'] = 'Unknown'
        
        # Enrich data
        enriched_holdings = []
        for _, row in df.iterrows():
            ticker = str(row['ticker']).strip().upper()
            name = str(row['name']).strip()
            sector = normalize_field(row.get('sector', 'Unknown'))
            country = normalize_field(row.get('country', 'Unknown'))
            weight = float(row['weight'])
            
            if not is_valid_ticker(ticker):
                continue
            
            # Enrich using master file
            sector, country = enricher.enrich(ticker, name, sector, country)
            
            enriched_holdings.append({
                'ticker': ticker,
                'name': name,
                'sector': sector,
                'country': country,
                'weight': weight
            })
        
        return enriched_holdings
        
    except Exception as e:
        print(f"Error processing State Street file {filepath}: {e}")
        return None


def process_vanguard_json(filepath: str, enricher: SecuritiesEnricher) -> Optional[List[Dict]]:
    """Process Vanguard JSON format with enrichment."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Extract holdings from the JSON structure
        if 'fund' in data and 'entity' in data['fund']:
            raw_holdings = data['fund']['entity']
        else:
            print(f"Unexpected JSON structure in {filepath}")
            return None
        
        enriched_holdings = []
        for h in raw_holdings:
            ticker = str(h.get('ticker', '')).strip().upper()
            name = str(h.get('longName', h.get('shortName', ''))).strip()
            weight = h.get('percentWeight', h.get('weight', 0))
            
            if not is_valid_ticker(ticker):
                continue
            
            try:
                weight = float(weight)
            except:
                weight = 0.0
            
            # Vanguard data doesn't have sector/country, so we rely entirely on enrichment
            sector, country = enricher.enrich(ticker, name, 'Unknown', 'Unknown')
            
            enriched_holdings.append({
                'ticker': ticker,
                'name': name,
                'sector': sector,
                'country': country,
                'weight': weight
            })
        
        return enriched_holdings
        
    except Exception as e:
        print(f"Error processing Vanguard JSON file {filepath}: {e}")
        return None


def compute_fund_metadata(holdings: List[Dict], ticker: str) -> Dict:
    """Compute aggregated fund metadata from holdings."""
    
    sector_allocation = {}
    country_allocation = {}
    total_weight = 0
    
    for holding in holdings:
        weight = holding.get('weight', 0)
        sector = holding.get('sector', 'Unknown')
        country = holding.get('country', 'Unknown')
        
        total_weight += weight
        
        # Aggregate sectors
        if sector not in sector_allocation:
            sector_allocation[sector] = 0
        sector_allocation[sector] += weight
        
        # Aggregate countries
        if country not in country_allocation:
            country_allocation[country] = 0
        country_allocation[country] += weight
    
    # Normalize to percentages (should already be, but just in case)
    if total_weight > 0:
        sector_allocation = {k: (v / total_weight * 100) for k, v in sector_allocation.items()}
        country_allocation = {k: (v / total_weight * 100) for k, v in country_allocation.items()}
    
    # Calculate coverage metrics
    unknown_sector_weight = sector_allocation.get('Unknown', 0)
    sector_coverage = 100 - unknown_sector_weight
    
    unknown_country_weight = country_allocation.get('Unknown', 0)
    country_coverage = 100 - unknown_country_weight
    
    metadata = {
        'ticker': ticker,
        'holdings_count': len(holdings),
        'total_weight': round(total_weight, 2),
        'sector_allocation': {k: round(v, 2) for k, v in sorted(sector_allocation.items(), key=lambda x: -x[1])},
        'country_allocation': {k: round(v, 2) for k, v in sorted(country_allocation.items(), key=lambda x: -x[1])},
        'sector_coverage_pct': round(sector_coverage, 2),
        'country_coverage_pct': round(country_coverage, 2)
    }
    
    return metadata


def save_outputs(ticker: str, holdings: List[Dict], metadata: Dict):
    """Save holdings and metadata to JSON and JS files."""
    
    # Save holdings JSON
    json_file = os.path.join(OUTPUT_DIR, f"{ticker}.json")
    with open(json_file, 'w') as f:
        json.dump(holdings, f, indent=2)
    
    # Save holdings JS
    js_file = os.path.join(OUTPUT_JS_DIR, f"{ticker}.js")
    with open(js_file, 'w') as f:
        f.write(f"if (!window.ETF_HOLDINGS) window.ETF_HOLDINGS = {{}};\n")
        f.write(f"window.ETF_HOLDINGS['{ticker}'] = ")
        json.dump(holdings, f, indent=2)
        f.write(";\n")
    
    # Save metadata
    metadata_file = os.path.join(METADATA_DIR, f"{ticker}.json")
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"  ✓ Saved {len(holdings)} holdings + metadata)")


def main():
    """Main processing pipeline."""
    
    print("="*70)
    print("ENHANCED HOLDINGS PROCESSOR WITH SECTOR/COUNTRY ENRICHMENT")
    print("="*70)
    
    # Load securities enricher
    enricher = SecuritiesEnricher(SECURITIES_MASTER_FILE)
    
    files = glob.glob(os.path.join(INPUT_DIR, '*'))
    
    print(f"\nProcessing {len(files)} holdings files...\n")
    
    success_count = 0
    failed_count = 0
    
    for filepath in sorted(files):
        filename = os.path.basename(filepath)
        ticker = filename.split('_')[0].upper()
        
        print(f"Processing {ticker:6s} from {filename}...")
        
        holdings = None
        if filename.endswith('.csv'):
            holdings = process_ishares_csv(filepath, enricher)
        elif filename.endswith('.xlsx'):
            holdings = process_statestreet_xlsx(filepath, enricher)
        elif filename.endswith('.json'):
            holdings = process_vanguard_json(filepath, enricher)
        
        if holdings:
            metadata = compute_fund_metadata(holdings, ticker)
            save_outputs(ticker, holdings, metadata)
            success_count += 1
        else:
            print(f"  ✗ Failed to extract holdings")
            failed_count += 1
    
    print(f"\n{'='*70}")
    print(f"PROCESSING COMPLETE")
    print(f"{'='*70}")
    print(f"Success: {success_count}")
    print(f"Failed:  {failed_count}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
