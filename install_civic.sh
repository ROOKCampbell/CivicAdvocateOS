#!/bin/bash
# CivicAdvocate.OS - Full Deployment Script for Termux

echo "[*] Installing dependencies..."
pkg install python -y
pip install ecdsa

echo "[*] Creating core architecture..."

# 1. Sync Client
cat << 'SYNC' > sync_client.py
import socket
def sync(peer_ip, port=5000):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((peer_ip, port))
    client.sendall(b'SYNC_REQUEST')
    data = client.recv(40960)
    with open("manifest.json", "w") as f:
        f.write(data.decode())
    print("[*] SYNC COMPLETE.")
    client.close()
sync("127.0.0.1")
SYNC

# 2. Audit Tool
cat << 'AUDIT' > audit_report.py
import json
with open("manifest.json", "r") as f:
    blocks = json.load(f)
proposals = [b for b in blocks if b.get('type') == 'PROPOSAL']
for p in proposals:
    votes = [b for b in blocks if b.get('type') == 'VOTE' and f"Proposal {p['id']}" in b['data']]
    yay = sum(1 for v in votes if "YAY" in v['data'])
    print(f"Law {p['id']}: '{p['data']}' | Votes: {yay}")
AUDIT

# 3. Genesis Init
echo '[{"id": 1, "data": "Genesis Block", "prev_hash": "0", "expected_hash": "0"}]' > manifest.json

echo "[*] CivicAdvocate.OS Deployment Complete."
