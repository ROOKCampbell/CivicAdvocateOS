import json
from datetime import datetime

# Define your custom Fee Schedule
FEE_SCHEDULE = {
    "forensic_audit_service": 500.00,  # Base fee per Abstract 544 audit
    "federal_strike_package_compilation": 1500.00,
    "succession_lineage_verification": 750.00,
    "notice_of_default_filing": 300.00,
    "currency": "USD"
}

def generate_fee_statement(service_id):
    statement = {
        "timestamp": datetime.now().isoformat(),
        "service": service_id,
        "fee": FEE_SCHEDULE.get(service_id, 0.00),
        "status": "ACCRUED"
    }
    return statement

def update_ledger_with_fees():
    # Append fee statement to the primary strike package
    try:
        with open("federal_strike_package_v1.json", "r") as f:
            package = json.load(f)
            
        # Inject fee structure into the meta-data or audit trail
        package["billing_ledger"] = {
            "current_accruals": [generate_fee_statement("forensic_audit_service")],
            "total_accrued": FEE_SCHEDULE["forensic_audit_service"]
        }
        
        with open("federal_strike_package_v1.json", "w") as f:
            json.dump(package, f, indent=2)
            
        print("[✓] FEE SCHEDULE INTEGRATED INTO FEDERAL STRIKE PACKAGE")
    except Exception as e:
        print(f"[!] FEE RECONCILIATION ERROR: {str(e)}")

if __name__ == "__main__":
    update_ledger_with_fees()
