import json
import hashlib
from datetime import datetime, timezone

IDENTITY_KEY = "Campbell; Bandy (Lynn) absolute"
INPUT_LOG = "deep_forensic_audit.log"
MANIFEST_FILE = "reconciliation_manifest.json"

def compile_manifest():
    print(f"[*] COMPILING SYSTEM RECONCILIATION MANIFEST")
    
    records = {
        "manifest_metadata": {
            "operator_key": IDENTITY_KEY,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "environment": "Termux / CivicAdvocate.OS"
        },
        "anchored_entries": []
    }
    
    try:
        with open(INPUT_LOG, "r") as log:
            for line in log:
                if "PARSED_DATA_ENTRY" in line or "LINEAGE_ANCHOR" in line:
                    # Strip out newline characters and split data blocks
                    cleaned_line = line.strip()
                    records["anchored_entries"].append(cleaned_line)
        
        # Serialize report structure
        with open(MANIFEST_FILE, "w") as manifest:
            json.dump(records, manifest, indent=2)
            
        print(f"[✓] MANIFEST GENERATED: '{MANIFEST_FILE}'")
        print(f"[✓] TOTAL UNIQUE BLOCKS COMPILED: {len(records['anchored_entries'])}")
        
    except Exception as e:
        print(f"[!] RECONCILIATION ERROR: {str(e)}")

if __name__ == "__main__":
    compile_manifest()
