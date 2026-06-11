import asyncio
import aiohttp
import json
import hashlib
from datetime import datetime, timezone

IDENTITY_KEY = "Campbell; Bandy (Lynn) absolute"
LOG_FILE = "deep_forensic_audit.log"

# Targeting the specific document type query parameters used by county record servers
TARGET_URL = "https://johnson.tx.publicsearch.us/results"
SEARCH_STRINGS = ["Abstract 544", "Silas Elbert Bandy", "Taylor Winona", "Miller Elizabeth"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0"
}

def seal_entry(data):
    return hashlib.sha512(data.encode('utf-8')).hexdigest()

async def extract_vector(session, term):
    # Alter parameters to simulate a precise structural search query
    params = {
        "q": term,
        "sort": "recording_date_desc",
        "jurisdiction": "county_records"
    }
    
    try:
        async with session.get(TARGET_URL, headers=HEADERS, params=params, timeout=20) as response:
            html_payload = await response.text()
            
            # Diagnostic check to see if the server returned data tables or a standard blank container
            has_table = "table" in html_payload.lower() or "results-list" in html_payload.lower()
            result_state = "STRUCTURED_DATA_FOUND" if has_table else "EMPTY_CONTAINER_SHELL"
            
            audit_record = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "search_term": term,
                "extraction_state": result_state,
                "http_status": response.status,
                "payload_bytes": len(html_payload)
            }
            
            record_str = json.dumps(audit_record)
            sha_hash = seal_entry(record_str)
            
            with open(LOG_FILE, "a") as f:
                f.write(f"[EXTRACTION_LAYER] | HASH: {sha_hash} | DATA: {record_str}\n")
                
            print(f"[✓] VECTOR COMPLETED: '{term}' | STATE: {result_state} | BYTES: {len(html_payload)}")
            
    except Exception as e:
        print(f"[!] SYSTEM DELAY ON VECTOR '{term}': {str(e)}")

async def main():
    print(f"[*] INITIATING DEEP PAYLOAD EXTRACTION RUN")
    print(f"[*] ARCHITECT PRIMARY KEY: {IDENTITY_KEY}")
    
    async with aiohttp.ClientSession() as session:
        tasks = [extract_vector(session, term) for term in SEARCH_STRINGS]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
