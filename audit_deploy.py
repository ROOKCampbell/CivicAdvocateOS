import hashlib
import json
from datetime import datetime, timezone

def get_hash(data):
    return hashlib.sha512(json.dumps(data, sort_keys=True).encode()).hexdigest()

def process_node(record_id, raw_data, truth_data):
    ledger_file = "forensic_ledger.json"
    status = "CONFIRMED" if raw_data == truth_data else "BREACH_DETECTED"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "record_id": record_id,
        "status": status,
        "hash": get_hash(raw_data)
    }
    with open(ledger_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry

if __name__ == "__main__":
    record = {"survey": "Silas Elbert Bandy", "status": "fiduciary_default"}
    truth = {"survey": "Silas Elbert Bandy", "status": "settled"}
    report = process_node("CLEBURNE_SURVEY_001", record, truth)
    print(f"AUDIT_RESULT: {report['status']} | HASH: {report['hash'][:16]}...")
