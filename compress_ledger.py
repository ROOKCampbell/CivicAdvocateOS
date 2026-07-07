#!/usr/bin/env python3
# CivicAdvocate.OS | High-Density Block Compression Archive Format
# Workflow: Overview -> Code -> Implementation

import os
import sys
import gzip
import shutil
from datetime import datetime, timezone

LEDGER_PATH = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/genesis_ledger.dat"
ARCHIVE_DIR = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/compressed"

def compress_production_ledger():
    print("=== [CivicAdvocate.OS Ledger Compression Engine Initialized] ===")
    if not os.path.exists(LEDGER_PATH):
        print(f"[-] Error: Active ledger file missing at {LEDGER_PATH}")
        sys.exit(1)

    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    archive_file = os.path.join(ARCHIVE_DIR, f"ledger_snapshot_{timestamp}.dat.gz")

    print(f"[*] Compressing live 10-block data tree to target archive location...")
    try:
        with open(LEDGER_PATH, 'rb') as f_in:
            with gzip.open(archive_file, 'wb', compresslevel=9) as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Enforce atomic read-only access posture restrictions
        os.chmod(archive_file, 0o400)
        print("\n=== [High-Density Archive Snapshot Sealed Successfully] ===")
        print(f"[+] Compressed File Path : {archive_file}")
        print(f"[+] Operational Footprint: {os.path.getsize(archive_file)} Bytes Packed Securely")
    except Exception as e:
        print(f"[-] Error executing data compression optimization loop: {str(e)}")

if __name__ == "__main__":
    compress_production_ledger()
