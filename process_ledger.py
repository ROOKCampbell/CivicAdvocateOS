import os

LOG_PATH = os.path.expanduser("~/CivicAdvocate.OS/rrc_cleburne_production.log")
OUTPUT_FILE = os.path.expanduser("~/CivicAdvocate.OS/Direct_Accounting_2026-06-11.txt")

def update_accounting():
    total_volume = 0.0
    
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as f:
            for line in f:
                # Skip header and separator lines
                if "|" in line and "Operator_ID" not in line and "-" not in line:
                    parts = line.split("|")
                    try:
                        # Index 2 is Production_Volume_MCF
                        total_volume += float(parts[2].strip())
                    except (ValueError, IndexError):
                        continue

    royalty_deficit = total_volume * 0.125
    total_liability = royalty_deficit * 1.05

    with open(OUTPUT_FILE, 'r') as f:
        data = f.read()
    
    data = data.replace("[PENDING_INPUT_REF]", f"{total_volume:.2f}")
    data = data.replace("[CALCULATED_VAL]", f"{royalty_deficit:.2f}")
    data = data.replace("[FINAL_SUM]", f"{total_liability:.2f}")

    with open(OUTPUT_FILE, 'w') as f:
        f.write(data)
    print("Accounting report finalized with production volume data.")

if __name__ == "__main__":
    update_accounting()
