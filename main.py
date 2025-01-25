import os
import requests
import csv
import time
from datetime import datetime, timedelta

def load_env():
    """Simple .env file loader"""
    try:
        with open('.env') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass

def get_daily_prices():
    """Get daily prices from Alpha Vantage API"""
    load_env()
    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    
    if not api_key:
        raise ValueError("Missing API key in environment variables")
    
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "BRENT",
        "interval": "daily",
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return parse_daily_data(response.json())
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None

def parse_daily_data(raw_data):
    """Extract and validate daily price data"""
    prices = []
    for entry in raw_data.get("data", []):
        if "date" in entry and "value" in entry:
            try:
                prices.append({
                    "date": entry["date"],
                    "price": float(entry["value"]),
                    "currency": "USD",
                    "unit": "barrel"
                })
            except (ValueError, TypeError):
                continue
    return prices

def save_daily_data(data):
    """Save daily data to CSV with duplicate prevention"""
    os.makedirs("data", exist_ok=True)
    file_path = "data/daily_oil_prices.csv"
    existing_dates = set()

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            existing_dates = {row['date'] for row in reader}

    new_data = [row for row in data if row['date'] not in existing_dates]

    if not new_data:
        print("No new daily data to save")
        return

    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["date", "price", "currency", "unit"])
        if not existing_dates:
            writer.writeheader()
        writer.writerows(new_data)
    print(f"Saved {len(new_data)} new daily entries")

def run_extraction():
    """Main extraction workflow"""
    print(f"Running extraction at {datetime.now()}")
    daily_prices = get_daily_prices()
    if daily_prices:
        save_daily_data(daily_prices)
    else:
        print("Failed to retrieve daily prices")

if __name__ == "__main__":
    # Initial run
    run_extraction()
    
    # Calculate next run in 10 days
    while True:
        next_run = datetime.now() + timedelta(days=10)
        print(f"Next extraction scheduled for {next_run}")
        time.sleep(10 * 24 * 60 * 60)  # Sleep for 10 days
        run_extraction()