#!/usr/bin/env python3
import sqlite3
import os

db_path = "civic_advocate_ledger.db"

if not os.path.exists(db_path):
    print(f"[-] Target database node not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT id, timestamp, payload, merkle_hash, previous_hash FROM transaction_ledger;")
    records = cursor.fetchall()
    
    if not records:
        print("[!] Database initialized successfully. State: Idle (0 records committed).")
    else:
        print(f"[✓] Active Ledger Matrix Sync: {len(records)} entries found.\n" + "="*80)
        for row in records:
            print(f"Block ID:      {row[0]}")
            print(f"Timestamp:     {row[1]}")
            print(f"Payload Data:  {row[2].strip()}")
            print(f"Current Hash:  {row[3]}")
            print(f"Previous Hash: {row[4]}")
            print("-" * 80)
            
except sqlite3.OperationalError as e:
    print(f"[-] Structural Error reading transaction table: {str(e)}")
finally:
    conn.close()
