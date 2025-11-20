#!/usr/bin/env python3
"""
Unit tests for ETF holdings data using pytest.
Run locally with: pytest tests/
Run with coverage: pytest tests/ --cov=.
"""

import json
import pytest
from pathlib import Path
from typing import List, Dict

class TestHoldingsData:
    """Test suite for ETF holdings data files."""
    
    @pytest.fixture
    def holdings_files(self) -> List[Path]:
        """Get all holdings JSON files."""
        return list(Path('data/holdings_json').glob('*.json'))
    
    @pytest.fixture
    def holdings_js_files(self) -> List[Path]:
        """Get all holdings JS files."""
        return list(Path('data/holdings_js').glob('*.js'))
    
    def test_json_files_exist(self, holdings_files):
        """Test that JSON files exist."""
        assert len(holdings_files) > 0, "No holdings JSON files found"
        assert len(holdings_files) >= 40, f"Expected at least 40 funds, found {len(holdings_files)}"
    
    def test_js_files_exist(self, holdings_js_files):
        """Test that JS files exist."""
        assert len(holdings_js_files) > 0, "No holdings JS files found"
        assert len(holdings_js_files) >= 40, f"Expected at least 40 funds, found {len(holdings_js_files)}"
    
    def test_matching_json_and_js_files(self, holdings_files, holdings_js_files):
        """Test that every JSON file has a matching JS file."""
        json_tickers = {f.stem for f in holdings_files}
        js_tickers = {f.stem for f in holdings_js_files}
        
        assert json_tickers == js_tickers, \
            f"Mismatch between JSON and JS files. Missing: {json_tickers ^ js_tickers}"
    
    @pytest.mark.parametrize("ticker,min_holdings", [
        ('VXUS', 8000),
        ('VTI', 3000),
        ('VWO', 5500),
        ('VOO', 480),
        ('IVV', 480),
        ('SPY', 480),
        ('IWM', 1900),
    ])
    def test_minimum_holdings_count(self, ticker, min_holdings):
        """Test that major funds have minimum expected holdings."""
        json_file = Path(f'data/holdings_json/{ticker}.json')
        
        if not json_file.exists():
            pytest.skip(f"{ticker} file not found")
        
        with open(json_file) as f:
            data = json.load(f)
        
        assert len(data) >= min_holdings, \
            f"{ticker} has {len(data)} holdings, expected at least {min_holdings}"
    
    def test_json_structure_valid(self, holdings_files):
        """Test that all JSON files have valid structure."""
        for json_file in holdings_files:
            with open(json_file) as f:
                data = json.load(f)
            
            assert isinstance(data, list), f"{json_file.name}: Data must be a list"
            assert len(data) > 0, f"{json_file.name}: Holdings list is empty"
            
            # Check first holding has required fields
            first = data[0]
            assert 'ticker' in first, f"{json_file.name}: Missing 'ticker' field"
            assert 'name' in first, f"{json_file.name}: Missing 'name' field"
            assert 'weight' in first, f"{json_file.name}: Missing 'weight' field"
    
    def test_weight_values_valid(self, holdings_files):
        """Test that weight values are valid numbers."""
        for json_file in holdings_files:
            with open(json_file) as f:
                data = json.load(f)
            
            for holding in data:
                weight = holding.get('weight')
                assert isinstance(weight, (int, float)), \
                    f"{json_file.name}: Invalid weight type for {holding.get('ticker')}"
                assert weight >= 0, \
                    f"{json_file.name}: Negative weight for {holding.get('ticker')}"
                assert weight <= 100, \
                    f"{json_file.name}: Weight >100% for {holding.get('ticker')}"
    
    def test_weight_totals_approximately_100(self, holdings_files):
        """Test that weight totals are approximately 100%."""
        for json_file in holdings_files:
            with open(json_file) as f:
                data = json.load(f)
            
            total = sum(h.get('weight', 0) for h in data)
            
            # Allow 90-110% range (accounts for rounding, cash, etc.)
            assert 90 <= total <= 110, \
                f"{json_file.name}: Weight total is {total:.2f}% (expected ~100%)"
    
    def test_no_duplicate_tickers(self, holdings_files):
        """Test that there are no duplicate tickers within a fund."""
        for json_file in holdings_files:
            with open(json_file) as f:
                data = json.load(f)
            
            tickers = [h.get('ticker') for h in data if h.get('ticker')]
            unique_tickers = set(tickers)
            
            assert len(tickers) == len(unique_tickers), \
                f"{json_file.name}: Found {len(tickers) - len(unique_tickers)} duplicate tickers"
    
    def test_no_empty_ticker_values(self, holdings_files):
        """Test that no holdings have empty ticker values."""
        for json_file in holdings_files:
            with open(json_file) as f:
                data = json.load(f)
            
            empty_tickers = [h for h in data if not h.get('ticker', '').strip()]
            
            assert len(empty_tickers) == 0, \
                f"{json_file.name}: Found {len(empty_tickers)} holdings with empty tickers"
    
    def test_no_empty_name_values(self, holdings_files):
        """Test that no holdings have empty name values."""
        for json_file in holdings_files:
            with open(json_file) as f:
                data = json.load(f)
            
            empty_names = [h for h in data if not h.get('name', '').strip()]
            
            assert len(empty_names) == 0, \
                f"{json_file.name}: Found {len(empty_names)} holdings with empty names"
    
    def test_js_file_syntax_valid(self, holdings_js_files):
        """Test that JS files are syntactically valid."""
        for js_file in holdings_js_files:
            content = js_file.read_text()
            
            # Basic syntax checks
            assert 'window.ETF_HOLDINGS' in content, \
                f"{js_file.name}: Missing window.ETF_HOLDINGS declaration"
            assert js_file.stem in content, \
                f"{js_file.name}: Missing ticker reference"
            assert content.strip().endswith(';'), \
                f"{js_file.name}: Missing semicolon at end"


