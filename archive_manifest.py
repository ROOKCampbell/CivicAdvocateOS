import os
import gzip
import json
import hashlib
from datetime import datetime, timezone

IDENTITY_KEY = "Campbell; Bandy (Lynn) absolute"
MANIFEST_FILE = "reconciliation_manifest.json"
BACKUP_DIR = "archive_store"

def secure_archive():
    print(f"[*] INITIALIZING SECURE ARCHIVAL ROUTINE")
    
    if not os.path.exists(MANIFEST_FILE):
        print(f"[!] ERROR: TARGET MANIFEST NOT FOUND")
        return

    # 1. Create dedicated archive directory if it doesn't exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"[*] CREATED LOCAL ARCHIVE STORAGE SYSTEM: {BACKUP_DIR}/")

    # 2. Establish uniform naming convention
    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    archive_name = f"manifest_snapshot_{timestamp_str}.json.gz"
    archive_path = os.path.join(BACKUP_DIR, archive_name)
    checksum_path = archive_path + ".sha512"

    try:
        # 3. Read manifest and write directly to compressed gzip format
        with open(MANIFEST_FILE, "rb") as src:
            data_bytes = src.read()
            
        with gzip.open(archive_path, "wb") as dest:
            dest.write(data_bytes)
            
        # 4. Calculate verification checksum of the compressed payload
        with open(archive_path, "rb") as f:
            archive_bytes = f.read()
            calc_hash = hashlib.sha512(archive_bytes).hexdigest()
            
        with open(checksum_path, "w") as f_hash:
            f_hash.write(f"{calc_hash}  {archive_name}\n")
            
        print(f"[✓] SNAPSHOT STORED: {archive_path}")
        print(f"[✓] DETACHED INTEGRITY CHECK CREATED: {archive_name}.sha512")
        print(f"[✓] SNAPSHOT SHA-512: {calc_hash[:16]}...")
        
    except Exception as e:
        print(f"[!] ARCHIVAL FAILURE: {str(e)}")

if __name__ == "__main__":
    secure_archive()
