import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_stock_mapping():
    urls = {
        "TWSE": "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2",
        "TPEX": "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4",
        "EMERGING": "https://isin.twse.com.tw/isin/C_public.jsp?strMode=5"
    }
    
    mapping = {}
    
    for market, url in urls.items():
        print(f"Fetching {market} data from {url}...")
        try:
            response = requests.get(url)
            response.encoding = 'ms950'
            
            soup = BeautifulSoup(response.text, 'lxml')
            table = soup.find('table', class_='h4')
            
            if not table:
                print(f"No table with class 'h4' found for {market}")
                continue
            
            rows = table.find_all('tr')
            market_label = "TWSE" if market == "TWSE" else "TPEX"
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 2:
                    continue
                
                val = cols[0].get_text(strip=True)
                parts = val.replace('\u3000', ' ').split(' ')
                parts = [p for p in parts if p.strip()]
                
                if len(parts) >= 2:
                    code = parts[0].strip()
                    name = parts[1].strip()
                    if code.isdigit() and (len(code) == 4 or len(code) == 5 or len(code) == 6):
                        mapping[code] = {
                            "name": name,
                            "prefix": market_label,
                            "market": market
                        }
        except Exception as e:
            print(f"Error fetching {market}: {e}")
            
    return mapping

if __name__ == "__main__":
    stock_mapping = fetch_stock_mapping()
    output_file = "stock_mapping.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(stock_mapping, f, ensure_ascii=False, indent=4)
    print(f"Generated {output_file} with {len(stock_mapping)} entries.")
