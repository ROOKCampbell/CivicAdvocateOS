#!/usr/bin/env python3
import hashlib
import json
import os
import datetime

LEDGER_FILE = "audit_ledger.json"

class LedgerBridge:
    def __init__(self):
        self.ledger = self._load_ledger()

    def _load_ledger(self):
        if os.path.exists(LEDGER_FILE):
            with open(LEDGER_FILE, 'r') as f:
                return json.load(f)
        return []

    def add_entry(self, case_id, abstract_id, survey_name, notes=""):
        timestamp = str(datetime.datetime.now())
        entry = {
            "timestamp": timestamp,
            "case_id": case_id,
            "abstract_id": abstract_id,
            "survey_name": survey_name,
            "notes": notes
        }
        
        # Generate SHA-512 Hash for immutability
        entry_string = json.dumps(entry, sort_keys=True)
        entry['hash'] = hashlib.sha512(entry_string.encode()).hexdigest()
        
        self.ledger.append(entry)
        self._save_ledger()
        print(f"[+] Entry Secured: {case_id} -> {abstract_id}")

    def _save_ledger(self):
        with open(LEDGER_FILE, 'w') as f:
            json.dump(self.ledger, f, indent=4)

if __name__ == "__main__":
    bridge = LedgerBridge()
    print("--- Ledger Bridge Operational ---")
    case = input("Enter Case ID: ")
    abs_id = input("Enter Abstract/Tract ID: ")
    survey = input("Enter Survey Name: ")
    notes = input("Audit Notes: ")
    
    bridge.add_entry(case, abs_id, survey, notes)
