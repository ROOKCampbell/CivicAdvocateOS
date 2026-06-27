#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys

def scrape_url(url, keywords):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text()
        found = [kw for kw in keywords if kw in page_text]
        if found:
            print(f"[!] FOUND PATTERNS: {found} at {url}")
        else:
            print(f"[*] No patterns found at {url}")
    except Exception as e:
        print(f"[!] Error accessing {url}: {e}")

if __name__ == "__main__":
    target_url = "https://www.cleburne.net/Archive.aspx"
    target_keywords = ["Development Agreement", "MLO", "TID"]
    scrape_url(target_url, target_keywords)
