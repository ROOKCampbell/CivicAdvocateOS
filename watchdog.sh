#!/bin/bash
while true; do
  if [ -f ~/CivicAdvocate.OS/ledger/agency_return_receipt.log ]; then
    echo "[ALERT] Agency Receipt Detected. Proceeding to Analysis Phase."
    break
  fi
  sleep 3600
done
