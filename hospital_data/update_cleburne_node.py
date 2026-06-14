import json

# Replace these placeholders with actual extracted figures
cleburne_metrics = {
    "total_community_benefit_expense": 4229254.20, # Example 5% of Revenue
    "financial_assistance_at_cost": 2100000.00,
    "total_revenue": 84585084.00
}

with open('cleburne_audit.json', 'w') as f:
    json.dump(cleburne_metrics, f)
