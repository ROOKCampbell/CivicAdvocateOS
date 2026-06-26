import hashlib
import json
import os

class TruthMandateLedger:
    def __init__(self, ledger_path="ledger.json"):
        self.ledger_path = ledger_path
        self.ledger = self._load_ledger()

    def _load_ledger(self):
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                return json.load(f)
        return {}

    def log_entry(self, entry_id, data):
        self.ledger[entry_id] = data
        with open(self.ledger_path, 'w') as f:
            json.dump(self.ledger, f, indent=4)
        print(f"Record successfully ingested: {entry_id[:16]}...")

if __name__ == "__main__":
    ledger = TruthMandateLedger()
    print("TruthMandateLedger initialized.")
