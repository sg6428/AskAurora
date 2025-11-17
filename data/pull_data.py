import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import os

def create_raw_data_dir(raw_data_dir="./raw_data"):
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)

def fetch_page(skip, api_url, page_limit=500):
    params = {"skip": skip, "limit": page_limit}
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    return response.json().get('items', [])

def pull_data(api_url, page_limit=500, raw_data_dir="data/raw_data"):
    # Check if raw_data directory exists, if not create it
    create_raw_data_dir(raw_data_dir)

    resp = requests.get(api_url, params={"skip": 0, "limit": 1})
    resp.raise_for_status()
    total = resp.json().get('total', 0)
    
    skip_values = list(range(0, total+page_limit, page_limit))
    
    for skip in skip_values:
        page_messages = fetch_page(skip, api_url, page_limit)
        ts = str(time.time()).replace('.', '_')
        with open(f'{raw_data_dir}/raw_{ts}.json', 'w') as f:
            json.dump(page_messages, f, indent=4)

# Alternative function for a thread-based approach
def pull_data_threaded(api_url, page_limit=500, raw_data_dir="data/raw_data"):
    # Check if raw_data directory exists, if not create it
    create_raw_data_dir(raw_data_dir)

    resp = requests.get(api_url, params={"skip": 0, "limit": 1})
    resp.raise_for_status()
    total = resp.json().get('total', 0)
    
    skip_values = list(range(0, total+page_limit, page_limit))

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_to_skip = {executor.submit(fetch_page, skip, api_url, page_limit): skip for skip in skip_values}
        for future in as_completed(future_to_skip):
            page_messages = future.result()
            ts = str(time.time()).replace('.', '_')
            with open(f'{raw_data_dir}/raw_{ts}.json', 'w') as f:     
                json.dump(page_messages, f, indent=4)       

if __name__ == "__main__":
    pull_data_threaded()
