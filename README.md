# FX Margin Sentinel

Automated FX channel calculating safety buffers for import businesses facing currency depreciation.

## The Problem
Import businesses in volatile currency environments face margin compression when purchasing products or inventory against unstable exchange rates. Standard pricing models rely on stale spot rates, eroding operational profits by invoice settlement.

## Features
- **Live Ingestion**: Queries spot rates for USD, EUR, and GBP against GHS via REST API.
- **Hedging Engine**: Computes dynamic risk buffers (default 5%) to absorb settlement volatility.
- **Auditable Exports**: Serializes snapshots to clean CSV records for accounting workflows.

## Quickstart

```bash
# 1. Clone repository
git clone [https://github.com/Robert-Danso/fx-margin-sentinel.git](https://github.com/Robert-Danso/fx-margin-sentinel.git)
cd fx-margin-sentinel

# 2. Virtual Environment setup
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies & run
pip install -r requirements.txt
python main.py

Output preview
Pair,    Spot,  Hedged (+5%), Buffer
USD_GHS, 16.20,  17.01,        0.81
EUR_GHS, 17.50,  18.37,        0.87
GBP_GHS, 20.80,  21.84,        1.04