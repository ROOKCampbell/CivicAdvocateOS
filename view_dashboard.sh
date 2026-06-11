#!/data/data/com.termux/files/usr/bin/bash
clear
echo "======================================================================"
echo "               CIVICADVOCATE.OS DUAL-VERIFICATION DASHBOARD           "
echo "======================================================================"
echo " System Time: $(date)"
echo " Database Instance: u0_a540 | Host: Termux Local Socket"
echo "----------------------------------------------------------------------"

# 1. Pull Table Volume Row-Counts
TOTAL_DB_RECORDS=$(psql -d u0_a540 -t -A -c "SELECT count(*) FROM public.reaper_audit;")
LAST_TIMESTAMP=$(psql -d u0_a540 -t -A -c "SELECT max(reset_at) FROM public.reaper_audit;")

# 2. Check File-System Sync Status
LEDGER_FILE="$HOME/truth_mandate/ledger/mission_ledger.jsonl"
if [ -f "$LEDGER_FILE" ]; then
    TOTAL_LEDGER_RECORDS=$(wc -l < "$LEDGER_FILE" | tr -d ' ')
else
    TOTAL_LEDGER_RECORDS=0
fi

echo " -> Total DB Audit Records:   $TOTAL_DB_RECORDS"
echo " -> Total Ledger Line-Items:  $TOTAL_LEDGER_RECORDS"
echo " -> Last Registered Ingest:  $LAST_TIMESTAMP"
echo "----------------------------------------------------------------------"
echo " Recent Repository State Anchors (Git Log):"

cd $HOME/CivicAdvocate.OS
if [ -d ".git" ]; then
    git log --oneline -n 5
else
    echo " [!] Local Git tracking not initialized."
fi

echo "----------------------------------------------------------------------"
echo " Recent Logs In public.reaper_audit:"
psql -d u0_a540 -c "SELECT audit_id, intake_id, length(checksum) AS hash_size, reset_at FROM public.reaper_audit ORDER BY audit_id DESC LIMIT 3;"
echo "======================================================================"
