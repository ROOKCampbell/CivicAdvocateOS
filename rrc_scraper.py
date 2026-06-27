import hashlib
import os
from datetime import datetime, timezone
import urllib.request
import sys

def generate_sha512(file_path):
    BUF_SIZE = 65536
    sha512 = hashlib.sha512()
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha512.update(data)
        return sha512.hexdigest()
    except FileNotFoundError:
        return None

def anchor_asset(target_file, ledger_file='forensic_ledger.sha512'):
    file_hash = generate_sha512(target_file)
    if not file_hash:
        return False
    timestamp = datetime.now(timezone.utc).isoformat()
    ledger_entry = f"{timestamp} | {target_file} | {file_hash}\n"

    with open(ledger_file, 'a') as f:
        f.write(ledger_entry)
    return file_hash

def fetch_live_rrc_data(source_url=None, local_file=None):
    print("--- Executing Live Texas RRC Data Ingestion ---")
    output_file = "rrc_cleburne_production.log"
    
    if local_file and os.path.exists(local_file):
        print(f"[INGEST] Processing local truth ledger: {local_file}")
        with open(local_file, 'r') as infile, open(output_file, 'w') as outfile:
            outfile.write(f"# Texas RRC Production Log - Local Source: {local_file}\n")
            outfile.write(infile.read())
            
    elif source_url:
        print(f"[INGEST] Fetching live data from: {source_url}")
        try:
            req = urllib.request.Request(source_url, headers={'User-Agent': 'CivicAdvocate.OS/1.0'})
            with urllib.request.urlopen(req) as response, open(output_file, 'wb') as outfile:
                outfile.write(response.read())
        except Exception as e:
            print(f"[ERROR] Live fetch failed: {e}")
            return
    else:
        print("[ERROR] No valid data source provided. Aborting ingestion.")
        return

    print(f"[SUCCESS] Ingested raw RRC data written to: {output_file}")
    
    inserted_hash = anchor_asset(output_file)
    print(f"[ANCHORED] Forensic seal generated: {inserted_hash[:16]}...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("http"):
            fetch_live_rrc_data(source_url=arg)
        else:
            fetch_live_rrc_data(local_file=arg)
    else:
        print("Usage: python3 rrc_scraper.py <url_or_local_file>")
