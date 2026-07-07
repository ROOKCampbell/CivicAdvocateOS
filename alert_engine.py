#!/usr/bin/env python3
# CivicAdvocate.OS | Real-Time Terminal Alert Matrix
# Workflow: Overview -> Code -> Implementation

import os
import sys
import json
import time

LEDGER_PATH = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/genesis_ledger.dat"

def monitor_ledger_alerts():
    print("=== [CivicAdvocate.OS Real-Time Alert Engine Active] ===")
    print("[*] Scan baseline locked. Monitoring network storage file changes...")
    
    # Establish initial baseline size boundary
    if os.path.exists(LEDGER_PATH):
        last_size = os.path.getsize(LEDGER_PATH)
    else:
        last_size = 0
        
    while True:
        try:
            time.sleep(1)
            if not os.path.exists(LEDGER_PATH):
                continue
                
            current_size = os.path.getsize(LEDGER_PATH)
            if current_size > last_size:
                # File expansion caught. Parse final committed block line
                with open(LEDGER_PATH, 'r') as f:
                    lines = [line.strip() for line in f if line.strip()]
                    if lines:
                        final_entry = json.loads(lines[-1])
                        payload = final_entry.get("payload", {})
                        
                        # Trigger system audio terminal bell + flashing ANSI layout warning blocks
                        sys.stdout.write("\a") # ASCII Terminal Bell Sound code trigger
                        print("\n\033[5;31;47m [ALERT] CRITICAL STATE ENVELOPE COMMITTED TO MAINNET LEDGER \033[0m")
                        print(f" [+] VECTOR TRACE ID : {payload.get('docket', 'UNKNOWN')}")
                        print(f" [+] COMPLIANCE EVENT: {payload.get('action', 'UNKNOWN')}")
                        print(f" [+] DATA RECORD     : {json.dumps(payload)[:100]}...")
                        print("-" * 70)
                        
                last_size = current_size
        except KeyboardInterrupt:
            print("\n[-] Shutting down Alert Listener securely.")
            break
        except Exception as e:
            time.sleep(2)

if __name__ == "__main__":
    monitor_ledger_alerts()
