# Testing & Validation Guide

This document explains how to test and validate the ETF holdings data both locally and in CI/CD.

## Quick Start

### Local Testing (Recommended)

```bash
# Run all tests
make test

# Or more detailed:
pytest tests/ -v

# With coverage report
pytest tests/ --cov --cov-report=html
```

### Full Update Pipeline

```bash
# Download, process, validate, and generate report
make update
```

---

## Testing Approaches

We use **two complementary testing approaches**:

### 1. ✅ Pytest Unit Tests (`tests/test_holdings.py`)
**Best for:** Granular, developer-focused testing

```bash
# Run all unit tests
pytest tests/

# Run specific test class
pytest tests/test_holdings.py::TestHoldingsData

# Run specific test
pytest tests/test_holdings.py::TestHoldingsData::test_minimum_holdings_count

# Run with coverage
pytest tests/ --cov --cov-report=term-missing

# Run and stop on first failure
pytest tests/ -x
```

**What it tests:**
- ✅ File existence (JSON and JS files)
- ✅ JSON structure validity
- ✅ Minimum holdings counts for major funds
- ✅ Weight value validity (0-100%)
- ✅ Weight totals (~100%)
- ✅ No duplicate tickers
- ✅ No empty values
- ✅ Provider-specific data presence
- ✅ Cross-fund consistency
- ✅ Total securities count sanity checks

### 2. ✅ Validation Script (`tests/validate_holdings.py`)
**Best for:** Quick validation, CI/CD, and human-readable reports

```bash
# Run validation (works locally AND in GitHub Actions)
python3 tests/validate_holdings.py

# Or via make
make validate
```

**What it tests:**
- 📁 File existence
- 🔧 Data structure
- 📊 Minimum holdings counts
- ⚖️  Weight totals
- 🔍 Duplicate detection
- 📅 Data freshness
- 📈 Statistics collection

**Output:** Colored, human-readable terminal output with clear pass/fail status

---

## Local Development Workflow

### Option A: Just Validate Existing Data
```bash
# Quick check
make validate

# Or detailed pytest
pytest tests/ -v
```

### Option B: Full Update & Validation
```bash
# 1. Download latest holdings
make download

# 2. Process into JSON/JS
make process

# 3. Validate
make validate

# 4. Generate report
make report
```

### Option C: One Command (Recommended)
```bash
# Does all of the above
make update
```

---

## Testing in GitHub Actions

The `.github/workflows/update-holdings.yml` workflow runs **both** validation approaches:

```yaml
- name: Run validation tests
  run: |
    python3 tests/validate_holdings.py  # Human-readable validation

# Could also add:
- name: Run pytest suite
  run: |
    pip install pytest pytest-cov
    pytest tests/ -v --cov
```

**When it runs:**
- ✅ Monthly on the 1st (scheduled)
- ✅ Manual trigger (workflow_dispatch)
- ✅ On push to main (for testing)

**What happens on failure:**
- ❌ Workflow fails
- 📧 GitHub sends notification
- 📦 Failed downloads saved as artifacts
- 🚫 No commit is made

---

## Testing Individual Funds

### Check specific fund
```bash
# Quick check
make check-VXUS

# Detailed pytest
pytest tests/test_holdings.py::test_minimum_holdings_count[VXUS-8000] -v
```

### Validate specific file manually
```python
python3 -c "
import json
data = json.load(open('data/holdings_json/VXUS.json'))
print(f'Holdings: {len(data)}')
print(f'Total weight: {sum(h.get(\"weight\", 0) for h in data):.2f}%')
"
```

---

## CI/CD Integration

### GitHub Actions (Current)
- ✅ Already configured in `.github/workflows/update-holdings.yml`
- ✅ Runs monthly automatically
- ✅ Can trigger manually from Actions tab

### Local Simulation of CI
```bash
# Simulate what GitHub Actions will do
bash -c "
  ./download_ishares.sh && \
  ./download_statestreet.sh && \
  ./download_vanguard.sh && \
  python3 process_holdings.py && \
  python3 tests/validate_holdings.py
"
```

### Pre-commit Hook (Optional)
Create `.git/hooks/pre-commit`:

``` bash
#!/bin/bash
# Validate holdings data before committing

if git diff --cached --name-only | grep -q "data/holdings"; then
    echo "🔍 Validating holdings data..."
    python3 tests/validate_holdings.py || exit 1
fi
```

---

## Understanding Test Output

### Pytest Output
```
tests/test_holdings.py::TestHoldingsData::test_json_files_exist PASSED     [ 5%]
tests/test_holdings.py::TestHoldingsData::test_minimum_holdings_count[VXUS-8000] PASSED [10%]
...
====== 42 passed in 2.34s ======
```

### Validation Script Output
```
🔍 Validating ETF Holdings Data
======================================================================

📁 Checking file existence...
   ✓ All expected files present

🔧 Validating data structure...
   ✓ All files have valid structure

📊 Checking holdings counts...
   ✓ All funds meet minimum holdings requirements
...

✅ ALL VALIDATIONS PASSED!
```

---

## Troubleshooting

### "pytest: command not found"
```bash
pip install pytest pytest-cov
```

### "No module named pandas"
```bash
pip install -r requirements.txt
```

### "File not found: data/holdings_json/VXUS.json"
```bash
# Download and process data first
make update
```

### Test fails but data looks correct
```bash
# Check if minimums are too strict
# View specific test:
pytest tests/test_holdings.py::test_minimum_holdings_count -v

# Adjust minimums in validate_holdings.py if needed
```

---

## Best Practices

1. **Always validate before committing**
   ```bash
   make validate && git commit
   ```

2. **Run full update monthly**
   ```bash
   # On the 1st of each month
   make update
   ```

3. **Check specific funds after provider changes**
   ```bash
   make check-VOO check-VTI check-VXUS
   ```

4. **Review HOLDINGS_REPORT.md** after each update
   - Check for stale data warnings
   - Verify holdings counts match expectations
   - Look for weight total anomalies

---

## Summary Table

| Command | Speed | Detail | CI-Compatible | Best For |
|---------|-------|--------|---------------|----------|
| `make validate` | ⚡ Fast | Medium | ✅ Yes | Quick checks |
| `pytest tests/` | ⚡ Fast | High | ✅ Yes | Development |
| `pytest --cov` | 🐌 Slow | Very High | ✅ Yes | Coverage reports |
| `make update` | 🐌 Slow | High | ✅ Yes | Full pipeline |
| `make check-TICKER` | ⚡ Fast | Low | ❌ Manual | Single fund check |

**Recommendation:** Use `pytest` for development, `make validate` for quick checks, and let GitHub Actions handle monthly updates.
