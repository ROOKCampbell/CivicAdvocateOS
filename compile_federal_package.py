import os
import zipfile
import hashlib
from datetime import datetime, timezone

def verify_asset_before_bundling(filename, ledger_file='forensic_ledger.sha512'):
    if not os.path.exists(filename):
        return False
    
    # Extract anchored hash from ledger
    anchored_hash = None
    with open(ledger_file, 'r') as f:
        for line in f:
            if filename in line:
                anchored_hash = line.strip().split(' | ')[2]
                break
                
    if not anchored_hash:
        return False

    # Calculate current hash
    sha512 = hashlib.sha512()
    with open(filename, 'rb') as f:
        while chunk := f.read(65536):
            sha512.update(chunk)
            
    return sha512.hexdigest() == anchored_hash

def build_package():
    print("--- Initializing Federal Evidentiary Package Compilation ---")
    
    required_assets = [
        'infrastructure.yaml',
        'cleburne.guard',
        'rrc_cleburne_production.log',
        'forensic_ledger.sha512'
    ]
    
    # Verify all components are uncorrupted before sealing
    for asset in required_assets:
        if asset == 'forensic_ledger.sha512':
            if not os.path.exists(asset):
                print(f"[ERROR] Missing critical anchor ledger: {asset}")
                return
            continue
            
        if not verify_asset_before_bundling(asset):
            print(f"[CRITICAL] Asset integrity check failed for: {asset}. Aborting package compilation.")
            return
        print(f"[READY] Integrity Verified: {asset}")

    # Generate Package Name with Temporal Anchor
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    package_name = f"enforcement_packages/CLEBURNE_COMPLIANCE_PACKAGE_{timestamp}.zip"
    
    os.makedirs('enforcement_packages', exist_ok=True)
    
    # Write to Zip Compressed Format
    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for asset in required_assets:
            zipf.write(asset)
            
    print("-" * 40)
    print(f"[SUCCESS] EVIDENTIARY ARCHIVE SEALED")
    print(f"Archive Path: {package_name}")
    print(f"Status: SECURE / READY FOR DISPATCH")
    print("-" * 40)

if __name__ == "__main__":
    build_package()
