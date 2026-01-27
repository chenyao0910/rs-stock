import json
import requests
import sys
import re

def load_stock_mapping(mapping_file="stock_mapping.json"):
    try:
        with open(mapping_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {mapping_file} not found. Please run generate_mapping.py first.")
        sys.exit(1)

def get_rs_rank_data(weeks, min_rs_rank):
    """
    Fetch RS Rank data from MoneyDJ.
    URL format: https://moneydj.emega.com.tw/z/zk/zkf/zkResult.asp?D=1&A=x@250,a@{weeks},b@{min_rs_rank}&site=
    """
    print(f"Fetching RS Rank data from MoneyDJ (weeks: {weeks}, min_rank: {min_rs_rank})...")
    
    # Construct URL. Assuming 'a@' is the week duration.
    url = f"https://moneydj.emega.com.tw/z/zk/zkf/zkResult.asp?D=1&A=x@250,a@{weeks},b@{min_rs_rank}&site="
    
    try:
        response = requests.get(url)
        # MoneyDJ typically uses big5 or cp950
        response.encoding = 'big5'
        
        # Look for the stock list in the JavaScript variable parent.sStklistAll
        match = re.search(r"parent\.sStklistAll\s*=\s*'([^']+)'", response.text)
        if match:
            raw_codes = match.group(1)
            # The string is unicode-escaped like \u0031\u0034...
            # We can decode it using unicode_escape
            decoded_codes = raw_codes.encode('utf-8').decode('unicode-escape')
            codes = [c.strip() for c in decoded_codes.split(',') if c.strip()]
            
            print(f"Found {len(codes)} stocks from MoneyDJ.")
            # Return as list of dicts. Rank is at least min_rs_rank.
            return [{"code": code, "rs_rank": f">{min_rs_rank}"} for code in codes]
        
        print("Warning: Could not find parent.sStklistAll in the response.")
        # Alternatively, find the codes in the table if parent.sStklistAll is not available
        # (Though based on test_api.py, it should be there)
        return []
        
    except Exception as e:
        print(f"Error fetching data from MoneyDJ: {e}")
        return []

def main():
    # 1. Input conditions
    try:
        # Default to 1 week and 80 rank as per user's URL example
        weeks_input = input("Enter number of weeks (default 1): ")
        weeks = int(weeks_input) if weeks_input else 1
        
        rank_input = input("Enter minimum RS Rank (default 80): ")
        min_rs_rank = int(rank_input) if rank_input else 80
    except ValueError:
        print("Invalid input. Please enter numbers.")
        return

    # 2. Call API to get stock codes
    rs_data = get_rs_rank_data(weeks, min_rs_rank)
    if not rs_data:
        print("No stocks found matching the criteria.")
        return

    # 3. Load mapping dictionary
    mapping = load_stock_mapping()

    # 4. Map to TWSE/TPEX and output
    print(f"\nFiltered Stocks (RS Rank >= {min_rs_rank} in last {weeks} weeks):")
    print("-" * 50)
    
    results = []
    for item in rs_data:
        code = item["code"]
        rs_rank = item["rs_rank"]
        
        info = mapping.get(code)
        if info:
            prefix = info["prefix"]
            name = info["name"]
            formatted_code = f"{prefix}:{code}"
            results.append({
                "code": formatted_code,
                "name": name,
                "rs_rank": rs_rank
            })
            print(f"{formatted_code} ({name})")
        else:
            # If not in mapping, we still show but warn
            print(f"UNKNOWN:{code} (Not in mapping)")

    # Save results to JSON
    with open("filtered_stocks.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    # Save results to TXT in "PREFIX:CODE,PREFIX:CODE" format
    code_list = [item["code"] for item in results]
    txt_output = ",".join(code_list)
    with open("filtered_stocks.txt", "w", encoding="utf-8") as f:
        f.write(txt_output)
        
    print(f"\nTotal: {len(results)} stocks.")
    print(f"Saved JSON results to filtered_stocks.json")
    print(f"Saved TXT results to filtered_stocks.txt")
    
    # Print the comma-separated string for easy copying
    if code_list:
        print("\nComma-separated list:")
        print(txt_output)

if __name__ == "__main__":
    main()
