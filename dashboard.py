#!/usr/bin/env python3
# CivicAdvocate.OS | Production Forensic Dashboard Interface
# Workflow: Overview -> Code -> Implementation

import os
import sys
import json
from datetime import datetime

STATUS_JSON = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/status.json"
LEDGER_PATH = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/genesis_ledger.dat"

def render_dashboard():
    # Clear screen and position cursor to top-left natively
    sys.stdout.write("\033[2J\033[H")
    
    print("================================================================================")
    print("                      CIVICADVOCATE.OS FORENSIC MONITORING UI                   ")
    print("================================================================================")
    
    # 1. Parse Status Metrics
    if os.path.exists(STATUS_JSON):
        with open(STATUS_JSON, 'r') as f:
            try:
                status = json.load(f)
            except:
                status = {}
    else:
        status = {}
        
    print(f" NETWORK:  [{status.get('network', 'UNKNOWN').upper()}]  |  HEALTH STATE: [{status.get('status', 'OFFLINE')}]")
    print(f" NODE REF: {status.get('last_committed_block_hash', 'N/A')[:32]}...")
    print(f" LATCH TIME: {status.get('timestamp', 'N/A')}")
    print("================================================================================")
    
    # 2. Parse Historical Blocks
    if not os.path.exists(LEDGER_PATH):
        print("[-] Active Mainnet ledger storage file not detected on disk.")
        return
        
    with open(LEDGER_PATH, 'r') as f:
        blocks = [json.loads(line.strip()) for line in f if line.strip()]
        
    print(f" TOTAL COMMITTED BLOCK HEIGHT: {len(blocks)} BLOCKS REGISTERED")
    print("--------------------------------------------------------------------------------")
    print(f" {'BLOCK':<6} | {'DOCKET TARGET':<15} | {'ACTION TYPE':<25} | {'SIGNER'} ")
    print("--------------------------------------------------------------------------------")
    
    # Display the final 8 blocks for clean, high-density terminal layout tracking
    for idx, b in enumerate(blocks[-8:], start=max(1, len(blocks) - 7)):
        payload = b.get("payload", {})
        signer = b.get("signer", "N/A")
        print(f" #{idx:<5} | {payload.get('docket', 'N/A'):<15} | {payload.get('action', 'N/A'):<25} | {signer[:14]}...")
        
    print("================================================================================")
    print(" [Actions]: Press Ctrl+C to exit dashboard tracking visualization frame.")

if __name__ == "__main__":
    try:
        render_dashboard()
    except KeyboardInterrupt:
        sys.exit(0)
