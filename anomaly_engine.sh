#!/bin/bash

# Configuration
AUDIT_LOG="./ledger/audit_trail.log"
MASTER_INDEX="./ledger/master_evidentiary_index.txt"
ANOMALY_LOG="./ledger/anomaly_alerts.log"

# Initialization & Integrity Check
mkdir -p ./ledger
# Ensure files exist before monitoring
touch "$AUDIT_LOG"
touch "$MASTER_INDEX"
touch "$ANOMALY_LOG"

echo "[ANOMALY ENGINE] Operational. Monitoring $AUDIT_LOG against Master Index..."

# Monitoring Loop
# Added tail -F to handle file truncation/recreation if necessary
tail -F "$AUDIT_LOG" | while read -r line; do
    # Extract hash (JSON format: {"hash": "..."})
    current_hash=$(echo "$line" | grep -o '"hash": "[^"]*' | cut -d'"' -f4)
    
    if [ -z "$current_hash" ]; then continue; fi

    # Check if hash exists in Master Index
    if ! grep -q "$current_hash" "$MASTER_INDEX"; then
        timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        echo "[$timestamp] ANOMALY DETECTED: Hash $current_hash not found in Master Index." | tee -a "$ANOMALY_LOG"
    else
        echo "[MATCH] Validated: $current_hash"
    fi
done
