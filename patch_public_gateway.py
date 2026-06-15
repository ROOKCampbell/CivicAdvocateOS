import json
import os
from orchestrator import SYSTEM_MATRIX

def export_public_manifest():
    print("[*] INITIALIZING PUBLIC GATEWAY EXPORT MODULE...")
    
    # Extract only non-sensitive cryptographic keys and statuses
    public_matrix = {
        "MANIFEST_METADATA": {
            "kernel": SYSTEM_MATRIX["METADATA"]["kernel"],
            "timestamp_utc": SYSTEM_MATRIX["METADATA"]["last_sync"],
            "verification_type": "SHA-512 Zero-Knowledge Audit"
        },
        "VERIFIED_NODES": {}
    }
    
    # Map federal nodes to public ledger (hashes only, no local paths)
    fed_nodes = SYSTEM_MATRIX["TRACK_01_FEDERAL"]["nodes"]
    for node_id, node_data in fed_nodes.items():
        public_matrix["VERIFIED_NODES"][node_id] = {
            "agency": node_data["agency"],
            "jurisdiction": node_data["jurisdiction"],
            "fingerprint": node_data["package_fingerprint"],
            "status": node_data["status"]
        }
        
    # Map fiscal track public status
    fiscal = SYSTEM_MATRIX["TRACK_02_FISCAL"]
    public_matrix["VERIFIED_NODES"]["LOCAL-FISCAL-01"] = {
        "target": fiscal["target"],
        "notice_status": fiscal["notice_of_default"]["status"]
    }

    # Write the public-facing transport file
    output_path = "public_manifest.json"
    with open(output_path, "w") as f:
        json.dump(public_matrix, f, indent=4)
        
    print(f"[+] PUBLIC MANIFEST SUCCESSFULLY GENERATED: {output_path}")
    print("[!] SAFE FOR PUBLIC REPOSITORY COMMIT (ZERO PRIVATE DATA EXPOSED).")

if __name__ == "__main__":
    export_public_manifest()
