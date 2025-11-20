# Portfolio X-Ray 📊

A comprehensive ETF portfolio analyzer that reveals the complete underlying holdings across all your funds. Built with vanilla JavaScript for maximum performance and zero dependencies.

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://mitchellrlayton.github.io/portfolio-xray/)
[![GitHub Actions](https://img.shields.io/badge/automation-github--actions-blue)](https://github.com/MitchellRLayton/portfolio-xray/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✨ Features

- **🔍 Complete Holdings Analysis**: See ALL underlying securities, not just top 10
- **📈 54,000+ Securities**: Tracks 43+ ETFs from Vanguard, iShares, and State Street
- **🌍 Geographic Breakdown**: Country allocation across your entire portfolio
- **🏭 Sector Analysis**: Industry exposure with visual charts
- **🔄 Overlap Detection**: Identify duplicate holdings across funds
- **💰 Flexible Input**: Add holdings by dollar amount or shares
- **🤖 Auto-Updates**: Monthly data refresh via GitHub Actions
- **📱 Responsive Design**: Works on desktop, tablet, and mobile

## 🚀 Quick Start

Visit the live app: **[mitchellrlayton.github.io/portfolio-xray](https://mitchellrlayton.github.io/portfolio-xray/)**

Or run locally:
```bash
python3 -m http.server 8000
# Open http://localhost:8000
```

## 📊 Supported Funds

**43+ ETFs & Mutual Funds** including:

### Vanguard (14 funds)
- VOO, VTI, VXUS, VWO, VEA, VUG, VTV, VIG, VYM, VB, VNQ, VGT, VO, VSS

### iShares (10+ funds)
- IVV, IWM, IEMG, EFA, ITOT, IXUS, IWD, IWF, IJR, IJH

### State Street SPDR (14+ funds)
- SPY, MDY, SPLG, XLK, XLF, XLV, XLE, XLP, XLY, XLI, XLB, XLC, XLRE, XLU

**Total securities tracked: 54,000+**

## 🛠️ Technology Stack

- **Frontend**: Vanilla HTML/CSS/JavaScript (no frameworks!)
- **Styling**: Custom CSS with glassmorphism effects
- **Data**: JSON/JS files loaded client-side
- **Automation**: GitHub Actions for monthly updates
- **Testing**: Python pytest + custom validation suite

## 🔄 Automated Updates

Holdings data is automatically updated monthly via GitHub Actions:

- **Schedule**: 1st of each month at 2 AM UTC
- **Source**: Direct API/downloads from fund providers
- **Process**: Download → Process → Validate → Commit
- **Validation**: 22 automated tests ensure data quality

Manual updates:
```bash
make update    # Download, process, validate all holdings
make test      # Run all validation tests
```

## 📁 Project Structure

```
portfolio-xray/
├── index.html              # Main application
├── styles.css              # Premium dark mode styling
├── app.js                  # UI logic & portfolio state
├── analytics.js            # Holdings analysis engine
├── data.js                 # Data loading & management
├── data/
│   ├── holdings/          # Provider data (Vanguard, iShares, SPDR)
│   ├── holdings_json/     # Processed fund data (JSON)
│   └── holdings_js/       # Browser-ready JS files
├── tests/
│   ├── test_holdings.py   # Pytest unit tests
│   ├── validate_holdings.py  # Data validation
│   └── generate_report.py    # Auto-reporting
├── .github/workflows/
│   └── update-holdings.yml    # Monthly automation
└── Makefile               # Local automation commands
```

## 🧪 Testing

```bash
# Run all tests
make test

# Pytest unit tests
make pytest

# Quick validation
make validate

# With coverage
make pytest-cov
```

## 📖 Documentation

- [TESTING.md](TESTING.md) - Complete testing guide
- [automation_setup.md](automation_setup.md) - Automation infrastructure
- [holdings_verification.md](holdings_verification.md) - Data accuracy report

## 🤝 Contributing

Contributions welcome! To add a new fund:

1. Add to appropriate download script (`download_vanguard.sh`, etc.)
2. Run `make update` to download and process
3. Run `make test` to validate
4. Submit PR

## 📝 License

MIT License - feel free to use for personal or commercial projects!

## 🙏 Acknowledgments

- Holdings data sourced from Vanguard, iShares (BlackRock), and State Street
- Built with ❤️ using vanilla JavaScript
- Automated with GitHub Actions

## 📧 Contact

Created by Mitchell Layton - [GitHub](https://github.com/MitchellRLayton)

---

**Disclaimer**: This tool uses representative holdings data and should not be used as the sole basis for investment decisions. Holdings data is updated monthly but may not reflect real-time changes. Always verify with official fund documentation.
