#!/usr/bin/env python3
# CivicAdvocate.OS | Secure Standalone Cryptographic Exporter
# Workflow: Overview -> Code -> Implementation

import os
import sys
import json
import hmac
import hashlib
from datetime import datetime, timezone

PRIVATE_KEY = os.getenv("ARCHITECT_PRIVATE_KEY")
NODE_ADDRESS = os.getenv("NODE_ADDRESS")
LEDGER_PATH = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/genesis_ledger.dat"
EXPORT_DIR = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/exports"

def run_state_export():
    print("=== [CivicAdvocate.OS Cryptographic State Exporter] ===")
    if not PRIVATE_KEY or not NODE_ADDRESS:
        print("[-] Error: Production credentials missing. Run 'source ~/node.env' first.")
        sys.exit(1)
        
    if not os.path.exists(LEDGER_PATH):
        print(f"[-] Error: Active ledger file not found at {LEDGER_PATH}")
        sys.exit(1)

    # 1. Read and package active block records
    ledger_entries = []
    with open(LEDGER_PATH, 'r') as f:
        for line in f:
            if line.strip():
                ledger_entries.append(json.loads(line.strip()))

    print(f"[+] Loaded {len(ledger_entries)} live blocks for export processing.")

    # 2. Build standalone metadata frame
    export_package = {
        "export_timestamp": datetime.now(timezone.utc).isoformat(),
        "origin_node": NODE_ADDRESS,
        "total_records": len(ledger_entries),
        "chain_data": ledger_entries
    }

    # 3. Sign the entire export package to anchor authenticity externally
    serialized_package = json.dumps(export_package, sort_keys=True).encode('utf-8')
    key_bytes = bytes.fromhex(PRIVATE_KEY)
    export_signature = hmac.new(key_bytes, serialized_package, hashlib.sha256).hexdigest()

    final_delivery = {
        "export_package": export_package,
        "export_signature": export_signature
    }

    # 4. Write export archive file asset out to the file system directory
    os.makedirs(EXPORT_DIR, exist_ok=True)
    export_filename = f"export_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    target_path = os.path.join(EXPORT_DIR, export_filename)
    
    with open(target_path, 'w') as out:
        json.dump(final_delivery, out, indent=4)
        
    print(f"\n=== [State Export Sealed Successfully] ===")
    print(f"[+] Cryptographic Seal Signature: {export_signature}")
    print(f"[+] Portable Export Package Path: {target_path}")

if __name__ == "__main__":
    run_state_export()
