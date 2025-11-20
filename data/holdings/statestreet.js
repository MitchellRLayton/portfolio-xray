registerFunds({
    'SPY': {
        ticker: 'SPY',
        name: 'SPDR S&P 500 ETF Trust',
        category: 'Large Blend',
        // Similar to VOO
        get top_holdings() { return window.ETF_DATABASE['VOO'].top_holdings; },
        get country_allocation() { return window.ETF_DATABASE['VOO'].country_allocation; },
        get sector_allocation() { return window.ETF_DATABASE['VOO'].sector_allocation; }
    },

    'GLD': {
        ticker: 'GLD',
        name: 'SPDR Gold Shares',
        category: 'Precious Metals',
        top_holdings: [
            { ticker: 'GOLD_BULLION', name: 'Gold Bullion', weight: 100, country: 'Global', sector: 'Basic Materials' }
        ],
        country_allocation: { 'Other': 100 },
        sector_allocation: { 'Basic Materials': 100 }
    },

    'XLK': {
        ticker: 'XLK',
        name: 'Technology Select Sector SPDR Fund',
        category: 'Technology',
        top_holdings: [
            { ticker: 'MSFT', name: 'Microsoft Corp.', weight: 22.5, country: 'United States', sector: 'Technology' },
            { ticker: 'AAPL', name: 'Apple Inc.', weight: 21.8, country: 'United States', sector: 'Technology' },
            { ticker: 'NVDA', name: 'NVIDIA Corp.', weight: 5.5, country: 'United States', sector: 'Technology' },
            { ticker: 'AVGO', name: 'Broadcom Inc.', weight: 4.8, country: 'United States', sector: 'Technology' },
            { ticker: 'CRM', name: 'Salesforce Inc.', weight: 2.8, country: 'United States', sector: 'Technology' },
            { ticker: 'AMD', name: 'Advanced Micro Devices Inc.', weight: 2.5, country: 'United States', sector: 'Technology' },
            { ticker: 'ADBE', name: 'Adobe Inc.', weight: 2.4, country: 'United States', sector: 'Technology' },
            { ticker: 'CSCO', name: 'Cisco Systems Inc.', weight: 2.1, country: 'United States', sector: 'Technology' },
            { ticker: 'ACN', name: 'Accenture PLC Class A', weight: 1.9, country: 'Ireland', sector: 'Technology' },
            { ticker: 'ORCL', name: 'Oracle Corp.', weight: 1.8, country: 'United States', sector: 'Technology' },
            { ticker: 'INTU', name: 'Intuit Inc.', weight: 1.7, country: 'United States', sector: 'Technology' },
            { ticker: 'IBM', name: 'International Business Machines Corp.', weight: 1.6, country: 'United States', sector: 'Technology' },
            { ticker: 'QCOM', name: 'QUALCOMM Inc.', weight: 1.6, country: 'United States', sector: 'Technology' },
            { ticker: 'TXN', name: 'Texas Instruments Inc.', weight: 1.5, country: 'United States', sector: 'Technology' },
            { ticker: 'AMAT', name: 'Applied Materials Inc.', weight: 1.4, country: 'United States', sector: 'Technology' },
            { ticker: 'NOW', name: 'ServiceNow Inc.', weight: 1.4, country: 'United States', sector: 'Technology' },
            { ticker: 'UBER', name: 'Uber Technologies Inc.', weight: 1.3, country: 'United States', sector: 'Technology' },
            { ticker: 'MU', name: 'Micron Technology Inc.', weight: 1.2, country: 'United States', sector: 'Technology' },
            { ticker: 'LRCX', name: 'Lam Research Corp.', weight: 1.1, country: 'United States', sector: 'Technology' },
            { ticker: 'ADI', name: 'Analog Devices Inc.', weight: 1.1, country: 'United States', sector: 'Technology' }
        ],
        country_allocation: { 'United States': 98.1, 'Ireland': 1.9 },
        sector_allocation: { 'Technology': 100 }
    },

    'XLF': {
        ticker: 'XLF',
        name: 'Financial Select Sector SPDR Fund',
        category: 'Financial',
        top_holdings: [
            { ticker: 'BRK.B', name: 'Berkshire Hathaway Inc. Class B', weight: 13.5, country: 'United States', sector: 'Financials' },
            { ticker: 'JPM', name: 'JPMorgan Chase & Co.', weight: 9.8, country: 'United States', sector: 'Financials' },
            { ticker: 'V', name: 'Visa Inc. Class A', weight: 7.5, country: 'United States', sector: 'Financials' },
            { ticker: 'MA', name: 'Mastercard Inc. Class A', weight: 6.2, country: 'United States', sector: 'Financials' },
            { ticker: 'BAC', name: 'Bank of America Corp.', weight: 3.8, country: 'United States', sector: 'Financials' },
            { ticker: 'WFC', name: 'Wells Fargo & Co.', weight: 3.5, country: 'United States', sector: 'Financials' },
            { ticker: 'GS', name: 'Goldman Sachs Group Inc.', weight: 2.8, country: 'United States', sector: 'Financials' },
            { ticker: 'SPGI', name: 'S&P Global Inc.', weight: 2.7, country: 'United States', sector: 'Financials' },
            { ticker: 'AXP', name: 'American Express Co.', weight: 2.5, country: 'United States', sector: 'Financials' },
            { ticker: 'MS', name: 'Morgan Stanley', weight: 2.2, country: 'United States', sector: 'Financials' },
            { ticker: 'BLK', name: 'BlackRock Inc.', weight: 2.1, country: 'United States', sector: 'Financials' },
            { ticker: 'C', name: 'Citigroup Inc.', weight: 2.0, country: 'United States', sector: 'Financials' },
            { ticker: 'PGR', name: 'Progressive Corp.', weight: 1.9, country: 'United States', sector: 'Financials' },
            { ticker: 'CB', name: 'Chubb Ltd.', weight: 1.8, country: 'Switzerland', sector: 'Financials' },
            { ticker: 'MMC', name: 'Marsh & McLennan Companies Inc.', weight: 1.7, country: 'United States', sector: 'Financials' },
            { ticker: 'SCHW', name: 'Charles Schwab Corp.', weight: 1.5, country: 'United States', sector: 'Financials' },
            { ticker: 'KKR', name: 'KKR & Co. Inc.', weight: 1.4, country: 'United States', sector: 'Financials' },
            { ticker: 'BX', name: 'Blackstone Inc.', weight: 1.3, country: 'United States', sector: 'Financials' },
            { ticker: 'AON', name: 'Aon PLC Class A', weight: 1.2, country: 'Ireland', sector: 'Financials' },
            { ticker: 'ICE', name: 'Intercontinental Exchange Inc.', weight: 1.2, country: 'United States', sector: 'Financials' }
        ],
        country_allocation: { 'United States': 97.0, 'Switzerland': 1.8, 'Ireland': 1.2 },
        sector_allocation: { 'Financials': 100 }
    },

    'SPYG': {
        ticker: 'SPYG',
        name: 'SPDR Portfolio S&P 500 Growth ETF',
        category: 'Large Growth',
        // Similar to VUG
        get top_holdings() { return window.ETF_DATABASE['VUG'].top_holdings; },
        get country_allocation() { return window.ETF_DATABASE['VUG'].country_allocation; },
        get sector_allocation() { return window.ETF_DATABASE['VUG'].sector_allocation; }
    },

    'BIL': {
        ticker: 'BIL',
        name: 'SPDR Bloomberg 1-3 Month T-Bill ETF',
        category: 'Ultrashort Bond',
        top_holdings: [
            { ticker: 'UST_BILL', name: 'United States Treasury Bill', weight: 100, country: 'United States', sector: 'Government' }
        ],
        country_allocation: { 'United States': 100 },
        sector_allocation: { 'Government': 100 }
    },

    'DIA': {
        ticker: 'DIA',
        name: 'SPDR Dow Jones Industrial Average ETF Trust',
        category: 'Large Value',
        top_holdings: [
            { ticker: 'UNH', name: 'UnitedHealth Group Inc.', weight: 8.5, country: 'United States', sector: 'Healthcare' },
            { ticker: 'GS', name: 'Goldman Sachs Group Inc.', weight: 7.2, country: 'United States', sector: 'Financials' },
            { ticker: 'MSFT', name: 'Microsoft Corp.', weight: 6.8, country: 'United States', sector: 'Technology' },
            { ticker: 'HD', name: 'Home Depot Inc.', weight: 6.1, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'CAT', name: 'Caterpillar Inc.', weight: 5.5, country: 'United States', sector: 'Industrials' },
            { ticker: 'AMGN', name: 'Amgen Inc.', weight: 4.8, country: 'United States', sector: 'Healthcare' },
            { ticker: 'V', name: 'Visa Inc. Class A', weight: 4.5, country: 'United States', sector: 'Financials' },
            { ticker: 'MCD', name: 'McDonald\'s Corp.', weight: 4.2, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'CRM', name: 'Salesforce Inc.', weight: 4.1, country: 'United States', sector: 'Technology' },
            { ticker: 'TRV', name: 'Travelers Companies Inc.', weight: 3.8, country: 'United States', sector: 'Financials' },
            { ticker: 'HON', name: 'Honeywell International Inc.', weight: 3.5, country: 'United States', sector: 'Industrials' },
            { ticker: 'AXP', name: 'American Express Co.', weight: 3.2, country: 'United States', sector: 'Financials' },
            { ticker: 'BA', name: 'Boeing Co.', weight: 3.1, country: 'United States', sector: 'Industrials' },
            { ticker: 'CVX', name: 'Chevron Corp.', weight: 3.0, country: 'United States', sector: 'Energy' },
            { ticker: 'JPM', name: 'JPMorgan Chase & Co.', weight: 2.9, country: 'United States', sector: 'Financials' },
            { ticker: 'IBM', name: 'International Business Machines Corp.', weight: 2.8, country: 'United States', sector: 'Technology' },
            { ticker: 'AAPL', name: 'Apple Inc.', weight: 2.7, country: 'United States', sector: 'Technology' },
            { ticker: 'JNJ', name: 'Johnson & Johnson', weight: 2.6, country: 'United States', sector: 'Healthcare' },
            { ticker: 'PG', name: 'Procter & Gamble Co.', weight: 2.5, country: 'United States', sector: 'Consumer Defensive' },
            { ticker: 'WMT', name: 'Walmart Inc.', weight: 2.4, country: 'United States', sector: 'Consumer Defensive' }
        ],
        country_allocation: { 'United States': 100 },
        sector_allocation: { 'Financials': 21.5, 'Healthcare': 18.2, 'Technology': 17.5, 'Industrials': 15.8, 'Consumer Cyclical': 12.5, 'Consumer Defensive': 7.5, 'Energy': 3.0, 'Communication Services': 2.5, 'Basic Materials': 1.5 }
    },

    'XLV': {
        ticker: 'XLV',
        name: 'Health Care Select Sector SPDR Fund',
        category: 'Health',
        top_holdings: [
            { ticker: 'LLY', name: 'Eli Lilly & Co.', weight: 11.5, country: 'United States', sector: 'Healthcare' },
            { ticker: 'UNH', name: 'UnitedHealth Group Inc.', weight: 9.2, country: 'United States', sector: 'Healthcare' },
            { ticker: 'JNJ', name: 'Johnson & Johnson', weight: 7.5, country: 'United States', sector: 'Healthcare' },
            { ticker: 'ABBV', name: 'AbbVie Inc.', weight: 6.8, country: 'United States', sector: 'Healthcare' },
            { ticker: 'MRK', name: 'Merck & Co. Inc.', weight: 6.2, country: 'United States', sector: 'Healthcare' },
            { ticker: 'TMO', name: 'Thermo Fisher Scientific Inc.', weight: 4.5, country: 'United States', sector: 'Healthcare' },
            { ticker: 'ABT', name: 'Abbott Laboratories', weight: 3.8, country: 'United States', sector: 'Healthcare' },
            { ticker: 'DHR', name: 'Danaher Corp.', weight: 3.2, country: 'United States', sector: 'Healthcare' },
            { ticker: 'PFE', name: 'Pfizer Inc.', weight: 3.1, country: 'United States', sector: 'Healthcare' },
            { ticker: 'AMGN', name: 'Amgen Inc.', weight: 3.0, country: 'United States', sector: 'Healthcare' },
            { ticker: 'ISRG', name: 'Intuitive Surgical Inc.', weight: 2.8, country: 'United States', sector: 'Healthcare' },
            { ticker: 'SYK', name: 'Stryker Corp.', weight: 2.5, country: 'United States', sector: 'Healthcare' },
            { ticker: 'ELV', name: 'Elevance Health Inc.', weight: 2.4, country: 'United States', sector: 'Healthcare' },
            { ticker: 'VRTX', name: 'Vertex Pharmaceuticals Inc.', weight: 2.2, country: 'United States', sector: 'Healthcare' },
            { ticker: 'REGN', name: 'Regeneron Pharmaceuticals Inc.', weight: 2.0, country: 'United States', sector: 'Healthcare' },
            { ticker: 'BSX', name: 'Boston Scientific Corp.', weight: 1.9, country: 'United States', sector: 'Healthcare' },
            { ticker: 'BMY', name: 'Bristol-Myers Squibb Co.', weight: 1.8, country: 'United States', sector: 'Healthcare' },
            { ticker: 'GILD', name: 'Gilead Sciences Inc.', weight: 1.7, country: 'United States', sector: 'Healthcare' },
            { ticker: 'ZTS', name: 'Zoetis Inc.', weight: 1.6, country: 'United States', sector: 'Healthcare' },
            { ticker: 'CVS', name: 'CVS Health Corp.', weight: 1.5, country: 'United States', sector: 'Healthcare' }
        ],
        country_allocation: { 'United States': 100 },
        sector_allocation: { 'Healthcare': 100 }
    },

    'SPDW': {
        ticker: 'SPDW',
        name: 'SPDR Portfolio Developed World ex-US ETF',
        category: 'Foreign Large Blend',
        // Similar to VEA
        get top_holdings() { return window.ETF_DATABASE['VEA'].top_holdings; },
        get country_allocation() { return window.ETF_DATABASE['VEA'].country_allocation; },
        get sector_allocation() { return window.ETF_DATABASE['VEA'].sector_allocation; }
    },

    'SPYV': {
        ticker: 'SPYV',
        name: 'SPDR Portfolio S&P 500 Value ETF',
        category: 'Large Value',
        // Similar to VTV
        get top_holdings() { return window.ETF_DATABASE['VTV'].top_holdings; },
        get country_allocation() { return window.ETF_DATABASE['VTV'].country_allocation; },
        get sector_allocation() { return window.ETF_DATABASE['VTV'].sector_allocation; }
    },

    'XLE': {
        ticker: 'XLE',
        name: 'Energy Select Sector SPDR Fund',
        category: 'Energy',
        top_holdings: [
            { ticker: 'XOM', name: 'Exxon Mobil Corp.', weight: 22.5, country: 'United States', sector: 'Energy' },
            { ticker: 'CVX', name: 'Chevron Corp.', weight: 18.2, country: 'United States', sector: 'Energy' },
            { ticker: 'EOG', name: 'EOG Resources Inc.', weight: 4.8, country: 'United States', sector: 'Energy' },
            { ticker: 'COP', name: 'ConocoPhillips', weight: 4.5, country: 'United States', sector: 'Energy' },
            { ticker: 'SLB', name: 'Schlumberger NV', weight: 4.2, country: 'United States', sector: 'Energy' },
            { ticker: 'MPC', name: 'Marathon Petroleum Corp.', weight: 3.8, country: 'United States', sector: 'Energy' },
            { ticker: 'PSX', name: 'Phillips 66', weight: 3.5, country: 'United States', sector: 'Energy' },
            { ticker: 'VLO', name: 'Valero Energy Corp.', weight: 3.2, country: 'United States', sector: 'Energy' },
            { ticker: 'OXY', name: 'Occidental Petroleum Corp.', weight: 2.8, country: 'United States', sector: 'Energy' },
            { ticker: 'WMB', name: 'Williams Companies Inc.', weight: 2.5, country: 'United States', sector: 'Energy' },
            { ticker: 'HES', name: 'Hess Corp.', weight: 2.4, country: 'United States', sector: 'Energy' },
            { ticker: 'KMI', name: 'Kinder Morgan Inc.', weight: 2.2, country: 'United States', sector: 'Energy' },
            { ticker: 'HAL', name: 'Halliburton Co.', weight: 2.1, country: 'United States', sector: 'Energy' },
            { ticker: 'BKR', name: 'Baker Hughes Co.', weight: 2.0, country: 'United States', sector: 'Energy' },
            { ticker: 'DVN', name: 'Devon Energy Corp.', weight: 1.8, country: 'United States', sector: 'Energy' },
            { ticker: 'TRGP', name: 'Targa Resources Corp.', weight: 1.7, country: 'United States', sector: 'Energy' },
            { ticker: 'FANG', name: 'Diamondback Energy Inc.', weight: 1.6, country: 'United States', sector: 'Energy' },
            { ticker: 'OKE', name: 'ONEOK Inc.', weight: 1.5, country: 'United States', sector: 'Energy' },
            { ticker: 'CTRA', name: 'Coterra Energy Inc.', weight: 1.4, country: 'United States', sector: 'Energy' },
            { ticker: 'MRO', name: 'Marathon Oil Corp.', weight: 1.3, country: 'United States', sector: 'Energy' }
        ],
        country_allocation: { 'United States': 100 },
        sector_allocation: { 'Energy': 100 }
    },

    'XLC': {
        ticker: 'XLC',
        name: 'Communication Services Select Sector SPDR Fund',
        category: 'Communications',
        top_holdings: [
            { ticker: 'META', name: 'Meta Platforms Inc.', weight: 22.5, country: 'United States', sector: 'Communication Services' },
            { ticker: 'GOOGL', name: 'Alphabet Inc. Class A', weight: 12.8, country: 'United States', sector: 'Communication Services' },
            { ticker: 'GOOG', name: 'Alphabet Inc. Class C', weight: 11.2, country: 'United States', sector: 'Communication Services' },
            { ticker: 'NFLX', name: 'Netflix Inc.', weight: 5.5, country: 'United States', sector: 'Communication Services' },
            { ticker: 'CMCSA', name: 'Comcast Corp. Class A', weight: 4.2, country: 'United States', sector: 'Communication Services' },
            { ticker: 'TMUS', name: 'T-Mobile US Inc.', weight: 3.8, country: 'United States', sector: 'Communication Services' },
            { ticker: 'DIS', name: 'Walt Disney Co.', weight: 3.5, country: 'United States', sector: 'Communication Services' },
            { ticker: 'VZ', name: 'Verizon Communications Inc.', weight: 3.2, country: 'United States', sector: 'Communication Services' },
            { ticker: 'T', name: 'AT&T Inc.', weight: 3.0, country: 'United States', sector: 'Communication Services' },
            { ticker: 'CHTR', name: 'Charter Communications Inc.', weight: 2.5, country: 'United States', sector: 'Communication Services' },
            { ticker: 'EA', name: 'Electronic Arts Inc.', weight: 1.8, country: 'United States', sector: 'Communication Services' },
            { ticker: 'TTWO', name: 'Take-Two Interactive Software Inc.', weight: 1.5, country: 'United States', sector: 'Communication Services' },
            { ticker: 'WBD', name: 'Warner Bros. Discovery Inc.', weight: 1.2, country: 'United States', sector: 'Communication Services' },
            { ticker: 'LYV', name: 'Live Nation Entertainment Inc.', weight: 1.1, country: 'United States', sector: 'Communication Services' },
            { ticker: 'OMC', name: 'Omnicom Group Inc.', weight: 1.0, country: 'United States', sector: 'Communication Services' },
            { ticker: 'IPG', name: 'Interpublic Group of Companies Inc.', weight: 0.9, country: 'United States', sector: 'Communication Services' },
            { ticker: 'FOXA', name: 'Fox Corp. Class A', weight: 0.8, country: 'United States', sector: 'Communication Services' },
            { ticker: 'FOX', name: 'Fox Corp. Class B', weight: 0.7, country: 'United States', sector: 'Communication Services' },
            { ticker: 'NWSA', name: 'News Corp. Class A', weight: 0.6, country: 'United States', sector: 'Communication Services' },
            { ticker: 'NWS', name: 'News Corp. Class B', weight: 0.5, country: 'United States', sector: 'Communication Services' }
        ],
        country_allocation: { 'United States': 100 },
        sector_allocation: { 'Communication Services': 100 }
    },

    'XLI': {
        ticker: 'XLI',
        name: 'Industrial Select Sector SPDR Fund',
        category: 'Industrials',
        top_holdings: [
            { ticker: 'CAT', name: 'Caterpillar Inc.', weight: 4.5, country: 'United States', sector: 'Industrials' },
            { ticker: 'GE', name: 'General Electric Co.', weight: 4.2, country: 'United States', sector: 'Industrials' },
            { ticker: 'UNP', name: 'Union Pacific Corp.', weight: 3.8, country: 'United States', sector: 'Industrials' },
            { ticker: 'HON', name: 'Honeywell International Inc.', weight: 3.5, country: 'United States', sector: 'Industrials' },
            { ticker: 'RTX', name: 'RTX Corp.', weight: 3.2, country: 'United States', sector: 'Industrials' },
            { ticker: 'BA', name: 'Boeing Co.', weight: 3.0, country: 'United States', sector: 'Industrials' },
            { ticker: 'ETN', name: 'Eaton Corp. PLC', weight: 2.8, country: 'Ireland', sector: 'Industrials' },
            { ticker: 'UBER', name: 'Uber Technologies Inc.', weight: 2.7, country: 'United States', sector: 'Industrials' },
            { ticker: 'DE', name: 'Deere & Co.', weight: 2.6, country: 'United States', sector: 'Industrials' },
            { ticker: 'ADP', name: 'Automatic Data Processing Inc.', weight: 2.5, country: 'United States', sector: 'Industrials' },
            { ticker: 'LMT', name: 'Lockheed Martin Corp.', weight: 2.4, country: 'United States', sector: 'Industrials' },
            { ticker: 'UPS', name: 'United Parcel Service Inc. Class B', weight: 2.2, country: 'United States', sector: 'Industrials' },
            { ticker: 'PCAR', name: 'PACCAR Inc.', weight: 2.0, country: 'United States', sector: 'Industrials' },
            { ticker: 'ITW', name: 'Illinois Tool Works Inc.', weight: 1.9, country: 'United States', sector: 'Industrials' },
            { ticker: 'PH', name: 'Parker-Hannifin Corp.', weight: 1.8, country: 'United States', sector: 'Industrials' },
            { ticker: 'TDG', name: 'TransDigm Group Inc.', weight: 1.7, country: 'United States', sector: 'Industrials' },
            { ticker: 'CSX', name: 'CSX Corp.', weight: 1.6, country: 'United States', sector: 'Industrials' },
            { ticker: 'GD', name: 'General Dynamics Corp.', weight: 1.5, country: 'United States', sector: 'Industrials' },
            { ticker: 'EMR', name: 'Emerson Electric Co.', weight: 1.4, country: 'United States', sector: 'Industrials' },
            { ticker: 'NSC', name: 'Norfolk Southern Corp.', weight: 1.3, country: 'United States', sector: 'Industrials' }
        ],
        country_allocation: { 'United States': 97.2, 'Ireland': 2.8 },
        sector_allocation: { 'Industrials': 100 }
    },

    'GLDM': {
        ticker: 'GLDM',
        name: 'SPDR Gold Minishares Trust',
        category: 'Precious Metals',
        // Same as GLD
        get top_holdings() { return window.ETF_DATABASE['GLD'].top_holdings; },
        get country_allocation() { return window.ETF_DATABASE['GLD'].country_allocation; },
        get sector_allocation() { return window.ETF_DATABASE['GLD'].sector_allocation; }
    },

    'XLY': {
        ticker: 'XLY',
        name: 'Consumer Discretionary Select Sector SPDR Fund',
        category: 'Consumer Cyclical',
        top_holdings: [
            { ticker: 'AMZN', name: 'Amazon.com Inc.', weight: 22.5, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'TSLA', name: 'Tesla Inc.', weight: 15.8, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'HD', name: 'Home Depot Inc.', weight: 9.5, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'MCD', name: 'McDonald\'s Corp.', weight: 4.8, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'NKE', name: 'NIKE Inc. Class B', weight: 3.5, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'LOW', name: 'Lowe\'s Companies Inc.', weight: 3.2, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'SBUX', name: 'Starbucks Corp.', weight: 2.8, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'BKNG', name: 'Booking Holdings Inc.', weight: 2.5, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'TJX', name: 'TJX Companies Inc.', weight: 2.2, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'CMG', name: 'Chipotle Mexican Grill Inc.', weight: 1.8, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'ORLY', name: 'O\'Reilly Automotive Inc.', weight: 1.5, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'MAR', name: 'Marriott International Inc. Class A', weight: 1.4, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'HLT', name: 'Hilton Worldwide Holdings Inc.', weight: 1.2, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'ROST', name: 'Ross Stores Inc.', weight: 1.1, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'F', name: 'Ford Motor Co.', weight: 1.0, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'GM', name: 'General Motors Co.', weight: 1.0, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'YUM', name: 'Yum! Brands Inc.', weight: 0.9, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'LEN', name: 'Lennar Corp. Class A', weight: 0.8, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'DHI', name: 'D.R. Horton Inc.', weight: 0.8, country: 'United States', sector: 'Consumer Cyclical' },
            { ticker: 'TSCO', name: 'Tractor Supply Co.', weight: 0.7, country: 'United States', sector: 'Consumer Cyclical' }
        ],
        country_allocation: { 'United States': 100 },
        sector_allocation: { 'Consumer Cyclical': 100 }
    }
});
