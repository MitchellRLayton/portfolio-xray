#!/bin/bash

# Download Vanguard ETF holdings using their API with pagination support
# These are equity funds only

TICKERS=(
    "VOO"   # S&P 500
    "VTI"   # Total Stock Market
    "VUG"   # Growth
    "VTV"   # Value
    "VXUS"  # Total International
    "VIG"   # Dividend Appreciation
    "VYM"   # High Dividend Yield
    "VNQ"   # Real Estate
    "VGT"   # Information Technology
    "VWO"   # Emerging Markets
    "VEA"   # Developed Markets
    "VO"    # Mid-Cap
    "VSS"   # Small-Cap International
    "VB"    # Small-Cap
)

mkdir -p data/holdings_files

for ticker in "${TICKERS[@]}"; do
    ticker_lower=$(echo "$ticker" | tr '[:upper:]' '[:lower:]')
    base_url="https://investor.vanguard.com/investment-products/etfs/profile/api/${ticker_lower}/portfolio-holding/stock"
    output_file="data/holdings_files/${ticker}_holdings.json"
    temp_dir="data/holdings_files/${ticker}_temp"
    
    echo "Downloading $ticker with pagination..."
    rm -rf "$temp_dir"
    mkdir -p "$temp_dir"
    
    # Start with first page
    start=1
    page=1
    total_downloaded=0
    
    while true; do
        url="${base_url}?start=${start}&count=500"
        page_file="${temp_dir}/page_${page}.json"
        
        echo "  Fetching page $page (start=$start)..."
        curl -s "$url" -o "$page_file"
        
        if [ ! -s "$page_file" ]; then
            echo "  ✗ Failed to download page $page"
            break
        fi
        
        # Check if there's a next page
        has_next=$(grep -o '"next"' "$page_file" | wc -l)
        holdings_count=$(grep -o '"ticker"' "$page_file" | wc -l)
        total_downloaded=$((total_downloaded + holdings_count))
        
        echo "  ✓ Page $page: $holdings_count holdings (total: $total_downloaded)"
        
        if [ "$has_next" -eq 0 ]; then
            echo "  No more pages"
            break
        fi
        
        # Move to next page
        start=$((start + 500))
        page=$((page + 1))
        
        sleep 0.5  # Be polite to their server
    done
    
    # Merge all pages into one JSON file
    if [ $page -gt 1 ]; then
        echo "  Merging $page pages..."
        python3 -c "
import json
import glob
import os

# Read all page files
all_entities = []
fund_data = None

for page_file in sorted(glob.glob('${temp_dir}/page_*.json')):
    with open(page_file, 'r') as f:
        data = json.load(f)
        if fund_data is None:
            # Use first page structure
            fund_data = data
            fund_data.pop('next', None)  # Remove pagination links
            fund_data.pop('self', None)
        
        if 'fund' in data and 'entity' in data['fund']:
            all_entities.extend(data['fund']['entity'])

# Update with merged entities
fund_data['fund']['entity'] = all_entities
fund_data['size'] = len(all_entities)

# Save merged file
with open('${output_file}', 'w') as f:
    json.dump(fund_data, f, indent=2)

print(f'Merged {len(all_entities)} total holdings')
"
    else
        # Only one page, just copy it
        cp "${temp_dir}/page_1.json" "$output_file"
    fi
    
    # Cleanup temp files
    rm -rf "$temp_dir"
    
    if [ -s "$output_file" ]; then
        echo "✓ Successfully downloaded $ticker: $total_downloaded holdings"
    else
        echo "✗ Failed to download $ticker"
        rm -f "$output_file"
    fi
    
    echo ""
done

echo "Download complete!"

