#!/bin/bash
set -e

echo "[*] RUNNING INTEGRATED CIVICADVOCATE.OS FREQUENCY PROTOCOL"
echo "------------------------------------------------------------"

python agency_engagement.py
python payload_extractor.py
python parse_payloads.py
python rrc_production_audit.py
python generate_manifest.py
python generate_strike_package.py
python generate_default_notice.py # Added to continuous cycle
python archive_manifest.py

echo "------------------------------------------------------------"
echo "[✓] SYSTEM INTEGRITY OPERATION COMPLETE. REPOSITORY HARMONIZED."
