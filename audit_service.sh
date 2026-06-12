# Paste the code above, then press Ctrl+O, Enter, and Ctrl+X#!/bin/bash

# Configuration
INGRESS_DIR="./data/ingress/cleburne"
ARCHIVE_DIR="./data/archive/cleburne"
LEDGER_FILE="./ledger/audit_trail.log"

# Initialization
mkdir -p "$INGRESS_DIR" "$ARCHIVE_DIR" "$(dirname "$LEDGER_FILE")"

echo "[AUDIT] Interface active: Monitoring $INGRESS_DIR"

# Execution Loop
while true; do
    # Check for files
    files=$(ls -A "$INGRESS_DIR")
    
    if [ -n "$files" ]; then
        for file_name in $files; do
            file_path="$INGRESS_DIR/$file_name"
            
            # Generate Metadata
            timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
            file_hash=$(sha512sum "$file_path" | awk '{print $1}')
            
            # Record to Ledger
            printf '{"timestamp": "%s", "source": "Cleburne_Municipal_Registry", "file": "%s", "hash": "%s"}\n' \
                "$timestamp" "$file_name" "$file_hash" >> "$LEDGER_FILE"
            
            # Archive
            mv "$file_path" "$ARCHIVE_DIR/$file_name"
            
            echo "[SUCCESS] Audited: $file_name | Hash: ${file_hash:0:16}..."
        done
    fi
    
    # Poll interval
    sleep 2
done
