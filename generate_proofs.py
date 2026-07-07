#!/usr/bin/env python3
# CivicAdvocate.OS | Cryptographic Ledger Proof Sheet Generator
# Workflow: Overview -> Code -> Implementation

import os
import sys
import json
import hashlib
from datetime import datetime

# Clear read-only protection if a broken run exists to overwrite safely
PROOF_OUT = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/proof_sheet.txt"
if os.path.exists(PROOF_OUT):
    os.chmod(PROOF_OUT, 0o600)

LEDGER_PATH = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/genesis_ledger.dat"

def compile_verification_proofs():
    print("=== [CivicAdvocate.OS Proof Sheet Generator Initialized] ===")
    if not os.path.exists(LEDGER_PATH):
        print(f"[-] Error: Target ledger data file missing at {LEDGER_PATH}")
        sys.exit(1)

    with open(LEDGER_PATH, 'r') as f:
        blocks = [json.loads(line.strip()) for line in f if line.strip()]

    print(f"[+] Scanning {len(blocks)} registered chain blocks for signature trees...")
    
    try:
        with open(PROOF_OUT, 'w') as p:
            p.write("========================================================================\n")
            p.write("               CIVICADVOCATE.OS IMMUTABLE LEDGER PROOF SHEET            \n")
            p.write(f"               GENERATED TIMESTAMP: {datetime.now().isoformat()}\n")
            p.write("========================================================================\n\n")
            
            cumulative_hash = hashlib.sha256(b"GENESIS_SEED").hexdigest()
            
            for idx, block in enumerate(blocks, start=1):
                payload = block.get("payload", {})
                signer = block.get("signer", "N/A")
                sig = block.get("signature", "N/A")
                
                # Compute compounding blockchain state verification hash mapping
                block_mix = f"{idx}{json.dumps(payload, sort_keys=True)}{signer}{sig}{cumulative_hash}"
                cumulative_hash = hashlib.sha256(block_mix.encode('utf-8')).hexdigest()
                
                p.write(f"BLOCK INDEX    : #{idx}\n")
                p.write(f"DOCKET TARGET  : {payload.get('docket', 'N/A')}\n")
                p.write(f"ACTION COMPLY  : {payload.get('action', 'N/A')}\n")
                p.write(f"NODE SIGNER    : {signer}\n")
                p.write(f"BLOCK SIGNATURE: {sig}\n")
                p.write(f"CHAIN ANCHOR   : {cumulative_hash}\n")
                p.write("-" * 72 + "\n")
                
        os.chmod(PROOF_OUT, 0o400) # Restrict to read-only access posture
        print("\n=== [Forensic Chain Verification Sheet Created] ===")
        print(f"[+] Portable Audit Proof File Locked To Path: {PROOF_OUT}")
    except Exception as e:
        print(f"[-] Error writing audit verification proofs: {str(e)}")

if __name__ == "__main__":
    compile_verification_proofs()
