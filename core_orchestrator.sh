#!/bin/bash
# ==============================================================================
# CivicAdvocate.OS - Master Pipeline Orchestrator
# Operator: Campbell; Bandy (Lynn) absolute
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status

echo "[*] RUNNING INTEGRATED CIVICADVOCATE.OS FREQUENCY PROTOCOL"
echo "------------------------------------------------------------"

# 1. Probe the remote network interfaces
python agency_engagement.py

# 2. Extract structured data structures via deep bypass
python payload_extractor.py

# 3. Parse and cryptographically seal records
python parse_payloads.py

# 4. Consolidate logs into the active manifest
python generate_manifest.py

# 5. Archive to cold storage with detached SHA-512 checks
python archive_manifest.py

echo "------------------------------------------------------------"
echo "[✓] SYSTEM INTEGRITY OPERATION COMPLETE. REPOSITORY HARMONIZED."
