#!/usr/bin/env python3
"""
Civic Advocate Service (CAS) - Duty-of-Notice Auditor
Description: Enforces the fiduciary mandate that public officials must notify 
             citizens of verified record updates. Filtered for system integrity.
"""

import sqlite3
import json
from datetime import datetime

class DutyAuditor:
    def __init__(self, db_path="civic_state.db"):
        self.db_path = db_path

    def audit_notification_duty(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Updated: Filter out system-generated records to prevent false positives
        cursor.execute("""
            SELECT entry_id, record_owner, record_type, payload 
            FROM cas_ledger 
            WHERE notification_status != 'VERIFIED'
            AND vector_type NOT IN ('CORE_SYSTEM_INIT', 'PUBLIC_OFFICIAL_ROSTER')
        """)
        pending_notices = cursor.fetchall()
        
        if not pending_notices:
            print("[DUTY_AUDIT] All administrative records verified. Notification protocols satisfied.")
            conn.close()
            return

        print(f"[DUTY_AUDIT] ALERT: {len(pending_notices)} records found without verified public notification.")
        
        for entry in pending_notices:
            tx_id, owner, r_type, payload = entry
            self.flag_violation(tx_id, owner, r_type)

        conn.close()

    def flag_violation(self, tx_id, owner, r_type):
        violation_alert = {
            "timestamp": datetime.now().isoformat(),
            "violation_type": "FAILURE_OF_DUTY_NOTICE",
            "record_id": tx_id,
            "impacted_party": owner,
            "status": "ACTION_REQUIRED"
        }
        
        with open("public_accountability_alerts.log", "a") as f:
            f.write(json.dumps(violation_alert) + "\n")
            
        print(f"[DUTY_AUDIT] Violation flagged for Record {tx_id}. Alert written to public log.")

if __name__ == "__main__":
    auditor = DutyAuditor()
    auditor.audit_notification_duty()
