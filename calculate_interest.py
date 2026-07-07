#!/usr/bin/env python3
# CivicAdvocate.OS | Statutory Interest Compounding Engine
# Workflow: Overview -> Code -> Implementation

import os
import sys
import json
import urllib.request
import hmac
import hashlib
from datetime import datetime, date, timezone

PRIVATE_KEY = os.getenv("ARCHITECT_PRIVATE_KEY")
NODE_ADDRESS = os.getenv("NODE_ADDRESS")

# Absolute Forensic Claim Accounting Parameters
PRINCIPAL_CLAIM = 128603.70  # RRC-Verified Suspense Principal Value
DAILY_ACCRUAL_RATE = 42.28   # Standard Daily Accrual Metric ($42.28/day baseline)
ANNUAL_RATE = 0.12           # 12% Statutory Suspense Interest under TX Nat. Res. Code § 91.402
CLAIM_START_DATE = date(2026, 4, 10) # Liquidated Demand Service Date Lock

def execute_interest_audit():
    print("=== [CivicAdvocate.OS Statutory Financial Accounting Engine] ===")
    if not PRIVATE_KEY or not NODE_ADDRESS:
        print("[-] Error: Active cryptographic credentials missing from shell environment.")
        sys.exit(1)

    today = datetime.now(timezone.utc).date()
    elapsed_days = (today - CLAIM_START_DATE).days
    
    if elapsed_days < 0:
        elapsed_days = 0

    # Calculate exact simple interest accrued on withheld funds at statutory rate
    statutory_interest = PRINCIPAL_CLAIM * (ANNUAL_RATE * (elapsed_days / 365.25))
    total_due_valuation = PRINCIPAL_CLAIM + statutory_interest
    daily_calculated_delta = (PRINCIPAL_CLAIM * ANNUAL_RATE) / 365.25

    print(f"[+] Principle Suspension Baseline : ${PRINCIPAL_CLAIM:,.2f}")
    print(f"[+] Liquidated Claim Start Date    : {CLAIM_START_DATE}")
    print(f"[+] Active Accounting Elapsed Time : {elapsed_days} Days Out from Service")
    print(f"[+] Statutory Suspense Interest (12%): ${statutory_interest:,.2f}")
    print(f"[+] True Updated Financial Demand  : ${total_due_valuation:,.2f}")
    print(f"[+] Derived Daily Accrual Speed   : ${daily_calculated_delta:.2f}/day (Target Baseline: ${DAILY_ACCRUAL_RATE:.2f}/day)")

    # Package metrics payload for Mainnet submission block
    payload = {
        "network": "mainnet",
        "docket": "ABSTRACT-544-FINANCIAL",
        "action": "STATUTORY_INTEREST_FLUSH",
        "accounting_metrics": {
            "elapsed_epoch_days": elapsed_days,
            "accrued_statutory_interest": round(statutory_interest, 2),
            "total_liquidated_demand": round(total_due_valuation, 2),
            "daily_accrual_yield": round(daily_calculated_delta, 2)
        }
    }

    # Asymmetrically sign and broadcast the update package
    serialized = json.dumps(payload, sort_keys=True).encode('utf-8')
    sig = hmac.new(bytes.fromhex(PRIVATE_KEY), serialized, hashlib.sha256).hexdigest()
    
    package = {"payload": payload, "signer": NODE_ADDRESS, "signature": sig}
    
    req = urllib.request.Request(
        'http://localhost:8080/v1/ledger/append',
        data=json.dumps(package).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as res:
            print(f"\n[+] Financial State Flush Complete: {res.read().decode('utf-8').strip()}")
    except Exception as e:
        print(f"\n[-] Failed auto-committing financial flush block: {e}")

if __name__ == "__main__":
    execute_interest_audit()
