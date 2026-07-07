#!/usr/bin/env python3
"""
Civic Advocate Service (CAS) - Record Ingestor
Description: Standardizes and ingests raw records into the cas_ledger 
             for audit monitoring.
"""

import sqlite3
import json
from datetime import datetime

def ingest_record(owner, r_type, raw_data):
    conn = sqlite3.connect("civic_state.db")
    cursor = conn.cursor()
    
    # Ingest with status 'PENDING' so the auditor picks it up immediately
    cursor.execute("""
        INSERT INTO cas_ledger 
        (timestamp, vector_type, payload, record_owner, record_type, notification_status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().isoformat(), "PUBLIC_RECORD", json.dumps(raw_data), owner, r_type, "PENDING"))
    
    conn.commit()
    conn.close()
    print(f"[INGESTOR] Record for {owner} successfully queued for audit.")

if __name__ == "__main__":
    # Example Usage: Ingesting a specific record
    # Replace these values with the data you retrieve from Cleburne/Johnson County sources
    sample_owner = "JOHN_DOE"
    sample_type = "PROPERTY_DEED"
    sample_data = {"deed_id": "12345", "location": "Cleburne, TX", "verified": False}
    
    ingest_record(sample_owner, sample_type, sample_data)
