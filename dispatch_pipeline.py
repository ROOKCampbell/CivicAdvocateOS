#!/usr/bin/env python3
import hashlib
import json
import os
import sys
import stat

LEDGER_FILE = "ledger/mission_ledger.jsonl"
GENESIS_SIGNATURE = "460596395ba5791761e2e1a3848b598d9f1f0a078d78f244589f6674681329be608a1563be8254c793260907d8966c8882583271787889364584282e38c5211d"

def verify_ledger_integrity():
    if not os.path.exists(LEDGER_FILE):
        print(f"[-] Error: {LEDGER_FILE} not found.")
        sys.exit(1)
    
    with open(LEDGER_FILE, 'rb') as f:
        content = f.read()
    
    current_hash = hashlib.sha512(content).hexdigest()
    print(f"[+] Current Ledger Integrity SHA-512 Hash generated.")
    return current_hash

def toggle_write_protection(enable=True):
    action = "Locking (Read-Only)" if enable else "Unlocking (Writeable)"
    print(f"[*] {action} ledger file...")
    try:
        if enable:
            # Set file permissions to Owner Read-Only (0o400)
            os.chmod(LEDGER_FILE, stat.S_IREAD)
            print(f"[+] Successfully write-protected {LEDGER_FILE}")
        else:
            # Set file permissions to Owner Read-Write (0o600)
            os.chmod(LEDGER_FILE, stat.S_IREAD | stat.S_IWRITE)
            print(f"[+] Successfully unlocked {LEDGER_FILE}")
    except Exception as e:
        print(f"[-] Failed to toggle lock: {e}")
        sys.exit(1)

def append_sign_off_entry():
    sign_off_payload = {
        "event": "TIER_3_FINAL_DISPATCH_SIGN_OFF",
        "survey": "Silas Elbert Bandy Survey (Abstract 544)",
        "status": "DISPATCHED",
        "genesis_anchor": GENESIS_SIGNATURE,
        "dispatch_targets": ["SEC", "DOJ", "DOE"]
    }
    
    with open(LEDGER_FILE, 'a') as f:
        f.write(json.dumps(sign_off_payload) + "\n")
    print("[+] Final dispatch block appended to ledger.")

if __name__ == "__main__":
    print("[*] Initializing CivicAdvocate.OS Dispatch Sequence (User-Space)...")
    
    # 1. Verify file exists and trace integrity
    verify_ledger_integrity()
    
    # 2. Temporarily unlock file permissions
    toggle_write_protection(enable=False)
    
    try:
        # 3. Commit the dispatch sign-off record
        append_sign_off_entry()
    finally:
        # 4. Immediately re-seal file permissions
        toggle_write_protection(enable=True)
        
    print("[+] Sequence complete. Ledger successfully updated and locked.")
