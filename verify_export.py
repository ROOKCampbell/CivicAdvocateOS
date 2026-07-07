#!/usr/bin/env python3
# CivicAdvocate.OS | External Export Package Verifier
# Workflow: Overview -> Code -> Implementation

import sys
import json
import hmac
import hashlib

def verify_external_package(file_path):
    print(f"=== [Analyzing External Export Package: {os.path.basename(file_path)}] ===")
    if not os.path.exists(file_path):
        print(f"[-] Error: Target export file missing at: {file_path}")
        return

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("[-] Error: Target file does not contain valid structured JSON data.")
            return

    export_package = data.get("export_package")
    export_signature = data.get("export_signature")
    
    if not export_package or not export_signature:
        print("[-] Error: Missing package data or cryptographic signature components.")
        return

    # Prompt user for the expected public/private key material to check the signature against
    print("[*] Enter the ARCHITECT_PRIVATE_KEY Hex String used to sign this package:")
    private_key_input = sys.stdin.readline().strip()
    
    if not private_key_input:
        print("[-] Error: Key input cannot be blank. Aborting verification.")
        return

    try:
        # Re-serialize the inner data frame exactly how the exporter sorted it
        serialized_package = json.dumps(export_package, sort_keys=True).encode('utf-8')
        key_bytes = bytes.fromhex(private_key_input)
        
        # Calculate expected signature match
        expected_signature = hmac.new(key_bytes, serialized_package, hashlib.sha256).hexdigest()
        
        print("\n=== [Cryptographic Analysis Complete] ===")
        print(f"[+] Authorized Node Origin : {export_package.get('origin_node')}")
        print(f"[+] Export Timestamp       : {export_package.get('export_timestamp')}")
        print(f"[+] Total Verified Blocks  : {export_package.get('total_records')}")
        
        if hmac.compare_digest(expected_signature, export_signature):
            print("\n[SUCCESS] CRITICAL DATA INTEGRITY MATCH: THIS EXPORT PACKAGE IS AUTHENTIC.")
        else:
            print("\n[CRITICAL FAILURE] SIGNATURE MISMATCH: THIS EXPORT PACKAGE HAS BEEN ALTERED OR CORRUPTED.")
            
    except Exception as e:
        print(f"[-] Error executing signature validation loop: {str(e)}")

import os
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[-] Error: Missing file path parameter argument.")
        print("Usage: python3 verify_export.py <path_to_export_file.json>")
    else:
        verify_external_package(sys.argv[1])
