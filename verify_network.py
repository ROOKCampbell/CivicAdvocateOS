#!/usr/bin/env python3
# CivicAdvocate.OS | Production Node Verification
# Workflow: Overview -> Code -> Implementation

import os
import sys
import json

STATUS_JSON = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/status.json"

def verify_live_state():
    print("=== [Analyzing Production Environment] ===")
    if not os.path.exists(STATUS_JSON):
        print(f"[-] Status matrix file not found at: {STATUS_JSON}")
        sys.exit(1)
        
    with open(STATUS_JSON, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("[-] Error: Status file contains invalid JSON data.")
            sys.exit(1)

    print(f"[+] Active Network Layer: {data.get('network', 'UNKNOWN')}")
    print(f"[+] Verified Ledger Block Height: {data.get('active_block_height', 'UNKNOWN')}")
    print(f"[+] Node Health Profile Status: {data.get('status', 'UNKNOWN')}")
    print("=== [Verification Sequence Complete] ===")

if __name__ == "__main__":
    verify_live_state()
