[![CI](https://github.com/devjohxylon/geoenrich/actions/workflows/ci.yml/badge.svg)]
[![PyPI](https://img.shields.io/pypi/v/geoenrich.svg)]
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]

# Geo-Enricher CLI

A fast, configurable command-line tool to enrich CSVs of IP addresses or latitude/longitude pairs with:

- **Country**, **Region/State**, **City**  
- **Latitude** & **Longitude**  
- **Timeouts**, **Retries**, **Verbose** logging

## 📥 Installation

git clone https://github.com/devjohxylon/geoenrich.git
cd geoenrich
python -m venv venv
source venv/Scripts/activate   # Git Bash on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .

🚀 Usage

# 1) Enrich IPs (default column 'ip')
geoenrich input.csv output.csv

# 2) Enrich latitude/longitude pair
geoenrich --ip-col none --coord-cols lat,lon input.csv output.csv

# 3) Custom timeouts, retries, verbose
geoenrich --timeout 10 --retries 3 --verbose input.csv output.csv

📊 Exit Codes
Code	Meaning
0	Success
1	I/O error
2	Invalid input file
3	HTTP error or timeout
4	Malformed CSV
5	Missing required columns

⚖️ License
MIT © 2025 John Lohse
See LICENSE for details.