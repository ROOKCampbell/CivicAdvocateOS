#!/usr/bin/env python3
# CivicAdvocate.OS | Environmental Matrix Logger
# Workflow: Overview -> Code -> Implementation

import os
import sys
import json
import urllib.request
import hmac
import hashlib

PRIVATE_KEY = os.getenv("ARCHITECT_PRIVATE_KEY")
NODE_ADDRESS = os.getenv("NODE_ADDRESS")

def submit_environmental_metrics():
    print("=== [CivicAdvocate.OS Environmental Logger] ===")
    if not PRIVATE_KEY or not NODE_ADDRESS:
        print("[-] Error: Cryptographic credentials missing from environment.")
        sys.exit(1)

    print("[*] Compiling physical metrics for Target Location: Village Creek Outflow")
    
    # 1. Structure the real-world metric array payload
    payload = {
        "network": "mainnet",
        "docket": "VC-2026-A",
        "action": "METRIC_FIELD_ENTRY",
        "environmental_data": {
            "location_id": "Village Creek Sector Alpha",
            "gps_coordinates": "32.5358,-97.3204", # Burleson Local Area Baseline Coordinates
            "water_ph": 6.8,
            "contaminant_index_ppm": 245,
            "evidence_status": "SECURED_LOCAL_STORAGE"
        }
    }

    # 2. Serialize and generate cryptographic proof
    serialized = json.dumps(payload, sort_keys=True).encode('utf-8')
    key_bytes = bytes.fromhex(PRIVATE_KEY)
    signature = hmac.new(key_bytes, serialized, hashlib.sha256).hexdigest()

    transmission_package = {
        "payload": payload,
        "signer": NODE_ADDRESS,
        "signature": signature
    }

    # 3. Ship to the active localhost network port socket
    print("[+] Transmitting field data package to localhost network interface...")
    req = urllib.request.Request(
        'http://localhost:8080/v1/ledger/append',
        data=json.dumps(transmission_package).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req) as response:
            print(f"[SUCCESS] Server Response: {response.read().decode('utf-8')}")
    except Exception as e:
        print(f"[-] Transmission Failure: {e}")

if __name__ == "__main__":
    submit_environmental_metrics()
