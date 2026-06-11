import hashlib
import os

def generate_sha512(file_path):
    BUF_SIZE = 65536
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

def verify_ledger(ledger_file):
    print(f"--- Integrity Report for {ledger_file} ---")
    if not os.path.exists(ledger_file):
        print("Error: Ledger file not found.")
        return

    # Simulate an internal counter or audit ID tracking
    audit_id = 101 
    mismatch_found = False

    with open(ledger_file, 'r') as f:
        for line in f:
            parts = line.strip().split(' | ')
            if len(parts) != 3:
                continue
            
            timestamp, filename, anchored_hash = parts
            current_hash = generate_sha512(filename)
            
            if current_hash is None:
                print(f"[MISSING] {filename}")
                mismatch_found = True
            elif current_hash == anchored_hash:
                print(f"[VERIFIED] {filename} (Matches anchor from {timestamp})")
            else:
                print(f"[WARNING] {filename} HAS BEEN MODIFIED since anchoring!")
                mismatch_found = True
                # Cleaned f-string using internal single quotes to prevent syntax breakage
                print(f"\n\a[!!] CRITICAL INTEGRITY MISMATCH: Audit ID {audit_id} hash drift detected!")
                os.system(f"termux-notification -t 'CRITICAL: Ledger Drift' -c 'Audit ID {audit_id} has been compromised.'")

    if not mismatch_found:
        print("\nAll systemic records match their anchored cryptographic hashes perfectly.")

if __name__ == "__main__":
    verify_ledger('forensic_ledger.sha512')
