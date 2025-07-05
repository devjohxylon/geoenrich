[![CI](https://github.com/devjohxylon/geoenrich/actions/workflows/ci.yml/badge.svg)]
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]
[![codecov](https://codecov.io/gh/devjohxylon/geoenrich/branch/main/graph/badge.svg?flag=unittests)](https://codecov.io/gh/devjohxylon/geoenrich)

# Geo-Enricher CLI

A fast, configurable command-line tool to enrich CSVs of IP addresses or latitude/longitude pairs with:

- **Country**, **Region/State**, **City**  
- **Latitude** & **Longitude**  
- **Configurable** timeouts, retries, and verbose logging  

---

## 📆 Roadmap

- [ ] Support nested JSON flattening (`--flatten`)  
- [ ] Custom column ordering (`--columns`)  
- [ ] Stream very large files via ijson  
- [ ] Windows PowerShell native integration  
- [ ] Improve geocoding fallback logic  

---

## 📥 Installation

### From source
git clone https://github.com/devjohxylon/geoenrich.git
cd geoenrich

# Create & activate virtualenv
python -m venv venv

# Install runtime dependencies
pip install -r requirements.txt

# Install dev tools (for testing/formatting/etc.)
pip install -r requirements-dev.txt

# Editable install for development
pip install -e .

---

## 🚀 Usage

1. **Enrich IP column** (default column name is \`ip\`):  

   geoenrich input.csv output.csv

2. **Enrich latitude/longitude columns**:  
   
   geoenrich --ip-col none --coord-cols lat,lon input.csv output.csv

3. **Custom timeouts, retries, verbose**:  
   
   geoenrich \
     --timeout 10 \
     --retries 3 \
     --verbose \
     input.csv \
     output.csv \

---

## 📊 Exit Codes

| Code | Meaning                     |
|:----:|-----------------------------|
| 0    | Success                     |
| 1    | I/O error                   |
| 2    | Invalid input file          |
| 3    | HTTP error or timeout       |
| 4    | Malformed CSV               |
| 5    | Missing required columns    |

---

## ⚖️ License

MIT © 2025 devjohxylon 
See [LICENSE](LICENSE) for full details.  