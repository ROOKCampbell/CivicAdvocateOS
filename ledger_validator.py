import os
import sqlite3
import hashlib

DATA_DIR = "./ca_ledger_data"
MASTER_INDEX_PATH = os.path.join(DATA_DIR, "master_index.db")

def calculate_file_hash(filepath):
    """Computes SHA-512 hash of a shard file to verify structural integrity."""
    hasher = hashlib.sha512()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

def verify_ledger_integrity():
    """Cross-references physical shard files against the Master Index registry."""
    if not os.path.exists(MASTER_INDEX_PATH):
        print("[CRITICAL] Master Index database is missing!")
        return False

    conn = sqlite3.connect(MASTER_INDEX_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT shard_id, shard_filename, sha512_hash FROM ledger_registry")
        records = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"[ERROR] Failed to read registry: {e}")
        conn.close()
        return False
    
    conn.close()

    if not records:
        print("[NOTICE] No shards registered in the Master Index yet.")
        return True

    print("\n==========================================")
    print("      CIVICADVOCATE.OS LEDGER AUDIT       ")
    print("==========================================")
    
    all_passed = True
    for shard_id, filename, recorded_hash in records:
        filepath = os.path.join(DATA_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"[-] {shard_id}: MISSING FILE ({filename})")
            all_passed = False
            continue
            
        current_hash = calculate_file_hash(filepath)
        
        # If it's a freshly anchored shard without a frozen hash record yet, log its baseline
        if recorded_hash is None:
            print(f"[!] {shard_id}: Open/Unfrozen state. Establishing baseline hash.")
            conn = sqlite3.connect(MASTER_INDEX_PATH)
            conn.execute("UPDATE ledger_registry SET sha512_hash = ? WHERE shard_id = ?", (current_hash, shard_id))
            conn.commit()
            conn.close()
            recorded_hash = current_hash

        if current_hash == recorded_hash:
            print(f"[+] {shard_id}: VALIDATED (Fidelity Match)")
        else:
            print(f"[X] {shard_id}: INVALID! CRYPTOGRAPHIC SIGNATURE MISMATCH!")
            all_passed = False

    print("==========================================")
    if all_passed:
        print("[STATUS] INTEGRITY CHECK: PASSED (All blocks secure)")
    else:
        print("[STATUS] INTEGRITY CHECK: FAILED (Anomalies detected)")
    print("==========================================\n")
    return all_passed

if __name__ == "__main__":
    verify_ledger_integrity()
