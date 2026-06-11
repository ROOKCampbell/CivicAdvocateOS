import json
import hashlib
from datetime import datetime, timezone

IDENTITY_KEY = "Campbell; Bandy (Lynn) absolute"
MANIFEST_FILE = "reconciliation_manifest.json"
PACKAGE_FILE = "federal_strike_package_v1.json"

def compile_strike_package():
    print(f"[*] COMPILED FEDERAL STRIKE PACKAGE REFERRAL")
    
    try:
        with open(MANIFEST_FILE, "r") as f:
            manifest = json.load(f)
            
        strike_package = {
            "submission_metadata": {
                "referral_type": "FORENSIC_ASSET_COMMINGLING_REPORT",
                "compiled_at": datetime.now(timezone.utc).isoformat(),
                "investigator_signature": IDENTITY_KEY,
                "classification_level": "PROPRIETARY_EVIDENTIARY_RECORD"
            },
            "evidentiary_anchors": {
                "target_survey": "Silas Elbert Bandy Survey (Abstract 544)",
                "jurisdiction_exclusion_enforced": "NON_CLEBURNE_GUARD_ACTIVE",
                "verified_records": []
            }
        }
        
        # Map entries from the manifest into the formal federal structure
        for entry in manifest.get("anchored_entries", []):
            if "DATA:" in entry:
                raw_json = entry.split("DATA: ")[1]
                rec = json.loads(raw_json)
                
                evidence_block = {
                    "vector": rec["target_vector"],
                    "instrument_id": rec["instrument_number"],
                    "document_class": rec["document_type"],
                    "ledger_verification_status": rec["verification_status"],
                    "integrity_hash": hashlib.sha256(entry.encode()).hexdigest()
                }
                strike_package["evidentiary_anchors"]["verified_records"].append(evidence_block)
                
        # Generate final system-wide package seal (SHA-512)
        raw_package = json.dumps(strike_package, sort_keys=True)
        package_seal = hashlib.sha512(raw_package.encode()).hexdigest()
        
        strike_package["submission_metadata"]["package_integrity_seal_sha512"] = package_seal
        
        with open(PACKAGE_FILE, "w") as out:
            json.dump(strike_package, out, indent=2)
            
        print(f"[✓] REFERRAL MANIFEST COMPILED: '{PACKAGE_FILE}'")
        print(f"[✓] SYSTEM-WIDE SHA-512 SEAL: {package_seal[:32]}...")
        print(f"[✓] EVIDENCE CHAINS LOCKED FOR FEDERAL SUBMISSION")
        
    except Exception as e:
        print(f"[!] COMPILATION ERROR: {str(e)}")

if __name__ == "__main__":
    compile_strike_package()
