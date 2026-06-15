#!/bin/bash
# CivicAdvocate.OS Node Initialization Script
echo "[*] Initializing new CivicAdvocate node..."

# Ensure environment dependencies are present
pip install ecdsa

# Create the foundational ledger file
touch manifest.json
echo '[{"id": 1, "data": "Genesis Block", "prev_hash": "0", "expected_hash": "0"}]' > manifest.json

# Initialize local state
echo '{"active_rule": "NONE", "status": "INITIALIZED"}' > system_state.json

echo "[*] Node initialized successfully."
echo "[*] Point network_node.py to your peer's IP to begin synchronization."
