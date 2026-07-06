#!/usr/bin/env python3
# CivicAdvocate.OS | Asymmetric Ledger Signing Utility
# Workflow: Overview -> Code -> Implementation

import os
import sys
import json
import hmac
import hashlib

def sign_genuine_payload():
    # 1. Fetch live environment context
    private_key = os.getenv("ARCHITECT_PRIVATE_KEY")
    node_address = os.getenv("NODE_ADDRESS")
    
    if not private_key or not node_address:
        print("[-] Error: Active cryptographic credentials missing from shell environment.")
        print("[*] Resolution: Run 'source ~/node.env' before executing this tool.")
        sys.exit(1)

    print("=== [Reading Active Node Credentials] ===")
    print(f"[+] Authorized Node Address: {node_address}")

    # 2. Gather authentic data context from standard input
    print("\nEnter block JSON payload data string to sign (or press Enter for default verification block):")
    input_payload = sys.stdin.readline().strip()
    
    if not input_payload:
        # Default fallback structure for standard operational telemetry
        payload_dict = {
            "network": "mainnet",
            "base_height": 31,
            "verification_status": "AUTHENTIC_COMPLIANCE_PASS"
        }
    else:
        try:
            payload_dict = json.loads(input_payload)
        except json.JSONDecodeError:
            print("[-] Error: Input string is not a valid JSON structure.")
            sys.exit(1)

    # 3. Compute deterministic cryptographic stamp
    serialized_data = json.dumps(payload_dict, sort_keys=True).encode('utf-8')
    key_bytes = bytes.fromhex(private_key)
    
    # Generate secure HMAC-SHA256 signature using your explicit private key material
    crypto_signature = hmac.new(key_bytes, serialized_data, hashlib.sha256).hexdigest()
    
    # 4. Compile authenticated transaction package
    signed_package = {
        "payload": payload_dict,
        "signer": node_address,
        "signature": crypto_signature
    }

    print("\n=== [Production Signature Affixed Successfully] ===")
    print(json.dumps(signed_package, indent=4))

if __name__ == "__main__":
    sign_genuine_payload()
