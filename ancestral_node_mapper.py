import json

def add_family_member(name, role, relation_type):
    with open("reconciliation_manifest.json", "r+") as f:
        data = json.load(f)
        
        member_node = {
            "name": name,
            "role": role,
            "relationship": relation_type,
            "status": "ANCESTRAL_ANCHOR_VERIFIED"
        }
        
        # Add to the manifest as a distinct Forensic Ancestral Unit
        data["anchored_entries"].append(f"[ANCESTRAL_UNIT] | DATA: {json.dumps(member_node)}")
        
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    print(f"[✓] ANCHORED ANCESTRAL VECTOR: {name} ({role})")

if __name__ == "__main__":
    # Expand to include the full family architecture
    family_members = [
        ("Winona Taylor", "ROOT_ANCESTOR", "MATERNAL"),
        ("Elizabeth Miller", "ROOT_ANCESTOR", "MATERNAL"),
        ("Laura Marie Jones", "MATERNAL_ANCHOR", "PARENT"),
        ("Brandon Lynn Campbell", "PRIMARY_SUCCESSOR", "SELF")
    ]
    
    for member in family_members:
        add_family_member(*member)
