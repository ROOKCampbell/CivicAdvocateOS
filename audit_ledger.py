#!/usr/bin/env python3
# CivicAdvocate.OS | Production Ledger Forensic Auditor
# Workflow: Overview -> Code -> Implementation

import os
import json
import hmac
import hashlib

PRIVATE_KEY = os.getenv("ARCHITECT_PRIVATE_KEY")
LEDGER_PATH = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/genesis_ledger.dat"

def audit_stored_ledger():
    print("=== [Commencing Forensic File Integrity Check] ===")
    if not os.path.exists(LEDGER_PATH):
        print(f"[-] Error: Target ledger data file missing at {LEDGER_PATH}")
        return

    if not PRIVATE_KEY:
        print("[-] Warning: ARCHITECT_PRIVATE_KEY environment variable missing.")
        print("[*] Proceeding with structural parsing only. Signature validation skipped.\n")

    with open(LEDGER_PATH, 'r') as f:
        lines = f.readlines()

    print(f"[+] Total Active Entries Found: {len(lines)}")
    print("-" * 60)

    for index, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            payload = entry.get("payload")
            signer = entry.get("signer")
            signature = entry.get("signature")
            
            print(f"Block {index} | Docket: {payload.get('docket', 'N/A')} | Action: {payload.get('action', 'N/A')}")
            print(f"  Signer: {signer}")
            
            if PRIVATE_KEY:
                # Re-verify matching structure serialization rules
                serialized = json.dumps(payload, sort_keys=True).encode('utf-8')
                key_bytes = bytes.fromhex(PRIVATE_KEY)
                expected_sig = hmac.new(key_bytes, serialized, hashlib.sha256).hexdigest()
                
                if hmac.compare_digest(expected_sig, signature):
                    print("  Cryptographic Integrity: [PASSED]")
                else:
                    print("  Cryptographic Integrity: [CORRUPTED/MISMATCH]")
            print("-" * 60)
            
        except Exception as e:
            print(f"[-] Line {index} Error parsing row: {str(e)}")

if __name__ == "__main__":
    audit_stored_ledger()
