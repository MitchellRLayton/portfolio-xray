// ETF Holdings Database
// Core functionality for managing fund data

// Initialize global database
window.ETF_DATABASE = window.ETF_DATABASE || {};

// Helper function to register funds
function registerFunds(funds) {
  Object.assign(window.ETF_DATABASE, funds);
}

// Helper function to get ETF data
function getETFData(ticker) {
  const fund = window.ETF_DATABASE[ticker.toUpperCase()] || null;

  // Check if full holdings data is available
  if (fund && window.ETF_HOLDINGS && window.ETF_HOLDINGS[ticker.toUpperCase()]) {
    // Return a new object with full holdings
    return {
      ...fund,
      holdings: window.ETF_HOLDINGS[ticker.toUpperCase()]
    };
  }

  return fund;
}

// Helper function to get all available tickers
function getAvailableTickers() {
  return Object.keys(window.ETF_DATABASE).sort();
}
