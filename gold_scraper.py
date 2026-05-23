import os, requests
from bs4 import BeautifulSoup
from datetime import datetime

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_gold_prices():
    url = "https://market.isagha.com/prices"
    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    
    prices = {}
    try:
        items = soup.select("div.price-item, tr, .price-row")
        for item in items:
            text = item.text.strip()
            if "21" in text:
                nums = [float(s.replace(",","")) for s in text.split() if s.replace(",","").replace(".","").isdigit()]
                if nums: prices["usd_21"] = nums[0]
            if "24" in text:
                nums = [float(s.replace(",","")) for s in text.split() if s.replace(",","").replace(".","").isdigit()]
                if nums: prices["usd_24"] = nums[0]
            if "18" in text:
                nums = [float(s.replace(",","")) for s in text.split() if s.replace(",","").replace(".","").isdigit()]
                if nums: prices["usd_18"] = nums[0]
    except Exception as e:
        print(f"Error parsing: {e}")
    
    return prices if prices else None

def save_to_supabase(prices):
    url = f"{SUPABASE_URL}/rest/v1/gold_prices"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    r = requests.post(url, json=prices, headers=headers, timeout=10)
    print(f"Saved: {r.status_code} — {prices}")

def main():
    prices = get_gold_prices()
    if prices:
        save_to_supabase(prices)
    else:
        print("مش قادر يجيب الأسعار")

if __name__ == "__main__":
    main()
