.PHONY: help download process validate test update clean report

# Default target
help:
	@echo "Portfolio X-Ray - ETF Holdings Management"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make download    - Download all ETF holdings data"
	@echo "  make process     - Process downloaded files into JSON/JS"
	@echo "  make validate    - Run validation tests on processed data"
	@echo "  make report      - Generate holdings data report"
	@echo "  make test        - Run validation tests only"
	@echo "  make update      - Full pipeline: download + process + validate"
	@echo "  make clean       - Remove downloaded and processed files"
	@echo ""

# Download all holdings data
download:
	@echo "📥 Downloading holdings data from providers..."
	@echo ""
	@echo "iShares ETFs..."
	@./download_ishares.sh || true
	@echo ""
	@echo "State Street (SPDR) ETFs..."
	@./download_statestreet.sh || true
	@echo ""
	@echo "Vanguard ETFs & Mutual Funds..."
	@./download_vanguard.sh || true
	@echo ""
	@echo "✅ Download complete!"

# Process downloaded files into JSON and JS
process:
	@echo "⚙️  Processing holdings data..."
	@python3 process_holdings.py
	@echo "✅ Processing complete!"

# Run validation tests
validate:
	@echo "🔍 Running validation tests..."
	@python3 tests/validate_holdings.py

# Run pytest unit tests
pytest:
	@echo "🧪 Running pytest unit tests..."
	@python3 -m pytest tests/ -v

# Run pytest with coverage
pytest-cov:
	@echo "🧪 Running pytest with coverage..."
	@python3 -m pytest tests/ -v --cov --cov-report=term-missing

# Generate report
report:
	@echo "📊 Generating holdings report..."
	@python3 tests/generate_report.py > HOLDINGS_REPORT.md
	@echo "✅ Report saved to HOLDINGS_REPORT.md"

# Run tests without downloading/processing
test: validate pytest

# Full update pipeline
update: download process validate report
	@echo ""
	@echo "✅ Holdings data updated successfully!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Review HOLDINGS_REPORT.md"
	@echo "  2. Test the application locally: python3 -m http.server 8000"
	@echo "  3. Commit changes: git add -A && git commit -m 'chore: update holdings'"
	@echo ""

# Clean all generated files
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -rf data/holdings_files/*
	@rm -rf data/holdings_json/*
	@rm -rf data/holdings_js/*
	@rm -f HOLDINGS_REPORT.md
	@echo "✅ Clean complete!"

# Quick validation of specific fund
check-%:
	@python3 -c "import json; data=json.load(open('data/holdings_json/$*.json')); print(f'$*: {len(data)} holdings, {sum(h.get(\"weight\",0) for h in data):.2f}% total weight')"
