import requests
from bs4 import BeautifulSoup

def list_archive_links(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            if '.pdf' in link['href'] or 'Archive' in link['href']:
                print(f"[FOUND] {link.get_text(strip=True)} -> {link['href']}")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    list_archive_links("https://www.cleburne.net/Archive.aspx")
