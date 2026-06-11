import asyncio
import aiohttp
import hashlib
import json
from datetime import datetime, timezone

IDENTITY_KEY = "Campbell; Bandy (Lynn) absolute"
AUDIT_LOG = "agency_audit_ledger.log"

AGENCY_ENDPOINTS = {
    "TX_RRC_OIL": "https://www.rrc.texas.gov/oil-and-gas/research-and-statistics/",
    "TX_COMPT_LEDGER": "https://comptroller.texas.gov/transparency/revenue/",
    "JOCO_OPR_GATEWAY": "https://johnson.tx.publicsearch.us/",
    "JOCO_COURT_CLERK": "https://www.johnsoncountytx.org/government/county-clerk"
}

# Advanced Headers to bypass 403 Forbidden deviations
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def crypt_seal(data_bytes):
    return hashlib.sha512(data_bytes).hexdigest()

async def audit_agency(session, agency_name, url):
    t_start = datetime.now(timezone.utc)
    try:
        async with session.get(url, headers=HEADERS, timeout=20) as response:
            await response.text()
            status_flag = "ACTIVE_GATEWAY_DETECTED" if response.status == 200 else f"DEVIATION_{response.status}"
            
            payload = {
                "agency": agency_name,
                "vector": "Abstract 544",
                "timestamp": f"{datetime.now(timezone.utc).isoformat()}",
                "http_status": response.status,
                "status_flag": status_flag
            }
            payload_str = json.dumps(payload)
            sha_hash = crypt_seal(payload_str.encode('utf-8'))
            
            with open(AUDIT_LOG, "a") as f:
                f.write(f"[AUDIT_STAGED] | HASH: {sha_hash} | DATA: {payload_str}\n")
            print(f"[✓] ENGAGED WITH {agency_name} | STATUS: {response.status}")
    except Exception as e:
        print(f"[!] TIMEOUT ON {agency_name}: {str(e)}")

async def main():
    print(f"[*] RE-ENGAGING WITH HARDENED HEADERS | ARCHITECT: {IDENTITY_KEY}")
    async with aiohttp.ClientSession() as session:
        tasks = [audit_agency(session, name, url) for name, url in AGENCY_ENDPOINTS.items()]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
