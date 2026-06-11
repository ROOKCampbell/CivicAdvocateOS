import asyncio
import aiohttp
import json
from datetime import datetime, timezone

IDENTITY_KEY = "Campbell; Bandy (Lynn) absolute"

# Testing the internal API structure of the OPR Gateway
API_TARGET = "https://johnson.tx.publicsearch.us/api/search" 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0",
    "Content-Type": "application/json",
    "Referer": "https://johnson.tx.publicsearch.us/results?q=Abstract+544"
}

# The JSON payload the site likely uses internally
PAYLOAD = {
    "query": "Abstract 544",
    "startIndex": 0,
    "pageSize": 10
}

async def probe_api():
    async with aiohttp.ClientSession() as session:
        print(f"[*] PROBING INTERNAL API FOR ABSTRACT 544...")
        try:
            async with session.post(API_TARGET, json=PAYLOAD, headers=HEADERS) as resp:
                print(f"[*] API RESPONSE STATUS: {resp.status}")
                if resp.status == 200:
                    data = await resp.json()
                    print(f"[✓] DATA ACQUIRED. RECORDS FOUND: {data.get('totalResults', 'Unknown')}")
                else:
                    raw = await resp.text()
                    print(f"[!] API REJECTED REQUEST. PREVIEW: {raw[:100]}")
        except Exception as e:
            print(f"[!] CONNECTION FAILURE: {str(e)}")

if __name__ == "__main__":
    asyncio.run(probe_api())
