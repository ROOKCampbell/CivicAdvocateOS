import hashlib
import sqlite3
import datetime

def generate_sha512(data):
    return hashlib.sha512(data.encode('utf-8')).hexdigest()

def purge_municipal_filter(db_path="forensic_ledger.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE system_protocols 
        SET status = 'INACTIVE' 
        WHERE protocol_name = 'Non-Cleburne Guard';
    """)

    cursor.execute("""
        UPDATE extraction_logs 
        SET filter_status = 'UNRESTRICTED' 
        WHERE municipal_signature = 'CLEBURNE';
    """)
    
    timestamp = str(datetime.datetime.now(datetime.timezone.utc))
    action = "NON-CLEBURNE GUARD PURGED. MUNICIPAL DATA UNRESTRICTED."
    hash_payload = f"{timestamp}|{action}"
    action_hash = generate_sha512(hash_payload)

    cursor.execute("""
        INSERT INTO audit_log (timestamp, action, sha512_hash)
        VALUES (?, ?, ?)
    """, (timestamp, action, action_hash))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    purge_municipal_filter()
