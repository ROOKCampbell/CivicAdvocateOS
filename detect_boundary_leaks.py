#!/usr/bin/env python3
import psycopg2
import re

def analyze_boundary_leaks():
    print("===============================================================================")
    print("                  CIVICADVOCATE.OS BOUNDARY INTEGRITY AUDIT                    ")
    print("===============================================================================")
    print("[*] Interrogating database 'u0_a540' for cross-jurisdictional leaks...")

    try:
        conn = psycopg2.connect(dbname="u0_a540")
        cur = conn.cursor()

        # 1. Extract survey anchor identifiers from the primary audit ledger
        cur.execute("SELECT DISTINCT intake_id FROM public.reaper_audit;")
        survey_ids = [str(row[0]) for row in cur.fetchall()]
        print(f"[+] Active Survey Trackers isolated: {survey_ids}")

        # 2. Extract municipal records staged for review
        cur.execute("SELECT id, raw_data, extracted_at FROM public.municipal_transparency;")
        municipal_records = cur.fetchall()
        print(f"[+] Staged Municipal Records evaluated: {len(municipal_records)}")

        leaks_found = 0
        print("-------------------------------------------------------------------------------")
        print(" Analyzing data payloads for token overlap...")

        for m_id, raw_data, extracted_at in municipal_records:
            # Check for direct leakage of survey identifiers into the municipal dataset
            for survey_id in survey_ids:
                # Match survey ID as a distinct token inside the municipal text string
                pattern = r'\b' + re.escape(survey_id) + r'\b'
                if re.search(pattern, raw_data):
                    leaks_found += 1
                    print(f"\n[!] ALERT: BOUNDARY LEAK DETECTED")
                    print(f"    └─ Municipal Record ID: {m_id}")
                    print(f"    └─ Ingest Timestamp   : {extracted_at}")
                    print(f"    └─ Contaminated Token : Abstract ID {survey_id}")
                    print(f"    └─ Raw Payload Text   : \"{raw_data.strip()}\"")
                    
                    # Update investigation status in the database to flag this record
                    cur.execute("""
                        UPDATE public.municipal_transparency 
                        SET investigation_status = 'CONTAGION_CONFIRMED' 
                        WHERE id = %s;
                    """, (m_id,))

        conn.commit()
        cur.close()
        conn.close()

        print("-------------------------------------------------------------------------------")
        if leaks_found == 0:
            print("[+] INTEGRITY VERIFIED: Zero boundary leaks detected between datasets.")
        else:
            print(f"[!] RECOVERY REQUIRED: Found {leaks_found} instances of cross-contamination.")
            print("[*] Contaminated records locked with status 'CONTAGION_CONFIRMED'.")
        print("===============================================================================")

    except psycopg2.Error as e:
        print(f"[!] Database processing error: {e}")

if __name__ == "__main__":
    analyze_boundary_leaks()
