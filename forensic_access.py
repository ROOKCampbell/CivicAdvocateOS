#!/usr/bin/env python3
import requests

def get_portal_access(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            print(f"[!] Access Granted to {url}")
            return True
        else:
            print(f"[!] Blocked/Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"[!] Connection Error: {e}")

if __name__ == "__main__":
    print("[*] Testing Probate Portal...")
    get_portal_access("https://portal-txjohnson.tylertech.cloud/PublicAccess/default.aspx")
    print("[*] Testing Deed Portal...")
    get_portal_access("https://johnson.tx.publicsearch.us/")
