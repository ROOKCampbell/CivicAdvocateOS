#!/usr/bin/env python3
import os
import json
import hashlib

STRIKE_DIR = os.path.expanduser("~/forensic_strikes")
MASTER_LEDGER = "/data/data/com.termux/files/home/truth_mandate/ledger/mission_ledger.jsonl"

def synchronize_master_ledger():
    if not os.path.exists(STRIKE_DIR):
        return

    # Gather existing synced IDs from the immutable ledger file
    synced_ids = set()
    if os.path.exists(MASTER_LEDGER):
        with open(MASTER_LEDGER, 'r') as ml:
            for line in ml:
                if line.strip():
                    try:
                        synced_ids.add(json.loads(line)["audit_id"])
                    except Exception:
                        continue

    # Process outstanding strikes sequentially
    for filename in sorted(os.listdir(STRIKE_DIR)):
        if filename.endswith(".json"):
            file_path = os.path.join(STRIKE_DIR, filename)
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                    audit_id = data["audit_id"]
                except Exception:
                    continue

            # Append structural data line if not already locked into the master ledger
            if audit_id not in synced_ids:
                with open(MASTER_LEDGER, 'a') as ml:
                    ml.write(json.dumps(data) + "\n")
                print(f"[+] Synced Audit ID {audit_id} to Master Ledger.")

if __name__ == "__main__":
    synchronize_master_ledger()
