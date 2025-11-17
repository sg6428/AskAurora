import requests

def test_ask_api():
    url = "http://127.0.0.1:8000/ask"
    payload = {"question": "Give information about Vikram's party"}
    
    response = requests.post(url, json=payload)
    
    print(response.json())

if __name__ == "__main__":
    test_ask_api()