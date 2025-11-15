import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

API_URL = "https://november7-730026606190.europe-west1.run.app/messages"
PAGE_LIMIT = 500  # Number of items per request (adjust as needed)
all_results = []
raw_data_file_path = "AskAurora/raw_data/raw"

def fetch_page(skip):
    params = {"skip": skip, "limit": PAGE_LIMIT}
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json().get('items', [])

def fetch_all_messages():
    # Get total number of messages
    resp = requests.get(API_URL, params={"skip": 0, "limit": 1})
    resp.raise_for_status()
    total = resp.json().get('total', 0)
    
    # Prepare all skip values
    skip_values = list(range(0, total+PAGE_LIMIT, PAGE_LIMIT))
    print(f"{skip_values=}")
    
    for skip in skip_values:
        page_messages = fetch_page(skip)
        # Insert messages into the json file
        # Generate timestamped filename till milliseconds
        ts = str(time.time()).replace('.', '_')
        with open(f'{raw_data_file_path}_{ts}.json', 'w') as f:
            json.dump(page_messages, f, indent=4)

# Alternative function for a thread-based approach
def fetch_all_messages_threaded():
    # Get total number of messages
    resp = requests.get(API_URL, params={"skip": 0, "limit": 1})
    resp.raise_for_status()
    total = resp.json().get('total', 0)
    
    # Prepare all skip values
    skip_values = list(range(0, total+PAGE_LIMIT, PAGE_LIMIT))
    print(f"{skip_values=}")

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_to_skip = {executor.submit(fetch_page, skip): skip for skip in skip_values}
        for future in as_completed(future_to_skip):
            page_messages = future.result()
            # Insert messages into the json file  
            ts = str(time.time()).replace('.', '_')
            with open(f'{raw_data_file_path}_{ts}.json', 'w') as f:     
                json.dump(page_messages, f, indent=4)       

if __name__ == "__main__":
    fetch_all_messages_threaded()
