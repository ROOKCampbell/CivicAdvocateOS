import json

def update_registry():
    full_lineage = [
        {"name": "Delbert Lee Campbell", "role": "FATHER", "relation": "PATERNAL"},
        {"name": "Laura Marie Jones", "role": "MOTHER", "relation": "MATERNAL"},
        {"name": "Oscar Campbell", "role": "GRANDFATHER", "relation": "PATERNAL"},
        {"name": "Elsie Campbell", "role": "GRANDMOTHER", "relation": "PATERNAL"},
        {"name": "Cary Lynn Bandy", "role": "GRANDFATHER", "relation": "MATERNAL"},
        {"name": "Robert Cary Bandy", "role": "GREAT_GRANDFATHER", "relation": "MATERNAL"},
        {"name": "Winona Taylor", "role": "GRANDMOTHER", "relation": "MATERNAL"},
        {"name": "Elizabeth Miller", "role": "ANCESTOR", "relation": "MATERNAL"},
        {"name": "Silas Elbert Bandy", "role": "PATRIARCH", "relation": "ANCESTRAL_ROOT"},
        {"name": "Justin Lee Campbell", "role": "BROTHER", "relation": "SIBLING"},
        {"name": "Travis Wayne Campbell", "role": "BROTHER", "relation": "SIBLING"},
        {"name": "Kayleah Marie Campbell", "role": "DAUGHTER", "relation": "SUCCESSOR"}
    ]
    
    with open("reconciliation_manifest.json", "w") as f:
        json.dump({"protected_lineage_vectors": full_lineage}, f, indent=2)
    print("[✓] REGISTRY RECONSTRUCTED WITH CORRECTED LINEAGE: KAYLEAH MARIE CAMPBELL")

if __name__ == "__main__":
    update_registry()
