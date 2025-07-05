# Geo-Enricher CLI

[![CI](https://github.com/devjohxylon/geoenrich/actions/workflows/ci.yml/badge.svg)]
[![PyPI](https://img.shields.io/pypi/v/geoenrich.svg)]
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]

Enrich a CSV of IPs or lat/lng pairs with country, region, city, coords.

## Install

pip install geoenrich  
# or from source:
# git clone ... && cd geoenrich && python -m venv venv
# source venv/Scripts/activate && pip install -r requirements.txt -r requirements-dev.txt && pip install -e .

## Usage

geoenrich in.csv out.csv  
geoenrich --timeout 10 --retries 3 --verbose in.csv out.csv

## Exit Codes

0 OK • 1 I/O error • 2 Invalid input • 3 HTTP error • 4 Bad CSV • 5 Missing columns

## License

MIT © John Lohse