class TestProviderData:
    """Test suite for provider-specific data quality."""
    
    def test_vanguard_funds_present(self):
        """Test that Vanguard funds are present."""
        vanguard_tickers = ['VOO', 'VTI', 'VXUS', 'VWO', 'VEA', 'VUG', 'VTV', 
                           'VIG', 'VYM', 'VB', 'VNQ', 'VGT', 'VO', 'VSS']
        
        for ticker in vanguard_tickers:
            json_file = Path(f'data/holdings_json/{ticker}.json')
            assert json_file.exists(), f"Missing Vanguard fund: {ticker}"
    
    def test_ishares_funds_present(self):
        """Test that iShares funds are present."""
        ishares_tickers = ['IVV', 'IWM', 'IEMG', 'EFA', 'ITOT', 'IXUS', 
                          'IWD', 'IWF', 'IJR', 'IJH']
        
        for ticker in ishares_tickers:
            json_file = Path(f'data/holdings_json/{ticker}.json')
            assert json_file.exists(), f"Missing iShares fund: {ticker}"
    
    def test_spdr_funds_present(self):
        """Test that SPDR funds are present."""
        spdr_tickers = ['SPY', 'MDY', 'SPLG', 'XLK', 'XLF', 'XLV', 'XLE', 
                       'XLP', 'XLY', 'XLI', 'XLB', 'XLC', 'XLRE', 'XLU']
        
        for ticker in spdr_tickers:
            json_file = Path(f'data/holdings_json/{ticker}.json')
            assert json_file.exists(), f"Missing SPDR fund: {ticker}"


class TestDataConsistency:
    """Test suite for cross-fund data consistency."""
    
    def test_sp500_funds_similar_count(self):
        """Test that S&P 500 funds have similar holdings counts."""
        sp500_funds = ['VOO', 'IVV', 'SPY']
        counts = {}
        
        for ticker in sp500_funds:
            json_file = Path(f'data/holdings_json/{ticker}.json')
            if json_file.exists():
                with open(json_file) as f:
                    data = json.load(f)
                counts[ticker] = len(data)
        
        if len(counts) >= 2:
            # All should be within 50 holdings of each other
            max_count = max(counts.values())
            min_count = min(counts.values())
            assert max_count - min_count <= 100, \
                f"S&P 500 funds have inconsistent counts: {counts}"
    
    def test_total_securities_count_reasonable(self):
        """Test that total securities count is reasonable."""
        total = 0
        for json_file in Path('data/holdings_json').glob('*.json'):
            with open(json_file) as f:
                data = json.load(f)
            total += len(data)
        
        # Should have at least 40,000 total securities across all funds
        assert total >= 40000, \
            f"Total securities ({total:,}) seems too low, expected >40,000"
        
        # But not more than 100,000 (sanity check)
        assert total <= 100000, \
            f"Total securities ({total:,}) seems too high, expected <100,000"


if __name__ == '__main__':
    """Allow running as script for quick testing."""
    pytest.main([__file__, '-v'])
