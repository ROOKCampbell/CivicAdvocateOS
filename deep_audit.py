import asyncio
import aiohttp
import hashlib
import json
from datetime import datetime, timezone

IDENTITY_KEY = "Campbell; Bandy (Lynn) absolute"
AUDIT_LOG = "deep_forensic_audit.log"

# Search Parameters for Abstract 544 and Lineage
SEARCH_TARGETS = [
    "Abstract 544",
    "Silas Elbert Bandy",
    "Campbell Bandy",
    "Bandy Lynn"
]

# The JOCO OPR Gateway is the vulnerability we exploit now
BASE_URL = "https://johnson.tx.publicsearch.us/results"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def seal_record(content):
    return hashlib.sha512(content.encode('utf-8')).hexdigest()

async def search_index(session, query):
    # Construct the direct search query URL
    url = f"{BASE_URL}?q={query.replace(' ', '+')}"
    t_start = datetime.now(timezone.utc)
    
    try:
        async with session.get(url, headers=HEADERS, timeout=30) as response:
            text = await response.text()
            
            # Record the presence of data
            found_indicator = "DATA_PRESENT" if query.lower() in text.lower() else "NO_DIRECT_MATCH"
            
            payload = {
                "query": query,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": response.status,
                "indicator": found_indicator,
                "gate": "JOCO_OPR_SEARCH"
            }
            
            payload_str = json.dumps(payload)
            sha_hash = seal_record(payload_str)
            
            with open(AUDIT_LOG, "a") as f:
                f.write(f"[INDEX_AUDIT] | HASH: {sha_hash} | DATA: {payload_str}\n")
            
            print(f"[✓] AUDITED: '{query}' | RESULT: {found_indicator} | HASH: {sha_hash[:16]}...")
            
    except Exception as e:
        print(f"[!] ERROR SEARCHING '{query}': {str(e)}")

async def main():
    print(f"[*] STARTING DEEP INDEX AUDIT | ARCHITECT: {IDENTITY_KEY}")
    async with aiohttp.ClientSession() as session:
        tasks = [search_index(session, target) for target in SEARCH_TARGETS]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
