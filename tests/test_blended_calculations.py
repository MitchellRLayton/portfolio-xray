#!/usr/bin/env python3
"""
Test suite for blended portfolio calculations.
Validates that multi-fund portfolio calculations are mathematically correct.
"""

import json
import pytest
from pathlib import Path
from typing import Dict, List

# Import the analytics module (we'll need to create a Python version or test via browser)
# For now, we'll test the underlying math directly

class MockPortfolioAnalyzer:
    """Mock analyzer for testing calculation logic."""
    
    def __init__(self, portfolio: List[Dict]):
        self.portfolio = portfolio
        self.total_value = sum(h['value'] for h in portfolio)
        self.metadata = {}
        
        # Load metadata for each fund
        for holding in portfolio:
            ticker = holding['ticker']
            metadata_file = Path(f'data/fund_metadata/{ticker}.json')
            if metadata_file.exists():
                with open(metadata_file) as f:
                    self.metadata[ticker] = json.load(f)
    
    def calculate_blended_sector_allocation(self) -> Dict[str, float]:
        """Calculate blended sector allocation across portfolio."""
        sector_map = {}
        
        for holding in self.portfolio:
            ticker = holding['ticker']
            value = holding['value']
            weight = value / self.total_value
            
            if ticker not in self.metadata:
                continue
            
            sector_alloc = self.metadata[ticker]['sector_allocation']
            
            for sector, percentage in sector_alloc.items():
                if sector not in sector_map:
                    sector_map[sector] = 0.0
                
                # Weighted blend
                sector_map[sector] += (percentage * weight)
        
        return sector_map
    
    def calculate_blended_country_allocation(self) -> Dict[str, float]:
        """Calculate blended country allocation across portfolio."""
        country_map = {}
        
        for holding in self.portfolio:
            ticker = holding['ticker']
            value = holding['value']
            weight = value / self.total_value
            
            if ticker not in self.metadata:
                continue
            
            country_alloc = self.metadata[ticker]['country_allocation']
            
            for country, percentage in country_alloc.items():
                if country not in country_map:
                    country_map[country] = 0.0
                
                country_map[country] += (percentage * weight)
        
        return country_map


