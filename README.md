cat > README.md << 'EOF'
[![CI](https://github.com/devjohxylon/geoenrich/actions/workflows/ci.yml/badge.svg)]
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]

# Geo-Enricher CLI

A fast, configurable command-line tool to enrich CSVs of IP addresses or latitude/longitude pairs with:

- **Country**, **Region/State**, **City**  
- **Latitude** & **Longitude**  
- **Configurable** timeouts, retries, and verbose logging  

---

## 📥 Installation

### From source
\`\`\`bash
git clone https://github.com/devjohxylon/geoenrich.git
cd geoenrich

# Create & activate virtualenv
python -m venv venv
# Git Bash on Windows:
source venv/Scripts/activate

# Install runtime dependencies
pip install -r requirements.txt

# Install dev tools (for testing/formatting/etc.)
pip install -r requirements-dev.txt

# Editable install for development
pip install -e .
\`\`\`

---

## 🚀 Usage

1. **Enrich IP column** (default column name is \`ip\`):  
   \`\`\`bash
   geoenrich input.csv output.csv
   \`\`\`

2. **Enrich latitude/longitude columns**:  
   \`\`\`bash
   geoenrich --ip-col none --coord-cols lat,lon input.csv output.csv
   \`\`\`

3. **Custom timeouts, retries, verbose**:  
   \`\`\`bash
   geoenrich \
     --timeout 10 \
     --retries 3 \
     --verbose \
     input.csv \
     output.csv
   \`\`\`

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