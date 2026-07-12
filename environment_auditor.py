import os
import sqlite3
import hashlib
from datetime import datetime, timezone

# Target the root of your project
ROOT_DIR = "."
# Exclude the ledger data so we don't audit the audit databases
EXCLUDE_DIRS = ["./ca_ledger_data", "./.git"]
INVENTORY_DB = "./system_inventory.db"

def calculate_hash(filepath):
    """Calculates SHA-512 for any given file."""
    hasher = hashlib.sha512()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, FileNotFoundError):
        return "UNREADABLE_OR_MISSING"

def build_inventory():
    """Crawls the environment and establishes a baseline inventory."""
    conn = sqlite3.connect(INVENTORY_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_inventory (
            file_path TEXT PRIMARY KEY,
            filename TEXT,
            last_seen TEXT,
            sha512_hash TEXT,
            status TEXT
        )
    """)
    conn.commit()

    print("\n==========================================")
    print("      ENVIRONMENT AUDIT INITIATED         ")
    print("==========================================")

    total_files = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in EXCLUDE_DIRS and not d.startswith('.')]
        
        for file in files:
            # Skip the inventory database itself and the script running it
            if file in ["system_inventory.db", "environment_auditor.py"]:
                continue
                
            filepath = os.path.join(root, file)
            file_hash = calculate_hash(filepath)
            timestamp = datetime.now(timezone.utc).isoformat()
            
            # Check if it already exists in the inventory
            cursor.execute("SELECT sha512_hash FROM file_inventory WHERE file_path = ?", (filepath,))
            existing_record = cursor.fetchone()
            
            if not existing_record:
                print(f"[+] NEW FILE LOGGED: {filepath}")
                cursor.execute("""
                    INSERT INTO file_inventory (file_path, filename, last_seen, sha512_hash, status)
                    VALUES (?, ?, ?, ?, 'VERIFIED')
                """, (filepath, file, timestamp, file_hash))
            elif existing_record[0] != file_hash:
                print(f"[!] MODIFIED DETECTED: {filepath}")
                cursor.execute("""
                    UPDATE file_inventory SET sha512_hash = ?, last_seen = ?, status = 'MODIFIED'
                    WHERE file_path = ?
                """, (file_hash, timestamp, filepath))
            
            total_files += 1

    conn.commit()
    conn.close()

    print("==========================================")
    print(f"[STATUS] AUDIT COMPLETE. {total_files} files secured in inventory.")
    print("==========================================\n")

if __name__ == "__main__":
    build_inventory()
