import json

LOG_FILE = "ledger/mission_ledger.jsonl"
OUTPUT_LOG = "ledger/high_velocity_anomalies_full.log"

def recursive_deep_audit():
    # Capture both baseline nodes and high-velocity sink nodes
    nodes_of_interest = ["0544", "0545"]
    with open(LOG_FILE, 'r') as f, open(OUTPUT_LOG, 'w') as out:
        for line in f:
            if line.strip():
                entry = json.loads(line.strip())
                if entry.get("intake_id") in nodes_of_interest:
                    out.write(json.dumps(entry) + "\n")
    print(f"[SYS] Deep recursive scan complete. Data stored in: {OUTPUT_LOG}")

if __name__ == "__main__":
    recursive_deep_audit()
