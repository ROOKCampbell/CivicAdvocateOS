#!/usr/bin/env python3
# CivicAdvocate.OS | Multi-Vector Production Batch Committer
# Workflow: Overview -> Code -> Implementation

import os
import sys
import json
import hmac
import hashlib
import urllib.request

# 1. Load Live Environment Context Variables
PRIVATE_KEY = os.getenv("ARCHITECT_PRIVATE_KEY")
NODE_ADDRESS = os.getenv("NODE_ADDRESS")

if not PRIVATE_KEY or not NODE_ADDRESS:
    print("[-] Error: Active cryptographic credentials missing from shell environment.")
    print("[*] Resolution: Execute 'source ~/node.env' before running this tool.")
    sys.exit(1)

# 2. Hardcode Actual Multi-Vector Production Text Datasets
DATASET = {
    "writ_of_mandamus": (
        "07/06/2026 - PETITION FOR WRIT OF MANDAMUS FILED BY RELATOR. "
        "RE: DISTRICT COURT DOCKET NO. 2026-CV-8841. SPECIAL HEARING ASSIGNED TO ADMINISTRATIVE NODE."
    ),
    "environmental_grievance": (
        "FIELD AUDIT LOG - JULY 6, 2026: DISCHARGE CONCENTRATE DETECTED AT VILLAGE CREEK OUTFLOW. "
        "RECORDING VISUAL EVIDENCE FOR COMPLIANCE DEFICIT CASE #VC-2026-A."
    ),
    "unclaimed_property": (
        "COMPLIANCE TRACKING: UNCLAIMED PROPERTY CLAIM SUBMITTED FOR ASSIGNED BENEFICIARY. "
        "STATE REF ID: TX-99214-B. STATUS: UNDER REVIEW."
    )
}

def transmit_package(vector_key, payload):
    """Serializes, signs, and posts packages natively to localhost:8080."""
    serialized = json.dumps(payload, sort_keys=True).encode('utf-8')
    
    # Compute signature block using real key material bytes
    key_bytes = bytes.fromhex(PRIVATE_KEY)
    signature = hmac.new(key_bytes, serialized, hashlib.sha256).hexdigest()
    
    transmission_data = {
        "payload": payload,
        "signer": NODE_ADDRESS,
        "signature": signature
    }
    
    req = urllib.request.Request(
        'http://localhost:8080/v1/ledger/append',
        data=json.dumps(transmission_data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_text = response.read().decode('utf-8')
            print(f"[+] Vector [{vector_key.upper()}]: {res_text}")
    except Exception as e:
        print(f"[-] Vector [{vector_key.upper()}] Transmission Failure: {e}")

def run_batch_pipeline():
    print("=== [CivicAdvocate.OS Batch Execution Commencing] ===")
    print(f"[+] Deploying from Node Authority: {NODE_ADDRESS}\n")
    
    # Process Vector 1: Mandamus Tracking Payload
    mandamus_payload = {
        "network": "mainnet",
        "docket": "2026-CV-8841",
        "action": "WRIT_OF_MANDAMUS_RECORD",
        "raw_text": DATASET["writ_of_mandamus"]
    }
    transmit_package("writ_of_mandamus", mandamus_payload)
    
    # Process Vector 2: Village Creek Environmental Tracking Payload
    environmental_payload = {
        "network": "mainnet",
        "docket": "VC-2026-A",
        "action": "ENVIRONMENTAL_NEGLIGENT_LOG",
        "raw_text": DATASET["environmental_grievance"]
    }
    transmit_package("environmental_grievance", environmental_payload)
    
    # Process Vector 3: Unclaimed Property Verification Payload
    property_payload = {
        "network": "mainnet",
        "docket": "TX-99214-B",
        "action": "UNCLAIMED_PROPERTY_CLAIM",
        "raw_text": DATASET["unclaimed_property"]
    }
    transmit_package("unclaimed_property", property_payload)

    print("\n=== [Batch Injection Complete] ===")

if __name__ == "__main__":
    run_batch_pipeline()
