#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# CIVICADVOCATE.OS LOCAL DASHBOARD INITIALIZER (SPATIAL & INTEGRITY)
# ==============================================================================

clear
echo "==============================================================================="
echo "                  CIVICADVOCATE.OS INTERACTIVE FORENSIC MONITOR               "
echo "==============================================================================="
echo "[*] Target Anchor: 5b0114590998451a | Baseline: v1.0.0-strike"
echo "[*] Target Tract  : Silas Elbert Bandy Survey (Abstract 544)"

# Check monitoring daemon health status
PID=$(pgrep -f live_watcher.sh)
if [ -n "$PID" ]; then
    echo -e "[+] System State: \033[0;32mACTIVE_SURVEILLANCE\033[0m (PID: $PID)"
else
    echo -e "[!] System State: \033[0;31mWATCHER_DAEMON_OFFLINE\033[0m"
fi

echo "-------------------------------------------------------------------------------"
echo " Recent Evidentiary Ledger Activity:"

psql -d u0_a540 -c "
SELECT audit_id, intake_id, reset_at, SUBSTRING(checksum FROM 1 FOR 16) AS short_hash
FROM public.reaper_audit 
ORDER BY audit_id DESC 
LIMIT 5;
" 2>/dev/null || echo "[!] Database connection idle or structural mismatch."

echo "-------------------------------------------------------------------------------"
echo " Spatial Ingest Boundaries:"
echo " [Region] Texas-RRC Zone 5 | [Survey Key] SE-Bandy-A544 | [Status] SECURED"
echo "==============================================================================="
