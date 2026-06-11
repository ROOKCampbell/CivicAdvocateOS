#!/usr/bin/env python3
import os
import json
import psycopg2
import sys

DB_NAME = "u0_a540"
DB_USER = "u0_a540"
STRIKE_DIR = os.path.expanduser("~/forensic_strikes")

def audit_stored_records():
    print("[*] Launching ledger verification sequence...")
    if not os.path.exists(STRIKE_DIR):
        print("[!] Strike directory missing. No files to verify.")
        return

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER)
        cursor = conn.cursor()
    except Exception as e:
        print(f"[!] Database connection failure: {e}")
        sys.exit(1)

    corrupted_nodes = 0
    verified_nodes = 0

    for filename in os.listdir(STRIKE_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(STRIKE_DIR, filename)
            
            with open(file_path, 'r') as f:
                try:
                    file_data = json.load(f)
                    file_hash = file_data.get("sha512_checksum")
                    audit_id = file_data.get("audit_id")
                except Exception:
                    print(f"[!!] Malformed JSON file: {filename}")
                    corrupted_nodes += 1
                    continue

            # Query database state
            cursor.execute("SELECT checksum FROM public.reaper_audit WHERE audit_id = %s;", (audit_id,))
            db_record = cursor.fetchone()

            if not db_record:
                print(f"[!!] TAMPER DETECTED: Audit ID {audit_id} missing from database (Orphaned File: {filename})")
                corrupted_nodes += 1
            elif db_record[0].strip() != file_hash:
                print(f"\n\a[!!] CRITICAL INTEGRITY MISMATCH: Audit ID {audit_id} hash drift detected!"); os.system("termux-notification -t "CRITICAL: Ledger Drift" -c "Audit ID " + str(audit_id) + " has been compromised."")
                corrupted_nodes += 1
            else:
                verified_nodes += 1

    cursor.close()
    conn.close()

    print("\n==================================================")
    print(f"[+] AUDIT COMPLETE. Verified: {verified_nodes} | Corrupted/Altered: {corrupted_nodes}")
    print("==================================================")
    
    if corrupted_nodes > 0:
        sys.exit(1)

if __name__ == "__main__":
    audit_stored_records()
