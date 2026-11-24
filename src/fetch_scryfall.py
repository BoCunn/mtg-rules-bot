import gzip
import json
import os
import requests

HEADERS = {"User-Agent": "mtg-rules-bot/0.1", "Accept": "application/json"}

def download_bulk(kind, out_path):
    # 1. Fetch the bulk-data index
    index = requests.get("https://api.scryfall.com/bulk-data", headers=HEADERS).json()
    entry = next(e for e in index["data"] if e["type"] == kind)
    
    # 2. Use the new 'jsonl_download_uri' key
    url = entry["jsonl_download_uri"]
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    # 3. Download and decompress the .jsonl.gz file
    print(f"Downloading {kind} from {url}...")
    compressed_data = requests.get(url, headers=HEADERS).content
    raw_jsonl = gzip.decompress(compressed_data).decode("utf-8")
    
    # 4. Convert JSONL (one JSON object per line) into a standard JSON array
    # so the rest of your bot's code works without needing changes
    records = [json.loads(line) for line in raw_jsonl.splitlines() if line.strip()]
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(records, f)
    print(f"Saved {len(records)} items to {out_path}")

if __name__ == "__main__":
    download_bulk("oracle_cards", "data/oracle_cards.json")  # one entry per unique card
    download_bulk("rulings", "data/rulings.json")            # official rulings, keyed by oracle_id

