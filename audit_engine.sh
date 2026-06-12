#!/bin/bash
# Reconstructed Audit Engine targeting local directory
KNOWN_ANOMALY_HASH="16eefc20941b9c16"
for file in *.txt *.log; do
    [ -f "$file" ] || continue
    FINGERPRINT=$(sha512sum "$file" | awk '{print $1}')
    if [[ "$FINGERPRINT" == "$KNOWN_ANOMALY_HASH"* ]]; then
        echo "[ALERT] Anomaly Detected in $file: $FINGERPRINT" | tee -a anomaly_flags.log
    fi
    echo "Processed $file: ${FINGERPRINT:0:16}..."
done
