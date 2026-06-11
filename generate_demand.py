#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone

STRIKE_DIR = os.path.expanduser("~/CivicAdvocate.OS/enforcement_packages")
LEDGER_FILE = os.path.expanduser("~/truth_mandate/ledger/mission_ledger.jsonl")
os.makedirs(STRIKE_DIR, exist_ok=True)

def scan_ledger_for_violations():
    if not os.path.exists(LEDGER_FILE):
        print("[-] Master ledger file not found.")
        return

    print("[*] Processing master ledger file for variance anomalies...")
    violation_count = 0

    with open(LEDGER_FILE, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                payload = record.get("payload_data", {})
                
                v_val = payload.get("variance_detected", 0)
                variance = float(v_val) if v_val is not None else 0.0
                is_flagged = payload.get("commingling_alert_flag", False)
                
                if is_flagged or variance > 0 or record.get("intake_id") == 544:
                    generate_formal_notice(record, payload, variance)
                    violation_count += 1
            except Exception as e:
                continue
                
    print(f"[+] Enforcement Pass Complete. {violation_count} formal default notices active.")

def generate_formal_notice(record, payload, variance):
    audit_id = record.get("audit_id") or "UNK"
    notice_path = os.path.join(STRIKE_DIR, f"NOTICE_OF_DEFAULT_AUDIT_{audit_id}.txt")
    
    if os.path.exists(notice_path):
        return

    notice_content = f"""======================================================================
                  STATEWIDE NOTICE OF NON-COMPLIANCE
======================================================================
ISSUED VIA: CivicAdvocate.OS Forensic Integrity Protocol
TIMESTAMP: {record.get("reset_at", datetime.now(timezone.utc).isoformat())}
AUDIT TRACKING ID: {audit_id}
CRYPTOGRAPHIC ANCHOR (SHA-512): {record.get("checksum")}
----------------------------------------------------------------------
TARGET LAND/MINERAL REGISTER:
Survey: {payload.get("survey", "Silas Elbert Bandy - Abstract 544")}
Lease Anchor ID: {payload.get("lease_id", "544-A")}
Primary Lineage Anchor: Campbell; Bandy (Lynn) absolute
----------------------------------------------------------------------
FORENSIC EVIDENCE FINDINGS:
- Reported Production Volume: {payload.get("reported_bbls", "DATA_STREAM_LOCK")} BBLS
- Allocated System Volume: {payload.get("allocated_bbls", "DATA_STREAM_LOCK")} BBLS
- Unaccounted Variance: {variance} BBLS
- Commingling Status: MONITORING ACTIVE / ACCOUNTABILITY MANDATE
======================================================================
"""
    with open(notice_path, "w") as nf:
        nf.write(notice_content)
    print(f"[!] Compiled Enforcement Strike: NOTICE_OF_DEFAULT_AUDIT_{audit_id}.txt")

if __name__ == "__main__":
    scan_ledger_for_violations()
