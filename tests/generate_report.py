#!/usr/bin/env python3
"""
Generate a comprehensive holdings report for documentation.
"""

import json
import glob
from pathlib import Path
from datetime import datetime
from typing import Dict, List

def generate_report() -> str:
    """Generate markdown report of all holdings data."""
    
    report_lines = [
        "# ETF Holdings Data Report",
        f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "\n## Summary\n",
    ]
    
    # Collect data
    holdings_data: List[Dict] = []
    total_holdings = 0
    
    for json_file in sorted(glob.glob('data/holdings_json/*.json')):
        ticker = Path(json_file).stem
        
        with open(json_file) as f:
            data = json.load(f)
        
        count = len(data)
        total_weight = sum(h.get('weight', 0) for h in data)
        
        holdings_data.append({
            'ticker': ticker,
            'count': count,
            'weight_total': total_weight
        })
        
        total_holdings += count
    
    # Summary statistics
    report_lines.extend([
        f"- **Total Funds**: {len(holdings_data)}",
        f"- **Total Securities**: {total_holdings:,}",
        f"- **Average Holdings per Fund**: {total_holdings // len(holdings_data) if holdings_data else 0}",
        "\n## Holdings by Fund\n",
        "| Ticker | Holdings | Weight Total | Status |",
        "|--------|----------|--------------|--------|"
    ])
    
    # Sort by holdings count (descending)
    holdings_data.sort(key=lambda x: x['count'], reverse=True)
    
    for fund in holdings_data:
        ticker = fund['ticker']
        count = fund['count']
        weight = fund['weight_total']
        
        # Determine status
        if 95 <= weight <= 105:
            status = "✅"
        elif 90 <= weight <= 110:
            status = "⚠️"
        else:
            status = "❌"
        
        report_lines.append(
            f"| {ticker} | {count:,} | {weight:.2f}% | {status} |"
        )
    
    # Provider breakdown
    vanguard = [h for h in holdings_data if h['ticker'].startswith('V')]
    ishares = [h for h in holdings_data if h['ticker'].startswith('I')]
    spdr = [h for h in holdings_data if h['ticker'].startswith(('X', 'S', 'M'))]
    
    report_lines.extend([
        "\n## Provider Breakdown\n",
        f"- **Vanguard**: {len(vanguard)} funds, {sum(h['count'] for h in vanguard):,} total holdings",
        f"- **iShares**: {len(ishares)} funds, {sum(h['count'] for h in ishares):,} total holdings",
        f"- **State Street (SPDR)**: {len(spdr)} funds, {sum(h['count'] for h in spdr):,} total holdings",
        "\n## Data Quality\n",
        f"- Funds with valid weight totals (95-105%): {sum(1 for h in holdings_data if 95 <= h['weight_total'] <= 105)}",
        f"- Funds with acceptable weight totals (90-110%): {sum(1 for h in holdings_data if 90 <= h['weight_total'] <= 110)}",
        f"- Funds requiring review: {sum(1 for h in holdings_data if h['weight_total'] < 90 or h['weight_total'] > 110)}",
        "\n---\n",
        "*This report is automatically generated during the holdings update process.*"
    ])
    
    return "\n".join(report_lines)

def main():
    """Print the report to stdout."""
    print(generate_report())

if __name__ == '__main__':
    main()
