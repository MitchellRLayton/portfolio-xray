// Portfolio X-Ray - Application Logic

class PortfolioApp {
  constructor() {
    this.portfolio = [];
    this.analysis = null;
    this.inputMode = 'dollars'; // 'dollars' or 'shares'
    this.init();
  }

  init() {
    this.loadFromLocalStorage();
    this.setupEventListeners();
    this.renderPortfolio();
    this.populateTickerDatalist();
    this.setInputMode('dollars'); // Set default mode
  }

  // Setup event listeners
  setupEventListeners() {
    const addBtn = document.getElementById('add-holding-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const clearBtn = document.getElementById('clear-all-btn');
    const modeDollarsBtn = document.getElementById('mode-dollars');
    const modeSharesBtn = document.getElementById('mode-shares');

    addBtn.addEventListener('click', () => this.addHolding());
    analyzeBtn.addEventListener('click', () => this.analyzePortfolio());
    clearBtn.addEventListener('click', () => this.clearAll());
    modeDollarsBtn.addEventListener('click', () => this.setInputMode('dollars'));
    modeSharesBtn.addEventListener('click', () => this.setInputMode('shares'));

    // Allow Enter key to add holding
    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(input => {
      input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.addHolding();
        }
      });
    });
  }

  // Populate ticker datalist with available ETFs
  populateTickerDatalist() {
    const datalist = document.getElementById('ticker-list');
    const tickers = getAvailableTickers();

    datalist.innerHTML = tickers.map(ticker => {
      const etf = getETFData(ticker);
      return `<option value="${ticker}">${etf.name}</option>`;
    }).join('');
  }

  // Set input mode (dollars or shares)
  setInputMode(mode) {
    this.inputMode = mode;

    // Update buttons
    document.getElementById('mode-dollars').className = `toggle-btn ${mode === 'dollars' ? 'active' : ''}`;
    document.getElementById('mode-shares').className = `toggle-btn ${mode === 'shares' ? 'active' : ''}`;

    // Update label and placeholder
    const label = document.getElementById('amount-label');
    const input = document.getElementById('amount-input');

    if (mode === 'dollars') {
      label.textContent = 'Amount ($)';
      input.placeholder = '10000';
    } else {
      label.textContent = 'Shares';
      input.placeholder = '100';
    }

    input.focus();
  }

  // Add a new holding
  addHolding() {
    const tickerInput = document.getElementById('ticker-input');
    const amountInput = document.getElementById('amount-input');
    const accountSelect = document.getElementById('account-select');

    const ticker = tickerInput.value.trim().toUpperCase();
    const amount = parseFloat(amountInput.value);
    const account = accountSelect.value;

    // Validation
    if (!ticker) {
      alert('Please enter a ticker symbol');
      return;
    }

    if (!amount || amount <= 0) {
      alert('Please enter a valid amount');
      return;
    }

    const etfData = getETFData(ticker);
    if (!etfData) {
      alert(`ETF data not found for ${ticker}. Available ETFs: ${getAvailableTickers().join(', ')}`);
      return;
    }

    // Calculate value and shares based on mode
    // For demo purposes, we assume $100/share price
    const PRICE_PER_SHARE = 100;
    let value, shares;

    if (this.inputMode === 'dollars') {
      value = amount;
      shares = amount / PRICE_PER_SHARE;
    } else {
      shares = amount;
      value = amount * PRICE_PER_SHARE;
    }

    // Add to portfolio
    this.portfolio.push({
      ticker,
      shares,
      value,
      account,
      name: etfData.name,
      inputMode: this.inputMode // Track how it was entered
    });

    // Clear inputs
    tickerInput.value = '';
    amountInput.value = '';

    // Save and render
    this.saveToLocalStorage();
    this.renderPortfolio();

    // Focus back on ticker input
    tickerInput.focus();
  }

  // Remove a holding
  removeHolding(index) {
    this.portfolio.splice(index, 1);
    this.saveToLocalStorage();
    this.renderPortfolio();

    // Clear analysis if portfolio is empty
    if (this.portfolio.length === 0) {
      this.clearAnalysis();
    }
  }

  // Clear all holdings
  clearAll() {
    // Directly clear without confirmation as requested
    this.portfolio = [];
    this.saveToLocalStorage();
    this.renderPortfolio();
    this.clearAnalysis();
  }

  // Render portfolio holdings
  renderPortfolio() {
    const container = document.getElementById('holdings-list');

    if (this.portfolio.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">📊</div>
          <div class="empty-state-title">No Holdings Yet</div>
          <div class="empty-state-description">Add your first ETF or mutual fund to get started</div>
        </div>
      `;
      return;
    }

    container.innerHTML = this.portfolio.map((holding, index) => `
      <div class="holding-item fade-in">
        <div class="holding-info">
          <div class="holding-ticker">${holding.ticker}</div>
          <div class="holding-name">${holding.name}</div>
        </div>
        <div class="holding-details">
          <span>${holding.inputMode === 'dollars'
        ? `$${holding.value.toLocaleString()}`
        : `${holding.shares.toLocaleString()} shares`}</span>
          <span class="holding-badge">${holding.account}</span>
          <button class="btn btn-danger" onclick="app.removeHolding(${index})">Remove</button>
        </div>
      </div>
    `).join('');
  }

  // Analyze portfolio
  analyzePortfolio() {
    if (this.portfolio.length === 0) {
      alert('Please add at least one holding to analyze');
      return;
    }

    const analyzer = new PortfolioAnalyzer(this.portfolio);
    this.analysis = analyzer.analyze();

    this.renderAnalysis();

    // Scroll to analysis section
    document.getElementById('analysis-section').scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  }

  // Render analysis results
  renderAnalysis() {
    const section = document.getElementById('analysis-section');
    section.style.display = 'block';

    // Render summary stats
    this.renderSummaryStats();

    // Render country allocation
    this.renderCountryAllocation();

    // Render sector allocation
    this.renderSectorAllocation();

    // Render individual holdings
    this.renderIndividualHoldings();
  }

  // Render summary statistics
  renderSummaryStats() {
    const container = document.getElementById('summary-stats');
    const { totalValue, summary } = this.analysis;

    container.innerHTML = `
      <div class="stat-card fade-in">
        <div class="stat-value">$${totalValue.toLocaleString()}</div>
        <div class="stat-label">Total Value</div>
      </div>
      <div class="stat-card fade-in">
        <div class="stat-value">${summary.totalETFs}</div>
        <div class="stat-label">ETFs/Funds</div>
      </div>
      <div class="stat-card fade-in">
        <div class="stat-value">${summary.totalSecurities}</div>
        <div class="stat-label">Total Securities</div>
      </div>
      <div class="stat-card fade-in">
        <div class="stat-value">${summary.overlapCount}</div>
        <div class="stat-label">Overlapping Holdings</div>
      </div>
    `;
  }

  // Render country allocation chart
  renderCountryAllocation() {
    const container = document.getElementById('country-allocation');
    const countries = this.analysis.countryAllocation.slice(0, 10); // Top 10

    container.innerHTML = countries.map(({ country, allocation }) => {
      const isSmall = allocation < 15;
      return `
      <div class="allocation-item fade-in">
        <div class="allocation-label">${country}</div>
        <div class="allocation-bar-container">
          <div class="allocation-bar" style="width: ${Math.max(allocation, 1)}%">
            ${!isSmall ? `<span class="allocation-percentage">${allocation.toFixed(1)}%</span>` : ''}
          </div>
          ${isSmall ? `<span class="allocation-percentage-outside">${allocation.toFixed(1)}%</span>` : ''}
        </div>
      </div>
    `}).join('');
  }

  // Render sector allocation chart
  renderSectorAllocation() {
    const container = document.getElementById('sector-allocation');
    const sectors = this.analysis.sectorAllocation;

    container.innerHTML = sectors.map(({ sector, allocation }) => {
      const isSmall = allocation < 15;
      return `
      <div class="allocation-item fade-in">
        <div class="allocation-label">${sector}</div>
        <div class="allocation-bar-container">
          <div class="allocation-bar" style="width: ${Math.max(Math.min(allocation, 100), 1)}%">
            ${!isSmall ? `<span class="allocation-percentage">${allocation.toFixed(1)}%</span>` : ''}
          </div>
          ${isSmall ? `<span class="allocation-percentage-outside">${allocation.toFixed(1)}%</span>` : ''}
        </div>
      </div>
    `}).join('');
  }

  // Render individual holdings table
  renderIndividualHoldings() {
    const container = document.getElementById('individual-holdings');
    const holdings = this.analysis.individualHoldings.slice(0, 50); // Top 50
    const maxWeight = holdings[0]?.weight || 1;

    container.innerHTML = `
      <table class="holdings-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Ticker</th>
            <th>Name</th>
            <th>Country</th>
            <th>Sector</th>
            <th>Weight</th>
            <th>Value</th>
            <th>Sources</th>
          </tr>
        </thead>
        <tbody>
          ${holdings.map((holding, index) => `
            <tr class="fade-in">
              <td>${index + 1}</td>
              <td class="table-ticker">${holding.ticker}</td>
              <td>${holding.name}</td>
              <td>${holding.country}</td>
              <td>${holding.sector}</td>
              <td>
                <div class="table-weight">${holding.weight.toFixed(2)}%</div>
                <div class="weight-bar" style="width: ${(holding.weight / maxWeight) * 100}%"></div>
              </td>
              <td>$${holding.value.toLocaleString()}</td>
              <td>
                ${holding.sources.length > 1
        ? `<span class="overlap-badge">${holding.sources.length} ETFs</span>`
        : holding.sources[0].etf
      }
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  }

  // Clear analysis display
  clearAnalysis() {
    const section = document.getElementById('analysis-section');
    section.style.display = 'none';
    this.analysis = null;
  }

  // Local storage
  saveToLocalStorage() {
    localStorage.setItem('portfolio-xray-holdings', JSON.stringify(this.portfolio));
  }

  loadFromLocalStorage() {
    const saved = localStorage.getItem('portfolio-xray-holdings');
    if (saved) {
      try {
        this.portfolio = JSON.parse(saved);
      } catch (e) {
        console.error('Error loading saved portfolio:', e);
        this.portfolio = [];
      }
    }
  }
}

// Initialize app when DOM is ready
let app;
document.addEventListener('DOMContentLoaded', () => {
  app = new PortfolioApp();
});
