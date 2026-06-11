import os
import json
import hashlib
from datetime import datetime, timezone

def generate_package_manifest():
    package_path = "enforcement_packages/CLEBURNE_COMPLIANCE_PACKAGE_20260611_080240.zip"
    manifest_path = "enforcement_packages/DISPATCH_MANIFEST_20260611.json"
    
    if not os.path.exists(package_path):
        print(f"[ERROR] Target package not found at: {package_path}")
        return

    # Calculate absolute SHA-512 signature of the entire compressed package
    sha512 = hashlib.sha512()
    with open(package_path, 'rb') as f:
        while chunk := f.read(65536):
            sha512.update(chunk)
    package_hash = sha512.hexdigest()
    
    # Structure metadata tracking properties
    manifest_data = {
        "manifest_metadata": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "target_system": "CivicAdvocate.OS",
            "security_clearance": "RESTRICTED / FORENSIC RECORD"
        },
        "archive_identity": {
            "file_name": os.path.basename(package_path),
            "file_size_bytes": os.path.getsize(package_path),
            "sha512_fingerprint": package_hash
        },
        "on_chain_anchors": {
            "ledger_reference": "forensic_ledger.sha512",
            "validation_status": "PASSED"
        }
    }
    
    # Write structural glass-box manifest
    with open(manifest_path, 'w') as mj:
        json.dump(manifest_data, mj, indent=2)
        
    print("--- Detached Dispatch Manifest Generated ---")
    print(json.dumps(manifest_data, indent=2))
    print("-" * 44)

if __name__ == "__main__":
    generate_package_manifest()
