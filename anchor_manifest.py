import hashlib
import os
from datetime import datetime, timezone

def generate_sha512(file_path):
    """Generates a SHA-512 hash for the specified file."""
    BUF_SIZE = 65536  # Read in 64kb chunks
    sha512 = hashlib.sha512()
    
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha512.update(data)
        return sha512.hexdigest()
    except FileNotFoundError:
        return None

def anchor_to_ledger(target_file, ledger_file):
    """Calculates hash and appends a timestamped entry to the ledger."""
    file_hash = generate_sha512(target_file)
    
    if file_hash is None:
        print(f"Error: Target file '{target_file}' not found.")
        return

    # UTC timestamp for absolute forensic tracking
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # Format: Timestamp | Filename | SHA-512 Hash
    ledger_entry = f"{timestamp} | {target_file} | {file_hash}\n"

    with open(ledger_file, 'a') as f:
        f.write(ledger_entry)
    
    print("-" * 20)
    print(f"ASSET ANCHORED SUCCESSFULLY")
    print(f"File: {target_file}")
    print(f"Hash: {file_hash}")
    print(f"Ledger: {ledger_file}")
    print("-" * 20)

if __name__ == "__main__":
    anchor_to_ledger('infrastructure.yaml', 'forensic_ledger.sha512')
