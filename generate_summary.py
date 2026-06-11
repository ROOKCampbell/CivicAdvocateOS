import json
from datetime import datetime

MANIFEST_FILE = "reconciliation_manifest.json"

def render_summary():
    print(f"[*] GENERATING GLASS-BOX FORENSIC SUMMARY")
    
    try:
        with open(MANIFEST_FILE, "r") as f:
            data = json.load(f)
            
        metadata = data.get("manifest_metadata", {})
        entries = data.get("anchored_entries", [])
        
        print("\n## [CivicAdvocate.OS] - FORENSIC LEDGER STATUS")
        print(f"> **Architect:** {metadata.get('operator_key')}")
        print(f"> **Environment:** {metadata.get('environment')}")
        print(f"> **Last Sync:** {metadata.get('generated_at')}\n")
        
        print("| Vector Target | Document Type | Instrument # | Status |")
        print("| :--- | :--- | :--- | :--- |")
        
        for entry in entries:
            if "PARSED_DATA_ENTRY" in entry:
                # Extract the JSON portion from the log string
                raw_json = entry.split("DATA: ")[1]
                rec = json.loads(raw_json)
                print(f"| **{rec['target_vector']}** | {rec['document_type']} | `{rec['instrument_number']}` | {rec['verification_status']} |")
                
        print("\n[✓] SUMMARY RENDER COMPLETE")
        
    except Exception as e:
        print(f"[!] RENDER ERROR: {str(e)}")

if __name__ == "__main__":
    render_summary()
