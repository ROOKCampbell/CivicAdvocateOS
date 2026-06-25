import requests
import hashlib
from bs4 import BeautifulSoup

def extract_and_verify(url):
    response = requests.get(url, headers={'User-Agent': 'CivicAdvocate-OS-Agent'})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        patentee_element = soup.find(string="Patentee")
        patentee = patentee_element.find_next().text.strip() if patentee_element else "N/A"
        content_hash = hashlib.sha512(response.content).hexdigest()
        print(f"Patentee: {patentee}")
        print(f"Hash: {content_hash[:16]}...")
        return {"patentee": patentee, "hash": content_hash}
    else:
        print(f"Error: {response.status_code}")

target = "https://www.glo.texas.gov/archives-heritage/search-our-collections/land-grant-search/land-grant/167688-1987"
extract_and_verify(target)
