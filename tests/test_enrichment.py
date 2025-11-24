#!/usr/bin/env python3
"""
Test suite for data enrichment quality.
Validates that enrichment process properly assigns sectors/countries.
"""

import json
import pytest
from pathlib import Path
from typing import Dict

class TestEnrichmentQuality:
    """Test suite for enriched holdings data quality."""
    
    @pytest.fixture
    def metadata_files(self):
        """Get all fund metadata files."""
        return list(Path('data/fund_metadata').glob('*.json'))
    
    @pytest.fixture
    def holdings_files(self):
        """Get all holdings JSON files."""
        return list(Path('data/holdings_json').glob('*.json'))
    
    def test_metadata_files_exist(self, metadata_files):
        """Test that metadata files were generated."""
        assert len(metadata_files) > 0, "No metadata files found"
        assert len(metadata_files) >= 40, f"Expected at least 40 metadata files, found {len(metadata_files)}"
    
    def test_metadata_structure(self, metadata_files):
        """Test that metadata files have correct structure."""
        for metadata_file in metadata_files:
            with open(metadata_file) as f:
                metadata = json.load(f)
            
            # Check required fields
            required_fields = [
                'ticker', 'holdings_count', 'total_weight',
                'sector_allocation', 'country_allocation',
                'sector_coverage_pct', 'country_coverage_pct'
            ]
            
            for field in required_fields:
                assert field in metadata, \
                    f"{metadata_file.name}: Missing field '{field}'"
    
    def test_sector_coverage_sufficient(self, metadata_files):
        """Test that sector coverage is above 95% for major funds."""
        major_funds = ['VOO', 'VTI', 'VXUS', 'VWO', 'IVV', 'SPY']
        
        for metadata_file in metadata_files:
            ticker = metadata_file.stem
            
            with open(metadata_file) as f:
                metadata = json.load(f)
            
            coverage = metadata.get('sector_coverage_pct', 0)
            
            if ticker in major_funds:
                assert coverage >= 95.0, \
                    f"{ticker}: Sector coverage is {coverage}%, expected >= 95%"
    
    def test_country_coverage_sufficient(self, metadata_files):
        """Test that country coverage is above 99% for all funds."""
        for metadata_file in metadata_files:
            ticker = metadata_file.stem
            
            with open(metadata_file) as f:
                metadata = json.load(f)
            
            coverage = metadata.get('country_coverage_pct', 0)
            
            assert coverage >= 99.0, \
                f"{ticker}: Country coverage is {coverage}%, expected >= 99%"
    
    def test_sector_allocations_sum_correctly(self, metadata_files):
        """Test that sector allocations sum to approximately 100%."""
        for metadata_file in metadata_files:
            ticker = metadata_file.stem
            
            with open(metadata_file) as f:
                metadata = json.load(f)
            
            sector_alloc = metadata.get('sector_allocation', {})
            total = sum(sector_alloc.values())
            
            # Should sum to close to total_weight
            expected_total = metadata.get('total_weight', 100)
            
            assert abs(total - expected_total) < 1.0, \
                f"{ticker}: Sector allocations sum to {total}%, expected {expected_total}%"
    
    def test_country_allocations_sum_correctly(self, metadata_files):
        """Test that country allocations sum to approximately 100%."""
        for metadata_file in metadata_files:
            ticker = metadata_file.stem
            
            with open(metadata_file) as f:
                metadata = json.load(f)
            
            country_alloc = metadata.get('country_allocation', {})
            total = sum(country_alloc.values())
            
            # Should sum to close to total_weight
            expected_total = metadata.get('total_weight', 100)
            
            assert abs(total - expected_total) < 1.0, \
                f"{ticker}: Country allocations sum to {total}%, expected {expected_total}%"
    
    def test_enriched_holdings_have_sectors(self, holdings_files):
        """Test that enriched holdings have valid sector assignments."""
        for holdings_file in holdings_files:
            ticker = holdings_file.stem
            
            with open(holdings_file) as f:
                holdings = json.load(f)
            
            # Count holdings with Unknown sector
            unknown_count = sum(1 for h in holdings if h.get('sector') == 'Unknown')
            unknown_pct = 100 * unknown_count / len(holdings)
            
            # Should be less than 5% Unknown for major US funds
            us_funds = ['VOO', 'VTI', 'SPY', 'IVV']
            if ticker in us_funds:
                assert unknown_pct < 5.0, \
                    f"{ticker}: {unknown_pct:.1f}% of holdings have unknown sectors (expected < 5%)"
    
    def test_major_holdings_enriched_correctly(self):
        """Test that major securities have correct sector assignments."""
        known_sectors = {
            'AAPL': 'Information Technology',
            'MSFT': 'Information Technology',
            'NVDA': 'Information Technology',
            'GOOGL': 'Communication Services',
            'AMZN': 'Consumer Discretionary',
            'TSLA': 'Consumer Discretionary',
            'META': 'Communication Services',
            'JPM': 'Financials',
            'JNJ': 'Health Care',
            'XOM': 'Energy'
        }
        
        holdings_files = list(Path('data/holdings_json').glob('*.json'))
        
        for holdings_file in holdings_files:
            with open(holdings_file) as f:
                holdings = json.load(f)
            
            for holding in holdings:
                ticker = holding.get('ticker')
                if ticker in known_sectors:
                    expected_sector = known_sectors[ticker]
                    actual_sector = holding.get('sector')
                    
                    assert actual_sector == expected_sector, \
                        f"{holdings_file.stem}: {ticker} has sector '{actual_sector}', expected '{expected_sector}'"
    
    def test_no_nan_sectors(self, holdings_files):
        """Test that no holdings have 'nan' as sector."""
        for holdings_file in holdings_files:
            with open(holdings_file) as f:
                holdings = json.load(f)
            
            nan_sectors = [h for h in holdings if str(h.get('sector')).lower() == 'nan']
            
            assert len(nan_sectors) == 0, \
                f"{holdings_file.name}: Found {len(nan_sectors)} holdings with 'nan' sector"
    
    def test_no_nan_countries(self, holdings_files):
        """Test that no holdings have 'nan' as country."""
        for holdings_file in holdings_files:
            with open(holdings_file) as f:
                holdings = json.load(f)
            
            nan_countries = [h for h in holdings if str(h.get('country')).lower() == 'nan']
            
            assert len(nan_countries) == 0, \
                f"{holdings_file.name}: Found {len(nan_countries)} holdings with 'nan' country"
    
    def test_sp500_funds_have_similar_sectors(self):
        """Test that S&P 500 funds have similar sector allocations."""
        sp500_funds = ['VOO', 'IVV', 'SPY']
        
        metadata = {}
        for ticker in sp500_funds:
            metadata_file = Path(f'data/fund_metadata/{ticker}.json')
            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata[ticker] = json.load(f)
        
        if len(metadata) < 2:
            pytest.skip("Need at least 2 S&P 500 funds for comparison")
        
        # Check that tech allocation is similar (within 5%)
        tech_allocations = [m['sector_allocation'].get('Information Technology', 0) 
                           for m in metadata.values()]
        
        max_tech = max(tech_allocations)
        min_tech = min(tech_allocations)
        
        assert max_tech - min_tech <= 5.0, \
            f"S&P 500 funds have divergent tech allocations: {tech_allocations}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
