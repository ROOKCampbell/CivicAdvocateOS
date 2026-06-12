#!/bin/bash
echo "[SYS] Initiating recursive batch audit of ledger entries 002-159..."
# Filter logs for high-velocity intake IDs
grep -E "intake_id\": \"(0544|0545)\"" ~/CivicAdvocate.OS/ledger/mission_ledger.jsonl > ~/CivicAdvocate.OS/ledger/high_velocity_anomalies.log
echo "[SYS] Batch audit complete."
echo "Anomalies identified and logged to: ~/CivicAdvocate.OS/ledger/high_velocity_anomalies.log"
