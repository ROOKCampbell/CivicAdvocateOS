import json
import os

SOURCE = os.path.expanduser("~/CivicAdvocate.OS/ledger/mission_ledger.jsonl")
OUTPUT = os.path.expanduser("~/CivicAdvocate.OS/ledger/high_velocity_anomalies_full.log")

def extract_all():
    # Targets corrected to integer values
    targets = [544, 545]
    count = 0
    with open(SOURCE, 'r') as f, open(OUTPUT, 'w') as out:
        for line in f:
            if line.strip():
                try:
                    entry = json.loads(line.strip())
                    # Integer comparison to match ledger structure
                    if int(entry.get("intake_id", 0)) in targets:
                        out.write(json.dumps(entry) + "\n")
                        count += 1
                except (json.JSONDecodeError, ValueError):
                    continue
    print(f"[SYS] Extraction complete. Total nodes identified: {count}")

if __name__ == "__main__":
    extract_all()
