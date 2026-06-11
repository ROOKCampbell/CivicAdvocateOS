import os, sys, hashlib, json, psycopg2

DB_NAME = "u0_a540"
DB_USER = "u0_a540"
STRIKE_DIR = os.path.expanduser("~/forensic_strikes")

def calculate_sha512(data_string):
    return hashlib.sha512(data_string.encode('utf-8')).hexdigest()

def process_audit_cycle(intake_id, payload_data):
    raw_payload_str = json.dumps(payload_data, sort_keys=True)
    checksum = calculate_sha512(raw_payload_str)
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO public.reaper_audit (intake_id, checksum) VALUES (%s, %s) RETURNING audit_id, reset_at;", (intake_id, checksum))
        audit_id, reset_at = cursor.fetchone()
        conn.commit()
        print(f"[+] DB Commit Successful. Audit ID: {audit_id}")
    except Exception as e:
        print(f"[!] Database Validation Failure: {e}"); sys.exit(1)
    finally:
        if 'conn' in locals(): cursor.close(); conn.close()
    
    os.makedirs(STRIKE_DIR, exist_ok=True)
    with open(f"{STRIKE_DIR}/strike_{intake_id}_{audit_id}.json", 'w') as sf:
        json.dump({"audit_id": audit_id, "intake_id": intake_id, "timestamp": str(reset_at), "sha512_checksum": checksum}, sf, indent=4)
    print(f"[+] Forensic Strike-File Persisted."); os.system("python3 append_to_ledger.py")

if __name__ == "__main__":
    process_audit_cycle(intake_id=101, payload_data={"system_node": "CivicAdvocate.OS_Core", "integrity": "SHA-512"})
