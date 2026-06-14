import json

def ingest_hospital_ledger(ein, facility_name):
    ledger = {
        "entity": facility_name,
        "ein": ein,
        "source": "IRS_Form_990_Schedule_H",
        "metrics": {
            "total_community_benefit_expense": 0.0,
            "financial_assistance_at_cost": 0.0,
            "total_revenue": 0.0
        },
        "integrity_hash": "SHA-512"
    }
    return json.dumps(ledger, indent=4)

print(ingest_hospital_ledger("75-1977850", "Texas_Health_Cleburne"))
print(ingest_hospital_ledger("45-2694620", "Texas_Health_Huguley"))
