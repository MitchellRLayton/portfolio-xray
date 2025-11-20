#!/bin/bash

# Define funds
funds=(
    "SPY"
    "XLK"
    "XLF"
    "XLV"
    "XLE"
    "XLY"
    "XLI"
    "XLC"
    "XLP"
    "XLU"
    "XLB"
    "XLRE"
    "MDY"
    "SLY"
    "SPLG"
)

# Base URL
base_url="https://www.ssga.com/us/en/individual/etfs/library-content/products/fund-data/etfs/us/holdings-daily-us-en"

# Create directory if it doesn't exist
mkdir -p data/holdings_files

# Loop through funds and download
for ticker in "${funds[@]}"; do
    echo "Downloading $ticker..."
    # Convert ticker to lowercase for URL
    ticker_lower=$(echo "$ticker" | tr '[:upper:]' '[:lower:]')
    
    url="${base_url}-${ticker_lower}.xlsx"
    
    curl -L -o "data/holdings_files/${ticker}_holdings.xlsx" "$url"
    
    # Check if file is valid
    if grep -q "<html" "data/holdings_files/${ticker}_holdings.xlsx"; then
        echo "Error: Downloaded file for $ticker is HTML (likely 404)."
    fi
    
    echo "Done."
done
