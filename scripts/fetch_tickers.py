import csv
import json
import requests
from pathlib import Path

OUT = Path("data")
OUT.mkdir(parents=True, exist_ok=True)
TICKERS_FILE = OUT / "tickers.json"

# Load existing tickers (if any)
if TICKERS_FILE.exists():
    with open(TICKERS_FILE, "r", encoding="utf-8") as f:
        tickers = json.load(f)
else:
    tickers = {"NSE": [], "BSE": []}

# Ensure structure
tickers.setdefault("NSE", [])
tickers.setdefault("BSE", [])

# Helper to check if symbol exists in a given list
def symbol_exists(exchange_list, symbol):
    return any(t["symbol"] == symbol for t in exchange_list)

# Single session for cookies & headers
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
})

def fetch_nse():
    """Fetch NSE F&O securities list via API."""
    try:
        url = "https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"
        session.get("https://www.nseindia.com", timeout=10)  # set cookies
        r = session.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()
        return [
            {"symbol": item.get("symbol", "").strip(),
             "name": item.get("identifier", "").strip()}
            for item in data.get("data", [])
            if "symbol" in item
        ]
    except Exception:
        # Alternate source (backup API)
        try:
            alt_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
            r = session.get(alt_url, timeout=30)
            r.raise_for_status()
            reader = csv.reader(r.text.splitlines())
            header = next(reader, [])
            return [{"symbol": row[0].strip(), "name": row[1].strip()}
                    for row in reader if len(row) >= 2]
        except Exception as e:
            print("NSE fetch failed from all sources:", e)
            return []
        
def main():
    try:
        print("Fetching NSE...")
        nse_data = fetch_nse()
        added = 0
        for item in nse_data:
            if not symbol_exists(tickers["NSE"], item["symbol"]):
                tickers["NSE"].append(item)
                added += 1
        print(f"Added {added} new NSE entries (total: {len(tickers['NSE'])}).")
    except Exception as e:
        print("NSE fetch failed:", e)

    with open(TICKERS_FILE, "w", encoding="utf-8") as f:
        json.dump(tickers, f, indent=2, ensure_ascii=False)
    print(f"Saved {TICKERS_FILE}")

if __name__ == "__main__":
    main()
