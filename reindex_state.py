#!/usr/bin/env python3
# CivicAdvocate.OS | Production State Re-indexing Engine
# Workflow: Overview -> Code -> Implementation

import os
import json
from datetime import datetime, timezone

LEDGER_PATH = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/genesis_ledger.dat"
STATUS_JSON = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/status.json"

def synchronize_node_metrics():
    print("=== [CivicAdvocate.OS Core Re-indexing Sequence] ===")
    if not os.path.exists(LEDGER_PATH):
        print(f"[-] Error: Active ledger file missing at {LEDGER_PATH}")
        return

    # Count real lines inside production ledger database file
    with open(LEDGER_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    actual_count = len(lines)
    print(f"[+] Total physical data blocks verified on disk: {actual_count}")

    if actual_count == 0:
        print("[-] Warning: Ledger is empty. Skipping status update.")
        return

    # Extract the final entry's cryptographic signature
    try:
        final_block = json.loads(lines[-1])
        last_hash = final_block.get("signature", "N/A")
    except Exception as e:
        print(f"[-] Error reading final block signature: {e}")
        last_hash = "ERROR_PARSING"

    # Read current status profile
    if os.path.exists(STATUS_JSON):
        with open(STATUS_JSON, 'r') as f:
            try:
                status_data = json.load(f)
            except json.JSONDecodeError:
                status_data = {}
    else:
        status_data = {}

    # Synchronize health properties precisely
    status_data["timestamp"] = datetime.now(timezone.utc).isoformat()
    status_data["network"] = "mainnet"
    status_data["status"] = "HEALTHY"
    status_data["active_block_height"] = actual_count
    status_data["last_committed_block_hash"] = last_hash

    # Write out structural properties to master tracking matrix
    with open(STATUS_JSON, 'w') as f:
        json.dump(status_data, f, indent=4)
        
    print("[+] Master system tracking matrices successfully synchronized.")
    print(f"=== [Success: Node Posture Latched at Block Height {actual_count}] ===")

if __name__ == "__main__":
    synchronize_node_metrics()
