#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# CIVICADVOCATE.OS REAL-TIME FORENSIC WATCHER
# ==============================================================================

DB_NAME="u0_a540"
echo "[*] Initializing Continuous Watcher Daemon..."

# Establish initial row count baseline
LAST_COUNT=$(psql -d "$DB_NAME" -t -A -c "SELECT count(*) FROM public.reaper_audit;")
echo "[+] Baseline verified. Current row count: $LAST_COUNT"

while true; do
    CURRENT_COUNT=$(psql -d "$DB_NAME" -t -A -c "SELECT count(*) FROM public.reaper_audit;")
    
    if [ "$CURRENT_COUNT" -ne "$LAST_COUNT" ]; then
        echo "[!] INGEST DRIFT DETECTED: Row count changed from $LAST_COUNT to $CURRENT_COUNT."
        
        # Trigger full automated re-compilation
        python3 generate_demand.py
        python3 compile_federal_package.py
        python3 verify_package_integrity.py
        ./build_submission_archive.sh
        
        LAST_COUNT=$CURRENT_COUNT
        echo "[+] Pipeline re-sealed at count: $CURRENT_COUNT"
    fi
    sleep 10
done
