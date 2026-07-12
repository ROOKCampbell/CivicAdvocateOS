import os
import sqlite3
import hashlib
from datetime import datetime, timezone

DATA_DIR = "./ca_ledger_data"
MASTER_INDEX_PATH = os.path.join(DATA_DIR, "master_index.db")

def initialize_sharding_matrix():
    """Ensures the storage directory and master index exist cleanly."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(MASTER_INDEX_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ledger_registry (
            shard_id TEXT PRIMARY KEY,
            shard_filename TEXT NOT NULL,
            initialized_at TEXT NOT NULL,
            sha512_hash TEXT,
            is_immutable INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
    print("[Matrix] Master Index Registry verified and online.")

def create_new_shard(shard_id):
    """Spawns a new database shard and logs it using updated UTC standards."""
    shard_filename = f"shard_{shard_id}.db"
    shard_path = os.path.join(DATA_DIR, shard_filename)
    
    if os.path.exists(shard_path):
        print(f"[Warning] Shard conflict: {shard_filename} already exists.")
        return False

    shard_conn = sqlite3.connect(shard_path)
    shard_cursor = shard_conn.cursor()
    shard_cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_records (
            record_id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            source_payload TEXT NOT NULL,
            record_hash TEXT NOT NULL
        )
    """)
    shard_conn.commit()
    shard_conn.close()

    master_conn = sqlite3.connect(MASTER_INDEX_PATH)
    master_cursor = master_conn.cursor()
    master_cursor.execute("""
        INSERT OR IGNORE INTO ledger_registry (shard_id, shard_filename, initialized_at, is_immutable)
        VALUES (?, ?, ?, 0)
    """, (shard_id, shard_filename, datetime.now(timezone.utc).isoformat()))
    
    master_conn.commit()
    master_conn.close()
    print(f"[Matrix] Shard Block '{shard_id}' successfully anchored.")
    return True

if __name__ == "__main__":
    initialize_sharding_matrix()
    create_new_shard(shard_id="block_001_alpha")