class TestBlendedCalculations:
    """Test suite for blended portfolio calculations."""
    
    def test_single_fund_passthrough(self):
        """Test that single-fund portfolio passes through allocations correctly."""
        portfolio = [
            {'ticker': 'VOO', 'value': 10000}
        ]
        
        analyzer = MockPortfolioAnalyzer(portfolio)
        sectors = analyzer.calculate_blended_sector_allocation()
        
        # Load expected
        with open('data/fund_metadata/VOO.json') as f:
            expected = json.load(f)['sector_allocation']
        
        # Should match exactly (within rounding)
        for sector, expected_pct in expected.items():
            actual_pct = sectors.get(sector, 0.0)
            assert abs(actual_pct - expected_pct) < 0.01, \
                f"{sector}: Expected {expected_pct}%, got {actual_pct}%"
    
    def test_50_50_blend_voo_vti(self):
        """Test 50/50 blend of VOO + VTI."""
        portfolio = [
            {'ticker': 'VOO', 'value': 10000},
            {'ticker': 'VTI', 'value': 10000}
        ]
        
        analyzer = MockPortfolioAnalyzer(portfolio)
        sectors = analyzer.calculate_blended_sector_allocation()
        
        # Load metadata
        with open('data/fund_metadata/VOO.json') as f:
            voo = json.load(f)
        with open('data/fund_metadata/VTI.json') as f:
            vti = json.load(f)
        
        # Test tech allocation
        voo_tech = voo['sector_allocation']['Information Technology']
        vti_tech = vti['sector_allocation']['Information Technology']
        
        expected_tech = (voo_tech * 0.5) + (vti_tech * 0.5)
        actual_tech= sectors['Information Technology']
        
        assert abs(actual_tech - expected_tech) < 0.1, \
            f"Tech blend: Expected {expected_tech}%, got {actual_tech}%"
    
    def test_weighted_blend_60_40(self):
        """Test 60/40 weighted blend."""
        portfolio = [
            {'ticker': 'VOO', 'value': 60000},  # 60%
            {'ticker': 'VTI', 'value': 40000}   # 40%
        ]
        
        analyzer = MockPortfolioAnalyzer(portfolio)
        sectors = analyzer.calculate_blended_sector_allocation()
        
        # Load metadata
        with open('data/fund_metadata/VOO.json') as f:
            voo = json.load(f)
        with open('data/fund_metadata/VTI.json') as f:
            vti = json.load(f)
        
        # Test multiple sectors
        for sector in ['Information Technology', 'Financials', 'Health Care']:
            voo_pct = voo['sector_allocation'].get(sector, 0)
            vti_pct = vti['sector_allocation'].get(sector, 0)
            
            expected = (voo_pct * 0.6) + (vti_pct * 0.4)
            actual = sectors.get(sector, 0)
            
            assert abs(actual - expected) < 0.1, \
                f"{sector}: Expected {expected}%, got {actual}%"
    
    def test_total_allocation_sums_to_100(self):
        """Test that blended allocations sum to approximately 100%."""
        portfolio = [
            {'ticker': 'VOO', 'value': 10000},
            {'ticker': 'VTI', 'value': 10000}
        ]
        
        analyzer = MockPortfolioAnalyzer(portfolio)
        sectors = analyzer.calculate_blended_sector_allocation()
        
        total = sum(sectors.values())
        
        # Should be close to 100% (within 5% for rounding/missing data)
        assert 95 <= total <= 105, \
            f"Sector allocations sum to {total}%, expected ~100%"
    
    def test_country_blend_us_international(self):
        """Test blending US and international funds."""
        portfolio = [
            {'ticker': 'VTI', 'value': 60000},   # ~96% US
            {'ticker': 'VXUS', 'value': 40000}   # ~0% US (all international)
        ]
        
        analyzer = MockPortfolioAnalyzer(portfolio)
        countries = analyzer.calculate_blended_country_allocation()
        
        # Load metadata
        with open('data/fund_metadata/VTI.json') as f:
            vti = json.load(f)
        with open('data/fund_metadata/VXUS.json') as f:
            vxus = json.load(f)
        
        vti_us = vti['country_allocation'].get('United States', 0)
        vxus_us = vxus['country_allocation'].get('United States', 0)
        
        expected_us = (vti_us * 0.6) + (vxus_us * 0.4)
        actual_us = countries.get('United States', 0)
        
        # Should be around 57.6% (96% × 0.6 + 0% × 0.4)
        assert abs(actual_us - expected_us) < 1.0, \
            f"US allocation: Expected {expected_us}%, got {actual_us}%"
    
    def test_multi_fund_complex_portfolio(self):
        """Test more complex multi-fund portfolio."""
        portfolio = [
            {'ticker': 'VOO', 'value': 40000},    # Large-cap
            {'ticker': 'VB', 'value': 20000},     # Small-cap
            {'ticker': 'VEA', 'value': 30000},    # International developed
            {'ticker': 'VWO', 'value': 10000}     # Emerging markets
        ]
        
        analyzer = MockPortfolioAnalyzer(portfolio)
        sectors = analyzer.calculate_blended_sector_allocation()
        countries = analyzer.calculate_blended_country_allocation()
        
        # Verify totals
        sector_total = sum(sectors.values())
        country_total = sum(countries.values())
        
        assert 90 <= sector_total <= 105, f"Sectors sum to {sector_total}%"
        assert 90 <= country_total <= 105, f"Countries sum to {country_total}%"
        
        # US allocation should be dominated by VOO + VB
        us_pct = countries.get('United States', 0)
        assert 40 <= us_pct <= 70, f"US allocation {us_pct}% seems wrong"
    
    def test_edge_case_tiny_allocation(self):
        """Test handling of very small allocations."""
        portfolio = [
            {'ticker': 'VOO', 'value': 99000},
            {'ticker': 'VTI', 'value': 1000}      # Only 1%
        ]
        
        analyzer = MockPortfolioAnalyzer(portfolio)
        sectors = analyzer.calculate_blended_sector_allocation()
        
        # Should still work correctly
        total = sum(sectors.values())
        assert 95 <= total <= 105
    
    def test_deterministic_calculation(self):
        """Test that calculations are deterministic (same input = same output)."""
        portfolio = [
            {'ticker': 'VOO', 'value': 10000},
            {'ticker': 'VTI', 'value': 10000}
        ]
        
        analyzer1 = MockPortfolioAnalyzer(portfolio)
        sectors1 = analyzer1.calculate_blended_sector_allocation()
        
        analyzer2 = MockPortfolioAnalyzer(portfolio)
        sectors2 = analyzer2.calculate_blended_sector_allocation()
        
        # Should be identical
        assert sectors1 == sectors2, "Calculations not deterministic!"


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_missing_metadata_graceful_handling(self):
        """Test that missing metadata is handled gracefully."""
        portfolio = [
            {'ticker': 'VOO', 'value': 10000},
            {'ticker': 'FAKE', 'value': 10000}  # Doesn't exist
        ]
        
        analyzer = MockPortfolioAnalyzer(portfolio)
        sectors = analyzer.calculate_blended_sector_allocation()
        
        # Should still work with  available data
        assert len(sectors) > 0
    
    def test_zero_weight_handling(self):
        """Test that zero-weight holdings don't cause errors."""
        portfolio = [
            {'ticker': 'VOO', 'value': 10000},
            {'ticker': 'VTI', 'value': 0}
        ]
        
        analyzer = MockPortfolioAnalyzer(portfolio)
        sectors = analyzer.calculate_blended_sector_allocation()
        
        # Should work (VTI has 0% weight)
        assert len(sectors) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
