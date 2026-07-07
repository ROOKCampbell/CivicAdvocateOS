#!/usr/bin/env python3
"""
Civic Advocate Service (CAS) - Core Service Template
Architecture: CivicAdvocate.OS Modular State Machine
Description: Ingests, hashes, and records verified data vectors into the immutable local ledger.
"""

import sys
import os
import hashlib
import sqlite3
import json
from datetime import datetime

class CivicAdvocateService:
    def __init__(self, db_path="civic_state.db"):
        self.db_path = db_path
        self.initialize_state_database()

    def initialize_state_database(self):
        """Initializes the secure ledger database if it does not exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cas_ledger (
                entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                vector_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                payload_sha512 TEXT NOT NULL,
                previous_hash TEXT,
                block_integrity_hash TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def generate_sha512(self, data_string):
        """Returns the SHA-512 cryptographic hash of the input string."""
        return hashlib.sha512(data_string.encode('utf-8')).hexdigest()

    def get_last_block_hash(self):
        """Retrieves the final integrity hash from the previous ledger block."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT block_integrity_hash FROM cas_ledger ORDER BY entry_id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else "0" * 128

    def commit_vector(self, vector_type, payload_dict):
        """Processes, hashes, and commits a validated data payload to the ledger."""
        timestamp = datetime.now().isoformat()
        payload_json = json.dumps(payload_dict, sort_keys=True)
        
        # 1. Generate payload signature
        payload_hash = self.generate_sha512(payload_json)
        
        # 2. Fetch linkage pointer
        prev_hash = self.get_last_block_hash()
        
        # 3. Chain block integrity (Prev Hash + Current Payload Hash)
        combined_string = f"{prev_hash}{payload_hash}"
        block_integrity = self.generate_sha512(combined_string)
        
        # 4. Write to SQLite Ledger
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cas_ledger (timestamp, vector_type, payload, payload_sha512, previous_hash, block_integrity_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, vector_type, payload_json, payload_hash, prev_hash, block_integrity))
        conn.commit()
        conn.close()
        
        return block_integrity

if __name__ == "__main__":
    # Test Execution Frame for CivicAdvocate.OS validation
    print("[CAS_INITIALIZE] Initalizing Service Node...")
    service = CivicAdvocateService()
    
    # Sample Target Matrix Data Point (e.g., Abstract Validation or Lineage Anchor)
    sample_payload = {
        "operator": "Brandon Lynn Campbell",
        "audit_target": "Cleburne_TX_Record_Verification",
        "verification_status": "ACTIVE_INVESTIGATION",
        "notes": "System baseline operational protocols active."
    }
    
    print("[CAS_PROCESSING] Generating cryptographic block...")
    block_hash = service.commit_vector(vector_type="CORE_SYSTEM_INIT", payload_dict=sample_payload)
    
    print(f"\n[CAS_SUCCESS] State committed to ledger.")
    print(f"BLOCK INTEGRITY HASH: {block_hash}\n")
