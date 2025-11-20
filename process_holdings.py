import os
import pandas as pd
import json
import glob

# Configuration
INPUT_DIR = 'data/holdings_files'
OUTPUT_DIR = 'data/holdings_json'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_ishares_csv(filepath):
    """Process iShares CSV format."""
    try:
        # iShares CSVs usually have a header, then data. 
        # Sometimes the header is on line 10.
        # We'll look for the line starting with "Ticker" or "Symbol".
        
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        header_row = 0
        for i, line in enumerate(lines):
            if line.startswith('Ticker') or line.startswith('Symbol'):
                header_row = i
                break
        
        df = pd.read_csv(filepath, skiprows=header_row)
        
        # Normalize columns
        # Expected: Ticker, Name, Sector, Weight (%)
        # Rename to standard: ticker, name, sector, weight, country
        
        # Handle weight column precedence
        weight_col = None
        if 'Weight (%)' in df.columns:
            weight_col = 'Weight (%)'
        elif 'Market Weight' in df.columns:
            weight_col = 'Market Weight'
        elif 'Notional Weight' in df.columns:
            weight_col = 'Notional Weight'
        elif 'Weight' in df.columns: # Sometimes just "Weight"
            weight_col = 'Weight'
            
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
            print(f"Skipping {filepath}: Missing required columns. Found: {df.columns}")
            return None
            
        # Clean data
        df['weight'] = pd.to_numeric(df['weight'], errors='coerce').fillna(0)
        
        # Handle missing sectors/countries
        if 'sector' not in df.columns:
            df['sector'] = 'Unknown'
        if 'country' not in df.columns:
            df['country'] = 'Unknown'
            
        # Select and order columns
        df = df[['ticker', 'name', 'sector', 'country', 'weight']]
        
        # Convert to list of dicts
        holdings = df.to_dict(orient='records')
        return holdings
        
    except Exception as e:
        print(f"Error processing iShares file {filepath}: {e}")
        return None

def process_statestreet_xlsx(filepath):
    """Process State Street XLSX format."""
    try:
        # State Street XLSX usually has header on line 5 or 6.
        # Look for 'Ticker' or 'Symbol'
        
        df = pd.read_excel(filepath)
        
        # Find header row
        header_row = -1
        for i, row in df.iterrows():
            # Check first few columns for "Ticker"
            row_str = row.astype(str).str.lower().tolist()
            if 'ticker' in row_str or 'symbol' in row_str:
                header_row = i
                break
        
        if header_row != -1:
            # Reload with correct header
            df = pd.read_excel(filepath, skiprows=header_row + 1)
        
        # Normalize columns
        # SSGA: Ticker, Name, Sector, Weight, Location
        # Sometimes: "Ticker", "Name", "Sector", "Weight"
        
        # Clean column names (strip whitespace, lower case)
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
             # Try to be flexible
             if 'ticker' not in df.columns and 'Identifier' in df.columns:
                 df['ticker'] = df['Identifier']
             
             if 'weight' not in df.columns:
                 # Maybe it's calculated? Or different name.
                 print(f"Skipping {filepath}: Missing required columns. Found: {df.columns}")
                 return None

        # Clean data
        df['weight'] = pd.to_numeric(df['weight'], errors='coerce').fillna(0)
        
        # SSGA weights might be decimal (0.05) or percent (5.0). 
        # Usually percent if it says "%".
        # Let's check max value. If max < 1, it's likely decimal.
        if df['weight'].max() < 1.05 and df['weight'].max() > 0:
             df['weight'] = df['weight'] * 100
             
        if 'sector' not in df.columns:
            df['sector'] = 'Unknown'
        if 'country' not in df.columns:
            df['country'] = 'Unknown'
            
        df = df[['ticker', 'name', 'sector', 'country', 'weight']]
        return df.to_dict(orient='records')

    except Exception as e:
        print(f"Error processing State Street file {filepath}: {e}")
        return None

def process_vanguard_json(filepath):
    """Process Vanguard JSON format from their API."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Extract holdings from the JSON structure
        # The API returns: {"fund": {"entity": [...]}}
        if 'fund' in data and 'entity' in data['fund']:
            raw_holdings = data['fund']['entity']
        else:
            print(f"Unexpected JSON structure in {filepath}")
            return None
        
        holdings = []
        for h in raw_holdings:
            # Extract relevant fields
            ticker = h.get('ticker', '').strip()
            name = h.get('longName', h.get('shortName', '')).strip()
            weight = h.get('percentWeight', h.get('weight', 0))
            
            # Skip if no ticker or name
            if not ticker or not name:
                continue
            
            # Convert weight to float
            try:
                weight = float(weight)
            except:
                weight = 0.0
            
            holdings.append({
                'ticker': ticker,
                'name': name,
                'sector': 'Unknown',  # Vanguard API doesn't provide sector in this endpoint
                'country': 'United States',  # Default assumption for most US-listed stocks
                'weight': weight
            })
        
        return holdings
        
    except Exception as e:
        print(f"Error processing Vanguard JSON file {filepath}: {e}")
        return None

def process_vanguard_csv(filepath):
    """Process Vanguard CSV format."""
    try:
        # Vanguard CSVs are tricky.
        # Usually: "Ticker","Name","Sector","Asset Class","Market Value","Weight (%)","Notional Value","Shares","Price","Location","Exchange","Currency","FX Rate","Market Currency"
        # Or similar.
        
        # Assume standard Vanguard export
        df = pd.read_csv(filepath, skiprows=10) # Often has header
        
        # Logic similar to iShares if format matches
        # ...
        return [] # Placeholder
    except Exception as e:
        return None

def main():
    files = glob.glob(os.path.join(INPUT_DIR, '*'))
    
    for filepath in files:
        filename = os.path.basename(filepath)
        ticker = filename.split('_')[0].upper()
        
        print(f"Processing {ticker} from {filename}...")
        
        holdings = None
        if filename.endswith('.csv'):
            # Check if iShares or Vanguard
            # Heuristic: iShares filenames usually don't have "Vanguard" in them :)
            # But we named them.
            # Let's try iShares processor first.
            holdings = process_ishares_csv(filepath)
            if not holdings:
                holdings = process_vanguard_csv(filepath)
        elif filename.endswith('.xlsx'):
            holdings = process_statestreet_xlsx(filepath)
        elif filename.endswith('.json'):
            holdings = process_vanguard_json(filepath)
            
        if holdings:
            # Save to JSON
            output_json = os.path.join(OUTPUT_DIR, f"{ticker}.json")
            with open(output_json, 'w') as f:
                json.dump(holdings, f, indent=2)
            
            # Save to JS (for local file access without server)
            # Create directory
            js_dir = 'data/holdings_js'
            os.makedirs(js_dir, exist_ok=True)
            output_js = os.path.join(js_dir, f"{ticker}.js")
            
            with open(output_js, 'w') as f:
                f.write(f"if (!window.ETF_HOLDINGS) window.ETF_HOLDINGS = {{}};\n")
                f.write(f"window.ETF_HOLDINGS['{ticker}'] = ")
                json.dump(holdings, f, indent=2)
                f.write(";\n")
                
            print(f"Saved {len(holdings)} holdings to {output_json} and {output_js}")
        else:
            print(f"Failed to extract holdings for {ticker}")

if __name__ == "__main__":
    main()
