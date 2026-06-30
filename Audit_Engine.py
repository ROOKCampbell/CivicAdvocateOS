import os
from pathlib import Path

ARCHIVE = Path("/data/data/com.termux/files/home/CivicAdvocate.OS/ledger/text_archive")
ROOT_NODE = "CAMPBELL; BANDY (LYNN)"

# Multi-file scope
target_nodes = [
    "Forensic_Audit_Report_Bandy_Survey.txt",
    "Forensic_Tax_Roll_Drainage_1870s.txt",
    "Forensic_Master_Ledger_Reconciliation.txt",
    "_05272025-2111.txt"
]

def run_reconciliation():
    print(f"--- INITIATING MULTI-NODE RECONCILIATION ---")
    print(f"ROOT KEY: {ROOT_NODE}\n")
    
    for filename in target_nodes:
        filepath = ARCHIVE / filename
        if not filepath.exists():
            print(f"[!] MISSING: {filename}")
            continue
            
        with open(filepath, 'r', errors='ignore') as f:
            content = f.read()
            # Verify compliance with the root node
            if ROOT_NODE not in content.upper():
                print(f"[!] COMPLIANCE FAILURE: {filename}")
            else:
                print(f"[+] COMPLIANCE VERIFIED: {filename}")

if __name__ == "__main__":
    run_reconciliation()
