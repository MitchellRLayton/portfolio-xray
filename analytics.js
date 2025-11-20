// Portfolio Analytics Engine
// Calculates aggregated allocations and individual holdings

class PortfolioAnalyzer {
    constructor(portfolio) {
        this.portfolio = portfolio; // Array of { ticker, shares, account }
        this.totalValue = 0;
        this.etfData = [];
    }

    // Load ETF data for all holdings
    loadETFData() {
        this.etfData = this.portfolio.map(holding => {
            const etf = getETFData(holding.ticker);
            if (!etf) {
                console.warn(`ETF data not found for ${holding.ticker}`);
                return null;
            }
            return {
                ...holding,
                etfInfo: etf,
                // Use provided value or calculate from shares (assuming $100/share for demo)
                value: holding.value || (holding.shares * 100)
            };
        }).filter(Boolean);

        this.totalValue = this.etfData.reduce((sum, h) => sum + h.value, 0);
    }

    // Calculate weighted country allocation across all holdings
    calculateCountryAllocation() {
        const countryMap = {};

        this.etfData.forEach(holding => {
            const weight = holding.value / this.totalValue;
            const countryAlloc = holding.etfInfo.country_allocation;

            Object.entries(countryAlloc).forEach(([country, percentage]) => {
                if (!countryMap[country]) {
                    countryMap[country] = 0;
                }
                countryMap[country] += (percentage * weight);
            });
        });

        // Sort by allocation descending
        return Object.entries(countryMap)
            .sort((a, b) => b[1] - a[1])
            .map(([country, allocation]) => ({
                country,
                allocation: parseFloat(allocation.toFixed(2))
            }));
    }

    // Calculate weighted sector allocation across all holdings
    calculateSectorAllocation() {
        const sectorMap = {};

        this.etfData.forEach(holding => {
            const weight = holding.value / this.totalValue;
            const sectorAlloc = holding.etfInfo.sector_allocation;

            Object.entries(sectorAlloc).forEach(([sector, percentage]) => {
                if (!sectorMap[sector]) {
                    sectorMap[sector] = 0;
                }
                sectorMap[sector] += (percentage * weight);
            });
        });

        // Sort by allocation descending
        return Object.entries(sectorMap)
            .sort((a, b) => b[1] - a[1])
            .map(([sector, allocation]) => ({
                sector,
                allocation: parseFloat(allocation.toFixed(2))
            }));
    }

    // Get all individual securities with aggregated weights
    getIndividualHoldings() {
        const securitiesMap = {};

        this.etfData.forEach(holding => {
            const weight = holding.value / this.totalValue;
            // Use full holdings if available, otherwise top_holdings
            const holdingsList = holding.etfInfo.holdings || holding.etfInfo.top_holdings;

            holdingsList.forEach(security => {
                const key = security.ticker;

                if (!securitiesMap[key]) {
                    securitiesMap[key] = {
                        ticker: security.ticker,
                        name: security.name,
                        country: security.country,
                        sector: security.sector,
                        weight: 0,
                        value: 0,
                        sources: [] // Track which ETFs contain this security
                    };
                }

                const contributedWeight = security.weight * weight;
                securitiesMap[key].weight += contributedWeight;
                securitiesMap[key].value += (this.totalValue * contributedWeight / 100);
                securitiesMap[key].sources.push({
                    etf: holding.ticker,
                    weight: security.weight
                });
            });
        });

        // Sort by weight descending and format
        return Object.values(securitiesMap)
            .sort((a, b) => b.weight - a.weight)
            .map(security => ({
                ...security,
                weight: parseFloat(security.weight.toFixed(2)),
                value: parseFloat(security.value.toFixed(2))
            }));
    }

    // Detect overlapping holdings (securities held in multiple ETFs)
    detectOverlaps() {
        const holdings = this.getIndividualHoldings();
        return holdings.filter(h => h.sources.length > 1);
    }

    // Generate complete analysis
    analyze() {
        this.loadETFData();

        return {
            totalValue: this.totalValue,
            countryAllocation: this.calculateCountryAllocation(),
            sectorAllocation: this.calculateSectorAllocation(),
            individualHoldings: this.getIndividualHoldings(),
            overlaps: this.detectOverlaps(),
            summary: {
                totalETFs: this.etfData.length,
                totalSecurities: this.getIndividualHoldings().length,
                overlapCount: this.detectOverlaps().length
            }
        };
    }
}

// Export for use in app.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PortfolioAnalyzer;
}
