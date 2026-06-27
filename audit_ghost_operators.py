import csv

def run_audit(production_log, tenure_ledger):
    authorized_operators = set()
    
    # Extract authorized operators from tenure ledger
    with open(tenure_ledger, 'r') as f:
        reader = csv.reader(f)
        try:
            next(reader)  # Skip header
            for row in reader:
                if row and len(row) > 0:
                    authorized_operators.add(row[0].strip())
        except StopIteration:
            pass

    # Check production log for unauthorized operators
    print(f"[AUDIT] Checking production operators against ledger...")
    with open(production_log, 'r') as f:
        for line in f:
            if "|" in line and "API" not in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 2:
                    op_id, api = parts[0], parts[1]
                    if op_id not in authorized_operators:
                        print(f"[ALERT] Unauthorized Operator Found: {op_id} | API: {api}")

if __name__ == "__main__":
    run_audit('rrc_cleburne_production.log', 'bandy_survey_tenure.csv')
