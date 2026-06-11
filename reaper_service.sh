#!/data/data/com.termux/files/usr/bin/bash

# Configuration
INTERVAL=60 # Run every minute
CYCLE=0

echo "[*] CivicAdvocate.OS Master Service Online."

while true; do
    CYCLE=$((CYCLE + 1))
    
    # 1. Intake: Pull Texas RRC Data
    python3 rrc_scraper.py > /dev/null 2>&1
    
    # 2. Verify: Integrity Check
    python3 verify_integrity.py
        python3 generate_demand.py
        python3 compile_federal_package.py
    if [ $? -ne 0 ]; then
        echo "[!] Integrity compromised. Alert triggered."
    fi
    
    # 3. Sync: Push Ledger to Git every 5 cycles
    if [ $((CYCLE % 5)) -eq 0 ]; then
        ./sync_git_ledger.sh
    fi
    
    sleep $INTERVAL
done
