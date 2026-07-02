import requests
import sys
import time

def check_server(url):
    try:
        # Simple GET request to see if the server is alive
        requests.get(url, timeout=2)
        return True
    except requests.ConnectionError:
        return False

def scrape_agenda():
    target = "https://www.cleburne.net/AgendaCenter/City-Council-1"
    api = "http://127.0.0.1:5001/audit/submit"
    
    # Pre-flight check
    if not check_server("http://127.0.0.1:5001"):
        print("[!] Warning: Audit server unreachable. Stashing results locally.")
        # We could save this to a file here instead of exiting
        return

    # ... [Rest of your scraping logic here] ...
    print("[+] Server reachable. Proceeding with audit submission.")

if __name__ == "__main__":
    scrape_agenda()
