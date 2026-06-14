import json
import os

# Paths defined by mission parameters
LEDGER_PATH = "municipal_data/forensic_ledger.json"
OUTPUT_FILE = os.path.expanduser("~/CivicAdvocate.OS/Direct_Accounting_2026-06-11.txt")

def update_accounting():
    total_volume = 0.0
    
    # Process Mission Ledger
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    total_volume += float(entry.get("drainage_volume", 0))
                except (ValueError, TypeError):
                    continue

    royalty_deficit = total_volume * 0.125
    total_liability = royalty_deficit * 1.05

    # Update Direct Accounting Report
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as f:
            data = f.read()
        
        data = data.replace("[PENDING_INPUT_REF]", f"{total_volume:.2f}")
        data = data.replace("[CALCULATED_VAL]", f"{royalty_deficit:.2f}")
        data = data.replace("[FINAL_SUM]", f"{total_liability:.2f}")
        data = data.replace("[STATED_RATE]", "5.0%")

        with open(OUTPUT_FILE, 'w') as f:
            f.write(data)
        print("Accounting report finalized successfully.")
    else:
        print("Error: Accounting file not found.")

if __name__ == "__main__":
    update_accounting()
