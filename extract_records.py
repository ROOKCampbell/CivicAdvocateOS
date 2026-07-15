import requests
from bs4 import BeautifulSoup

# Define targets
BASE_URL = "https://johnson.tx.publicsearch.us"
SEARCH_URL = f"{BASE_URL}/search/results"
SESSION = requests.Session()

def get_token():
    # Fetch landing page to initiate session and grab CSRF token
    resp = SESSION.get(BASE_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Locate token in the script tag or meta tag
    token = SESSION.cookies.get_dict().get('XSRF-TOKEN') or soup.find("meta", {"name": "csrf-token"})
    return token.get('content') if hasattr(token, 'get') else token

def execute_search(query):
    token = get_token()
    headers = {
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/",
        "X-XSRF-TOKEN": token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "legalDescription": query,
        "search_type": "legal"
    }
    response = SESSION.post(SEARCH_URL, headers=headers, data=payload)
    return response.text

if __name__ == "__main__":
    results = execute_search("SILAS ELBERT BANDY")
    with open("raw_output.html", "w") as f:
        f.write(results)
    print("Search complete. Data written to raw_output.html.")
