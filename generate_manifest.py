import json
from datetime import datetime, timezone

IDENTITY_KEY = "Campbell; Bandy (Lynn) absolute"
INPUT_LOG = "deep_forensic_audit.log"
MANIFEST_FILE = "reconciliation_manifest.json"

def compile_manifest():
    print(f"[*] REFINING MANIFEST: DEDUPLICATING ENTRIES BY INSTRUMENT ID")
    
    metadata = {
        "operator_key": IDENTITY_KEY,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "environment": "Termux / CivicAdvocate.OS"
    }
    
    unique_records = {}
    anchored_lineage = None

    try:
        with open(INPUT_LOG, "r") as log:
            for line in log:
                line = line.strip()
                if "LINEAGE_ANCHOR" in line:
                    anchored_lineage = line
                elif "PARSED_DATA_ENTRY" in line:
                    raw_json = line.split("DATA: ")[1]
                    data = json.loads(raw_json)
                    # Use instrument number as key to ensure only the latest version persists
                    unique_records[data["instrument_number"]] = line

        final_entries = []
        if anchored_lineage:
            final_entries.append(anchored_lineage)
        
        final_entries.extend(list(unique_records.values()))

        with open(MANIFEST_FILE, "w") as manifest:
            json.dump({"manifest_metadata": metadata, "anchored_entries": final_entries}, manifest, indent=2)
            
        print(f"[✓] MANIFEST REFINED: {len(final_entries)} UNIQUE BLOCKS ANCHORED")
        
    except Exception as e:
        print(f"[!] REFINEMENT ERROR: {str(e)}")

if __name__ == "__main__":
    compile_manifest()
