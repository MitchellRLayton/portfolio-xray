#!/bin/bash

# Define funds and their IDs as a string list "TICKER:ID"
funds=(
    "IVV:239726"
    "ITOT:239724"
    "IWF:239706"
    "IWD:239708"
    "IEMG:244050"
    "EFA:239623"
    "IXUS:244048"
    "USMV:239695"
    "IJH:239763"
    "IJR:239774"
    "IWM:239710"
    "QUAL:256101"
    "MTUM:251614"
    "VLUE:251616"
    "LRGF:272824"
)

# Base URL for iShares CSV download
base_url="https://www.ishares.com/us/products"

# Create directory if it doesn't exist
mkdir -p data/holdings_files

# Loop through funds and download
for item in "${funds[@]}"; do
    ticker="${item%%:*}"
    id="${item##*:}"
    echo "Downloading $ticker (ID: $id)..."
    
    # Construct URL with generic slug first
    url="${base_url}/${id}/fund/1467271812596.ajax?fileType=csv&fileName=${ticker}_holdings&dataType=fund"
    
    # Try downloading
    curl -L -o "data/holdings_files/${ticker}_holdings.csv" "$url"
    
    # Check if file is valid (not HTML)
    if grep -q "<html" "data/holdings_files/${ticker}_holdings.csv"; then
        echo "Error: Downloaded file for $ticker is HTML (likely 404). Trying to find correct slug..."
        # Extract slug from product_links.txt
        slug=$(grep "/products/$id/" product_links.txt | head -n 1 | sed -E 's/.*\/products\/[0-9]+\/([^"]+).*/\1/')
        echo "Found slug: $slug"
        if [ -n "$slug" ]; then
            url="${base_url}/${id}/${slug}/1467271812596.ajax?fileType=csv&fileName=${ticker}_holdings&dataType=fund"
            curl -L -o "data/holdings_files/${ticker}_holdings.csv" "$url"
        else
            echo "Could not find slug for $ticker. Download failed."
        fi
    fi
    
    echo "Done."
done
