import requests
import pandas as pd

BASE_URL = "https://open.er-api.com/v6/latest/USD"

def fetch_rates():
    response = requests.get(BASE_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    rates = data.get("rates", {})
    
    usd_to_ghs = rates.get("GHS")
    usd_to_eur = rates.get("EUR")
    usd_to_gbp = rates.get("GBP")

    if not all([usd_to_ghs, usd_to_eur, usd_to_gbp]):
        raise ValueError("One or more required currency pairs missing from API payload.")

    # GHS / EUR = EUR_GHS
    eur_to_ghs = usd_to_ghs / usd_to_eur
    gbp_to_ghs = usd_to_ghs / usd_to_gbp
    
    return {
        "USD_GHS": round(usd_to_ghs, 4),
        "EUR_GHS": round(eur_to_ghs, 4),  
        "GBP_GHS": round(gbp_to_ghs, 4)
    }

def add_buffer(rates_dict, buffer_percent = 0.05):
    rows = []
    for pair, rate in rates_dict.items():
        # skip if rate is not a number
        if not isinstance(rate, (int, float)):
            continue
        
        hedged = round(rate * (1 + buffer_percent), 4)
        buffer = round(hedged - rate, 4)
        
        rows.append({
            "Pair": pair,
            "Spot": rate,
            "Hedged": hedged,
            "Buffer": buffer
        })
    
    return pd.DataFrame(rows)

def main():
    rates = fetch_rates()
    table = add_buffer(rates)
    print(table.to_string(index=False))
    table.to_csv("my_fx_report.csv", index=False)
    print("Saved!")

if __name__ == "__main__":
    main()