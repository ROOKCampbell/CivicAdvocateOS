import os, sqlite3, hashlib
from datetime import datetime

DATA_DIR = "./ca_ledger_data"
MASTER_INDEX_PATH = os.path.join(DATA_DIR, "master_index.db")

os.makedirs(DATA_DIR, exist_ok=True)
conn = sqlite3.connect(MASTER_INDEX_PATH)
conn.execute("CREATE TABLE IF NOT EXISTS ledger_registry (shard_id TEXT PRIMARY KEY, shard_filename TEXT, initialized_at TEXT, sha512_hash TEXT, is_immutable INTEGER DEFAULT 0)")
conn.close()

print("\n==========================================")
print("[STATUS] CivicAdvocate.OS Engine Online")
print(f"[STATUS] Storage Directory: {os.path.abspath(DATA_DIR)}")
print("[STATUS] Master Ledger Index Initialized Successfully.")
print("==========================================\n")
