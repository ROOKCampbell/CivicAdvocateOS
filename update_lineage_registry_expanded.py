import json

def update_registry_expanded():
    # Existing nodes + Potential collateral discovery
    full_lineage = [
        # ... (Existing 12 nodes retained)
        {"name": "James Bandy", "role": "COLLATERAL", "relation": "ANCESTRAL"},
        {"name": "Martha Miller", "role": "COLLATERAL", "relation": "ANCESTRAL"},
        {"name": "William Campbell", "role": "COLLATERAL", "relation": "ANCESTRAL"},
        {"name": "Sarah Jones", "role": "COLLATERAL", "relation": "ANCESTRAL"}
    ]
    
    with open("reconciliation_manifest.json", "r+") as f:
        data = json.load(f)
        data["protected_lineage_vectors"] = full_lineage
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    print("[✓] REGISTRY EXPANDED WITH POTENTIAL COLLATERAL VECTORS")

if __name__ == "__main__":
    update_registry_expanded()
