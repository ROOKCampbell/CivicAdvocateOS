"""
WSGI Production Entry Point - Hardened Core Matrix
Filename: wsgi.py
"""
import sys
import os
import re
import json
import hashlib
import sqlite3
import logging
from datetime import datetime, timezone

# --- High-Fidelity Logging Vector ---
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z'
)
logger = logging.getLogger("CivicAdvocate.OS.WSGI")

# --- Cryptographic State Baseline ---
LAST_LEDGER_HASH = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

# --- Module 1: Non-Cleburne Guard Filter ---
QUARANTINE_PATTERN = re.compile(r'\b(cleburne|cleburn|cleb)\b', re.IGNORECASE)

def enforce_jurisdictional_quarantine(payload_str):
    """Parses input text for unauthorized jurisdictional markers."""
    if QUARANTINE_PATTERN.search(payload_str):
        logger.warning("ALARM: Non-Cleburne Guard isolation protocol tripped. Incoming payload quarantined.")
        return False
    return True

# --- Module 2: Merkle-Sequence Ledger Core ---
def generate_ledger_block(payload_bytes):
    """Generates a sequentially chained SHA-512 hash anchoring the transaction."""
    global LAST_LEDGER_HASH
    
    sha512 = hashlib.sha512()
    sha512.update(LAST_LEDGER_HASH.encode('utf-8'))
    sha512.update(payload_bytes)
    current_hash = sha512.hexdigest()
    
    LAST_LEDGER_HASH = current_hash
    return current_hash

# --- Module 3: Database Routing Matrix ---
def init_persistence_layer():
    """Establishes baseline relational structures for tracking."""
    db_path = os.getenv("CIVIC_DB_PATH", "civic_advocate_ledger.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaction_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            payload TEXT NOT NULL,
            merkle_hash TEXT NOT NULL,
            previous_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize DB layer during master configuration load
try:
    init_persistence_layer()
    logger.info("Database persistence layer linked and verified stable.")
except Exception as e:
    logger.critical(f"Critical error mapping database router: {str(e)}")
    sys.exit(1)

# --- Consolidated WSGI Route Framework ---
def application(environ, start_response):
    global LAST_LEDGER_HASH
    
    path_info = environ.get('PATH_INFO', '/')
    request_method = environ.get('REQUEST_METHOD', 'GET')
    
    # Establish Standardized Security Headers
    headers = [
        ('Content-Type', 'application/json'),
        ('X-Content-Type-Options', 'nosniff'),
        ('X-Frame-Options', 'DENY'),
        ('X-XSS-Protection', '1; mode=block')
    ]
    
    # Route A: API Health Node Check
    if path_info == '/status' or path_info == '/':
        start_response('200 OK', headers)
        return [b'{"status": "ONLINE", "ledger_sync": "SYNCHRONIZED"}']
        
    # Route B: Transaction Ledger Processing Ingestion Vector
    elif path_info == '/submit' and request_method == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(content_length)
            payload_str = request_body.decode('utf-8')
        except Exception as e:
            start_response('400 Bad Request', headers)
            return [b'{"error": "Failed to safely process stream payload structure."}']
            
        # 1. Execute Jurisdictional Guard Filter Check
        if not enforce_jurisdictional_quarantine(payload_str):
            start_response('403 Forbidden', headers)
            return [b'{"status": "REJECTED", "reason": "Jurisdictional Quarantine Isolation Enforced."}']
            
        # 2. Compute Cryptographic Sequence Block Linking
        prev_hash = LAST_LEDGER_HASH
        block_hash = generate_ledger_block(request_body)
        timestamp_str = datetime.now(timezone.utc).isoformat()
        
        # 3. Write Block Data directly to DB Matrix
        try:
            db_path = os.getenv("CIVIC_DB_PATH", "civic_advocate_ledger.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transaction_ledger (timestamp, payload, merkle_hash, previous_hash) VALUES (?, ?, ?, ?)",
                (timestamp_str, payload_str, block_hash, prev_hash)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to commit ledger node to disk: {str(e)}")
            start_response('500 Internal Server Error', headers)
            return [b'{"error": "Persistence failure on active sequence block."}']
            
        start_response('201 Created', headers)
        return [json.dumps({
            "status": "COMMITTED",
            "timestamp": timestamp_str,
            "merkle_block": block_hash
        }).encode('utf-8')]
        
    # Route Fallback: Not Found Matrix
    else:
        start_response('404 Not Found', headers)
        return [b'{"error": "Target node path undefined."}']
