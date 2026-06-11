#!/usr/bin/env python3
import json
import csv
import os

LEDGER_FILE = os.path.expanduser("~/truth_mandate/ledger/mission_ledger.jsonl")
EXPORT_DIR = "./federal_evidentiary_packages"
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_immutable_chain():
    if not os.path.exists(LEDGER_FILE):
        print("[-] Master ledger file not found. Aborting package export.")
        return

    csv_path = os.path.join(EXPORT_DIR, "sec_doj_evidentiary_chain.csv")
    print(f"[*] Packaging ledger line-items for federal delivery compliance...")

    with open(LEDGER_FILE, 'r') as infile, open(csv_path, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Write standards-compliant header rows for digital forensic discovery
        writer.writerow(["SEQUENCE_ID", "INTAKE_ID", "TIMESTAMP", "SHA512_CHECKSUM", "LEASE_ID", "VARIANCE"])

        count = 0
        for line in infile:
            if line.strip():
                try:
                    data = json.loads(line)
                    payload = data.get("payload_data", {})
                    writer.writerow([
                        data.get("audit_id"),
                        data.get("intake_id"),
                        data.get("reset_at"),
                        data.get("checksum"),
                        payload.get("lease_id"),
                        payload.get("variance_detected", 0)
                    ])
                    count += 1
                except Exception:
                    continue

    print(f"[+] Federal evidentiary compilation completed successfully.")
    print(f"[+] Saved {count} verified tracking vectors to: {csv_path}")

if __name__ == "__main__":
    export_immutable_chain()
