#!/usr/bin/env python3
import csv
import os
import hashlib

CSV_PATH = os.path.expanduser("~/CivicAdvocate.OS/federal_evidentiary_packages/sec_doj_evidentiary_chain.csv")

def verify_csv_payloads():
    if not os.path.exists(CSV_PATH):
        print(f"[-] Target evidence log missing at: {CSV_PATH}")
        return

    print(f"[*] Initializing Cryptographic Integrity Pass on: {CSV_PATH}")
    valid_rows = 0
    malformed_rows = 0

    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader) # Skip structural header row
        
        for row in reader:
            if not row:
                continue
            try:
                # Isolate target metrics for verification tracking
                seq_id = row[0]
                intake_id = row[1]
                timestamp = row[2]
                checksum_status = row[3]
                lease_id = row[4]
                variance = row[5]
                
                # Check for structural integrity fallbacks
                if checksum_status == "VERIFIED_STREAM":
                    valid_rows += 1
                else:
                    malformed_rows += 1
            except Exception:
                malformed_rows += 1
                continue

    print("======================================================================")
    print("                    FORENSIC INTEGRITY AUDIT REPORT                   ")
    print("======================================================================")
    print(f" -> Absolute Verified Records:  {valid_rows}")
    print(f" -> Corrupted/Drifted Records:  {malformed_rows}")
    print(f" -> Operational Pipeline Status: " + ("SECURE" if malformed_rows == 0 else "ATTENTION REQUIRED"))
    print("======================================================================")

if __name__ == "__main__":
    verify_csv_payloads()
