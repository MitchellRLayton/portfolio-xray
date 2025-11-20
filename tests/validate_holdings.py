#!/usr/bin/env python3
"""
Comprehensive validation tests for ETF holdings data.
Ensures downloaded data meets quality standards before deployment.
"""

import json
import glob
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class HoldingsValidator:
    """Validates ETF holdings data for quality and completeness."""
    
    # Expected minimum holdings counts for major funds
    MINIMUM_HOLDINGS = {
        # Vanguard
        'VXUS': 8000,   # Total International
        'VTI': 3000,    # Total Stock Market
        'VWO': 5500,    # Emerging Markets
        'VEA': 3500,    # Developed Markets
        'VSS': 4500,    # Small-Cap International
        'VB': 1200,     # Small-Cap
        'VYM': 400,     # High Dividend
        'VOO': 480,     # S&P 500
        'VUG': 150,     # Growth
        'VTV': 300,     # Value
        'VIG': 300,     # Dividend Appreciation
        'VGT': 300,     # Tech
        'VNQ': 150,     # Real Estate
        'VO': 280,      # Mid-Cap
        
        # iShares
        'IVV': 480,     # S&P 500
        'IWM': 1900,    # Russell 2000
        'IEMG': 3000,   # Emerging Markets
        'EFA': 700,     # EAFE
        'ITOT': 2400,   # Total Market
        'IXUS': 4000,   # Total International
        'IWD': 800,     # Russell 1000 Value
        'IWF': 380,     # Russell 1000 Growth
        'IJR': 600,     # S&P Small-Cap
        'IJH': 400,     # S&P Mid-Cap
        
        # State Street (SPDR)
        'SPY': 480,     # S&P 500
        'MDY': 450,     # S&P Mid-Cap 400
        'SPLG': 480,    # S&P 500 Low Cost
        'XLK': 60,      # Tech
        'XLF': 60,      # Financials
        'XLV': 60,      # Healthcare
        'XLE': 20,      # Energy
        'XLP': 30,      # Consumer Staples
        'XLY': 50,      # Consumer Discretionary
        'XLI': 70,      # Industrials
        'XLB': 25,      # Materials
        'XLC': 20,      # Communications
        'XLRE': 30,     # Real Estate
        'XLU': 30,      # Utilities
    }
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.stats: Dict[str, int] = {}
        
    def validate_all(self) -> bool:
        """
        Run all validation tests.
        Returns True if all tests pass, False otherwise.
        """
        print(f"\n{Colors.BOLD}🔍 Validating ETF Holdings Data{Colors.END}\n")
        print("="*70)
        
        self.test_files_exist()
        self.test_data_structure()
        self.test_minimum_holdings()
        self.test_weight_totals()
        self.test_no_duplicates()
        self.test_data_freshness()
        self.collect_statistics()
        
        return self.report_results()
    
    def test_files_exist(self):
        """Verify all expected holdings files exist."""
        print("\n📁 Checking file existence...")
        
        for ticker in self.MINIMUM_HOLDINGS.keys():
            json_file = Path(f'data/holdings_json/{ticker}.json')
            js_file = Path(f'data/holdings_js/{ticker}.js')
            
            if not json_file.exists():
                self.errors.append(f"Missing JSON file for {ticker}")
            if not js_file.exists():
                self.errors.append(f"Missing JS file for {ticker}")
        
        if not self.errors:
            print(f"   {Colors.GREEN}✓{Colors.END} All expected files present")
    
    def test_data_structure(self):
        """Verify JSON structure is correct."""
        print("\n🔧 Validating data structure...")
        
        structure_errors = 0
        
        for json_file in glob.glob('data/holdings_json/*.json'):
            ticker = Path(json_file).stem
            
            try:
                with open(json_file) as f:
                    data = json.load(f)
                
                if not isinstance(data, list):
                    self.errors.append(f"{ticker}: Data is not a list")
                    structure_errors += 1
                    continue
                
                if len(data) == 0:
                    self.errors.append(f"{ticker}: Empty holdings list")
                    structure_errors += 1
                    continue
                
                # Check first holding has required fields
                first_holding = data[0]
                required_fields = ['ticker', 'name', 'weight']
                
                for field in required_fields:
                    if field not in first_holding:
                        self.errors.append(f"{ticker}: Missing '{field}' field")
                        structure_errors += 1
                
                # Check for valid weight values
                invalid_weights = [h for h in data if not isinstance(h.get('weight'), (int, float)) or h.get('weight', 0) < 0]
                if invalid_weights:
                    self.warnings.append(f"{ticker}: {len(invalid_weights)} holdings have invalid weights")
                        
            except json.JSONDecodeError as e:
                self.errors.append(f"{ticker}: Invalid JSON - {e}")
                structure_errors += 1
        
        if structure_errors == 0:
            print(f"   {Colors.GREEN}✓{Colors.END} All files have valid structure")
    
    def test_minimum_holdings(self):
        """Verify funds have reasonable number of holdings."""
        print("\n📊 Checking holdings counts...")
        
        count_errors = 0
        
        for ticker, min_count in self.MINIMUM_HOLDINGS.items():
            json_file = Path(f'data/holdings_json/{ticker}.json')
            
            if not json_file.exists():
                continue  # Already reported in file existence check
            
            with open(json_file) as f:
                data = json.load(f)
                count = len(data)
                
                if count < min_count:
                    self.errors.append(
                        f"{ticker}: Only {count} holdings (expected >{min_count})"
                    )
                    count_errors += 1
                elif count < min_count * 1.1:  # Within 10% of minimum
                    self.warnings.append(
                        f"{ticker}: {count} holdings (close to minimum of {min_count})"
                    )
        
        if count_errors == 0:
            print(f"   {Colors.GREEN}✓{Colors.END} All funds meet minimum holdings requirements")
    
    def test_weight_totals(self):
        """Verify weights sum to approximately 100%."""
        print("\n⚖️  Validating weight totals...")
        
        weight_errors = 0
        
        for json_file in glob.glob('data/holdings_json/*.json'):
            ticker = Path(json_file).stem
            
            with open(json_file) as f:
                data = json.load(f)
            
            total_weight = sum(h.get('weight', 0) for h in data)
            
            # Should be between 95% and 105% (some rounding/cash positions)
            if total_weight < 90 or total_weight > 110:
                self.errors.append(
                    f"{ticker}: Weights sum to {total_weight:.2f}% (expected ~100%)"
                )
                weight_errors += 1
            elif total_weight < 95 or total_weight > 105:
                self.warnings.append(
                    f"{ticker}: Weights sum to {total_weight:.2f}% (acceptable but unusual)"
                )
        
        if weight_errors == 0:
            print(f"   {Colors.GREEN}✓{Colors.END} All weight totals are valid")
    
    def test_no_duplicates(self):
        """Check for duplicate tickers within a fund."""
        print("\n🔍 Checking for duplicate holdings...")
        
        dup_errors = 0
        
        for json_file in glob.glob('data/holdings_json/*.json'):
            ticker = Path(json_file).stem
            
            with open(json_file) as f:
                data = json.load(f)
            
            tickers = [h.get('ticker', '') for h in data if h.get('ticker')]
            duplicates = set([t for t in tickers if tickers.count(t) > 1])
            
            if duplicates:
                self.errors.append(
                    f"{ticker}: {len(duplicates)} duplicate holdings: {', '.join(list(duplicates)[:3])}..."
                )
                dup_errors += 1
        
        if dup_errors == 0:
            print(f"   {Colors.GREEN}✓{Colors.END} No duplicate holdings found")
    
    def test_data_freshness(self):
        """Check if data files have been recently modified."""
        print("\n📅 Checking data freshness...")
        
        from datetime import datetime, timedelta
        
        stale_files = []
        
        for json_file in glob.glob('data/holdings_json/*.json'):
            mtime = datetime.fromtimestamp(Path(json_file).stat().st_mtime)
            age = datetime.now() - mtime
            
            if age > timedelta(days=45):  # Alert if >45 days old
                ticker = Path(json_file).stem
                self.warnings.append(
                    f"{ticker}: Data is {age.days} days old"
                )
                stale_files.append(ticker)
        
        if stale_files:
            print(f"   {Colors.YELLOW}⚠{Colors.END}  {len(stale_files)} funds have stale data (>45 days)")
        else:
            print(f"   {Colors.GREEN}✓{Colors.END} All data is fresh")
    
    def collect_statistics(self):
        """Collect overall statistics about holdings data."""
        print("\n📈 Collecting statistics...")
        
        total_files = 0
        total_holdings = 0
        
        for json_file in glob.glob('data/holdings_json/*.json'):
            total_files += 1
            with open(json_file) as f:
                data = json.load(f)
                total_holdings += len(data)
        
        self.stats = {
            'total_funds': total_files,
            'total_holdings': total_holdings,
            'avg_holdings': total_holdings // total_files if total_files > 0 else 0
        }
        
        print(f"   • Total funds: {self.stats['total_funds']}")
        print(f"   • Total holdings: {self.stats['total_holdings']:,}")
        print(f"   • Average holdings per fund: {self.stats['avg_holdings']}")
    
    def report_results(self) -> bool:
        """Print validation results and return success status."""
        print("\n" + "="*70)
        print(f"\n{Colors.BOLD}VALIDATION RESULTS{Colors.END}\n")
        
        if self.errors:
            print(f"{Colors.RED}{Colors.BOLD}❌ {len(self.errors)} CRITICAL ERROR(S):{Colors.END}")
            for error in self.errors:
                print(f"   • {error}")
            print()
        
        if self.warnings:
            print(f"{Colors.YELLOW}⚠️  {len(self.warnings)} WARNING(S):{Colors.END}")
            for warning in self.warnings:
                print(f"   • {warning}")
            print()
        
        if not self.errors and not self.warnings:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ ALL VALIDATIONS PASSED!{Colors.END}\n")
        elif not self.errors:
            print(f"{Colors.GREEN}✅ All critical validations passed{Colors.END}")
            print(f"{Colors.YELLOW}   (warnings can be safely ignored){Colors.END}\n")
        
        print("="*70 + "\n")
        
        # Return success if no critical errors
        success = len(self.errors) == 0
        
        if not success:
            sys.exit(1)
        
        return success

def main():
    """Main entry point."""
    validator = HoldingsValidator()
    validator.validate_all()

if __name__ == '__main__':
    main()
